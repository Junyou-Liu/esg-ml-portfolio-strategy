# GitHub Publishing Notes

Recommended repository name:

```text
finai-esg-allocation-strategy
```

Create a new **empty** GitHub repository under `Junyou-Liu`:

- do not add a GitHub README,
- do not add a GitHub `.gitignore`,
- do not add a license during repository creation.

This local project already contains those files and a clean initial commit.

After the empty repository is created, run the following commands from this folder:

```bash
git remote add origin https://github.com/Junyou-Liu/finai-esg-allocation-strategy.git
git push -u origin main
```

The project includes a roadshow video of roughly 73 MB. This is below GitHub's 100 MB single-file hard limit, but it should be pushed with Git from the command line rather than uploaded through the GitHub web file uploader.
