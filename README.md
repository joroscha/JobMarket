# JobMarket

This repository contains the industry resume source used for GitHub and Overleaf.

## Files

- `resume_cv/`: resumes, CVs, cover letters, and local LaTeX build artifacts
- `interview_prep/`: interview prep notes, scripts, and notebooks
- `industry_meeting_notes/`: company-specific meeting notes, trackers, and cheatsheets
- `.gitignore`: LaTeX and local artifact ignores

## Local build

```bash
cd resume_cv
latexmk -pdf jose_oros_cv_202604.tex
```

This should generate the PDF in `resume_cv/`.

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

The initial `resume.tex` was copied from `INDUSTRY/ANTHROPIC_202601/ANTHROPIC_CV_202601.tex`.
