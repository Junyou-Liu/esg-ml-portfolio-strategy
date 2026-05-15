from lumibot.strategies import Strategy as LumibotStrategy

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


class Strategy(LumibotStrategy):
    """
    Two-level ESG allocation strategy.

    Level 1: Market-regime estimation using an ESG broad-market proxy (ESGU).
      - Features: lagged daily returns, RSI, and realized volatility.
      - Models: Random Forest by default, with Logistic Regression available.
      - Outputs: next-day up probability and near-term pullback probability.
      - Regimes: RISK_ON, NEUTRAL, RISK_OFF.

    Level 2: Core-satellite ESG portfolio construction.
      - Core ESG beta: ESGU, VSGX, SUSA.
      - Green-theme satellite sleeve: ICLN, TAN, LIT, QCLN.
      - Defensive asset: SHY.
      - Within each sleeve, the strategy selects the top two ETFs by
        six-month momentum and allocates 70/30 between them.
    """

    def initialize(self, model_type="RF"):
        self.sleeptime = "1D"
        self.model_type = model_type.upper()

        # Tradable universe.
        self.core = ["ESGU", "VSGX", "SUSA"]
        self.sat = ["ICLN", "TAN", "LIT", "QCLN"]
        self.def_asset = "SHY"
        self.trade_syms = self.core + self.sat + [self.def_asset]

        # Regime model configuration.
        self.regime_proxy = "ESGU"
        self.training_days = 252 * 2
        self.feature_lags = 5
        self.lookforward_days = 7

        self.risk_on_prob = 0.55
        self.risk_off_prob = 0.45
        self.dd_ok = 0.50
        self.dd_bad = 0.60

        if self.model_type == "LR":
            self.model = LogisticRegression(max_iter=1000)
        else:
            self.model_type = "RF"
            self.model = RandomForestClassifier(
                n_estimators=200,
                max_depth=5,
                random_state=42,
            )

        self.scaler = StandardScaler()

        # Refit periodically to reduce portfolio churn and computation.
        self.regime_retrain_every = 5
        self._regime_iter = 0
        self.last_prob_up = 0.5
        self.last_dd_prob = 0.5
        self.last_regime = "NEUTRAL"

        # Portfolio construction parameters.
        self.mom_lookback = 126
        self.top2_w1 = 0.70
        self.top2_w2 = 0.30
        self.risk_budget = {"RISK_ON": 0.95, "NEUTRAL": 0.65, "RISK_OFF": 0.40}
        self.sat_share_by_regime = {"RISK_ON": 0.30, "NEUTRAL": 0.20, "RISK_OFF": 0.10}
        self.def_split_shy = 0.85

        # Execution controls.
        self.drift_tolerance = 0.02
        self.min_trade_value = 100.0
        self.min_trade_shares = 1

        self.log_message(
            f"Initialized Two-Level ESG Strategy | model_type={self.model_type} "
            f"regime_proxy={self.regime_proxy} retrain_every={self.regime_retrain_every}D"
        )

    # -------- Level 1: regime model helpers --------
    def _bars_to_df(self, bars):
        if bars is None:
            return None

        if hasattr(bars, "df") and bars.df is not None:
            df = bars.df.copy()
        else:
            try:
                df = pd.DataFrame(bars)
            except Exception:
                return None

        df.columns = [str(c).lower() for c in df.columns]
        if "close" not in df.columns:
            return None

        return df.dropna(subset=["close"]).reset_index(drop=True)

    def _feature_columns(self):
        return [f"lag_{i}" for i in range(1, self.feature_lags + 1)] + ["rsi", "vol"]

    def _calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["close"] = df["close"].astype(float)

        df["ret"] = df["close"].pct_change()
        df["vol"] = df["ret"].rolling(window=10).std()

        delta = df["close"].diff()
        gain = delta.where(delta > 0, 0.0).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0.0)).rolling(window=14).mean()
        df["rsi"] = 100.0 - (100.0 / (1.0 + (gain / (loss + 1e-9))))

        for i in range(1, self.feature_lags + 1):
            df[f"lag_{i}"] = df["ret"].shift(i)

        return df.dropna()

    def _prepare_ml_data(self):
        bars = self.get_historical_prices(
            self.regime_proxy,
            length=self.training_days + 60,
            timestep="1D",
        )
        df = self._bars_to_df(bars)
        if df is None or len(df) < (self.feature_lags + 80):
            return None, None, None

        df = self._calculate_indicators(df)
        features = self._feature_columns()
        feature_frame = df[features].dropna()
        if feature_frame.empty:
            return None, None, None

        future_ret = df["ret"].shift(-1)
        train_index = feature_frame.index.intersection(future_ret.dropna().index)
        if len(train_index) < 80:
            return None, None, None

        X_train = feature_frame.loc[train_index].values
        y = (future_ret.loc[train_index] > 0).astype(int).values
        X_latest = feature_frame.iloc[[-1]].values
        return X_train, y, X_latest

    def _predict_drawdown_probability_7d(self) -> float:
        """
        Estimate near-term pullback risk using a secondary classifier.

        The label is 1 when the future seven-day average return of ESGU is
        negative, and 0 otherwise.
        """
        try:
            bars = self.get_historical_prices(
                self.regime_proxy,
                length=self.training_days + 80,
                timestep="1D",
            )
            df = self._bars_to_df(bars)
            if df is None or len(df) < (self.lookforward_days + 120):
                return 0.5

            df = self._calculate_indicators(df)
            features = self._feature_columns()
            feature_frame = df[features].dropna()
            future_ret_7d = df["ret"].rolling(window=self.lookforward_days).mean().shift(-self.lookforward_days)
            train_index = feature_frame.index.intersection(future_ret_7d.dropna().index)

            if len(train_index) < 200:
                return 0.5

            X_train = feature_frame.loc[train_index].values
            y = (future_ret_7d.loc[train_index] < 0).astype(int).values
            if len(np.unique(y)) < 2:
                return 0.5

            dd_model = RandomForestClassifier(
                n_estimators=80,
                max_depth=3,
                random_state=42,
            )
            dd_model.fit(X_train, y)
            p = float(dd_model.predict_proba(feature_frame.iloc[[-1]].values)[0, 1])
            return p if np.isfinite(p) else 0.5
        except Exception as exc:
            self.log_message(f"Drawdown model error: {exc}")
            return 0.5

    def _decide_regime(self, prob_up: float, dd_prob: float) -> str:
        if prob_up > self.risk_on_prob and dd_prob < self.dd_ok:
            return "RISK_ON"
        if prob_up < self.risk_off_prob or dd_prob > self.dd_bad:
            return "RISK_OFF"
        return "NEUTRAL"

    # -------- Level 2: portfolio construction helpers --------
    def _momentum_score(self, sym: str) -> float:
        bars = self.get_historical_prices(sym, length=self.mom_lookback + 5, timestep="1D")
        df = self._bars_to_df(bars)
        if df is None or len(df) < self.mom_lookback + 1:
            return np.nan
        close = df["close"].astype(float)
        return float(close.iloc[-1] / close.iloc[-(self.mom_lookback + 1)] - 1.0)

    def _pick_top2(self, symbols):
        scored = []
        for sym in symbols:
            score = self._momentum_score(sym)
            if np.isfinite(score):
                scored.append((sym, score))
        scored.sort(key=lambda item: item[1], reverse=True)
        return [sym for sym, _ in scored[:2]]

    def _alloc_top2(self, targets, picks, weight):
        if weight <= 0 or not picks:
            return targets
        if len(picks) == 1:
            targets[picks[0]] += weight
        else:
            targets[picks[0]] += weight * self.top2_w1
            targets[picks[1]] += weight * self.top2_w2
        return targets

    def _build_targets(self, regime: str):
        equity_budget = float(self.risk_budget.get(regime, 0.65))
        sat_share = float(np.clip(self.sat_share_by_regime.get(regime, 0.20), 0.0, 1.0))
        core_share = max(0.0, 1.0 - sat_share)

        core_picks = self._pick_top2(self.core)
        sat_picks = self._pick_top2(self.sat)
        targets = {sym: 0.0 for sym in self.trade_syms}

        if not core_picks:
            targets["ESGU"] = 0.60
            targets[self.def_asset] = 0.30
            targets["CASH"] = 0.10
            return targets, core_picks, sat_picks, equity_budget, sat_share

        w_core = equity_budget * core_share
        w_sat = equity_budget * sat_share if sat_picks else 0.0
        targets = self._alloc_top2(targets, core_picks, w_core)
        targets = self._alloc_top2(targets, sat_picks, w_sat)

        w_def = max(0.0, 1.0 - (w_core + w_sat))
        targets[self.def_asset] = w_def * self.def_split_shy
        targets["CASH"] = w_def * (1.0 - self.def_split_shy)
        return targets, core_picks, sat_picks, equity_budget, sat_share

    # -------- Execution helpers --------
    def _safe_last_price(self, sym: str) -> float:
        try:
            price = self.get_last_price(sym)
            price = float(price)
            return price if np.isfinite(price) and price > 0 else np.nan
        except Exception:
            return np.nan

    def _rebalance(self, targets):
        portfolio_value = float(self.get_portfolio_value())
        if portfolio_value <= 0:
            return

        planned_trades = []
        for sym in self.trade_syms:
            position = self.get_position(sym)
            current_qty = float(position.quantity) if position is not None else 0.0
            price = self._safe_last_price(sym)
            if not np.isfinite(price):
                continue

            current_weight = (current_qty * price) / portfolio_value
            desired_weight = float(targets.get(sym, 0.0))
            if abs(desired_weight - current_weight) <= self.drift_tolerance:
                continue

            target_qty = int(round((portfolio_value * desired_weight) / price))
            delta_qty = target_qty - int(round(current_qty))
            if abs(delta_qty) < self.min_trade_shares:
                continue
            if abs(delta_qty) * price < self.min_trade_value:
                continue

            side = "buy" if delta_qty > 0 else "sell"
            planned_trades.append((sym, abs(int(delta_qty)), side))

        # Sell first to reduce cash-pressure issues during a rebalance.
        planned_trades.sort(key=lambda trade: 0 if trade[2] == "sell" else 1)
        for sym, quantity, side in planned_trades:
            order = self.create_order(sym, quantity, side)
            self.submit_order(order)

    def on_trading_iteration(self):
        self._regime_iter += 1
        do_retrain = (self._regime_iter == 1) or (self._regime_iter % self.regime_retrain_every == 0)

        if do_retrain:
            prob_up = 0.5
            try:
                X_train, y, X_latest = self._prepare_ml_data()
                if X_train is not None and len(y) > 50 and len(np.unique(y)) > 1:
                    if self.model_type == "LR":
                        X_train_scaled = self.scaler.fit_transform(X_train)
                        X_latest_scaled = self.scaler.transform(X_latest)
                        self.model.fit(X_train_scaled, y)
                        prob_up = float(self.model.predict_proba(X_latest_scaled)[0, 1])
                    else:
                        self.model.fit(X_train, y)
                        prob_up = float(self.model.predict_proba(X_latest)[0, 1])
            except Exception as exc:
                self.log_message(f"Regime ML error: {exc}")
                prob_up = 0.5

            dd_prob = self._predict_drawdown_probability_7d()
            regime = self._decide_regime(prob_up, dd_prob)
            self.last_prob_up = prob_up
            self.last_dd_prob = dd_prob
            self.last_regime = regime
        else:
            prob_up = self.last_prob_up
            dd_prob = self.last_dd_prob
            regime = self.last_regime

        targets, core_picks, sat_picks, equity_budget, sat_share = self._build_targets(regime)
        train_flag = "RETRAIN" if do_retrain else "CACHED"
        self.log_message(
            f"[{train_flag}] REGIME={regime} proxy={self.regime_proxy} model={self.model_type} "
            f"prob_up={prob_up:.2f} dd_prob_7d={dd_prob:.2f} "
            f"equity_budget={equity_budget:.2%} sat_share={sat_share:.0%} "
            f"core_picks={core_picks} sat_picks={sat_picks}"
        )
        self.log_message(f"targets={targets}")

        self._rebalance(targets)
