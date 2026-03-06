# JobMarket

This repository contains the industry resume source used for GitHub and Overleaf.

## Files

- `main.tex`: current resume source
- `.gitignore`: LaTeX and local artifact ignores

## Local build

```bash
latexmk -pdf main.tex
```

This should generate `main.pdf`.

## Create the GitHub repo

If `gh` is authenticated:

```bash
gh repo create JobMarket --public --source=. --remote=origin --push
```

## Sync with Overleaf

Two common options:

1. Connect the GitHub repo from Overleaf, if your Overleaf plan supports GitHub sync.
2. Add the Overleaf Git remote to this repo and push to it.

Example:

```bash
git remote add overleaf <overleaf-git-url>
git push overleaf main
```

## Notes

The initial `main.tex` was copied from `INDUSTRY/ANTHROPIC_202601/ANTHROPIC_CV_202601.tex`.

