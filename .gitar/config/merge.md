# Auto-merge criteria

Merge a pull request when it is approved and CI is green.

- Squash merge.
- Hold the merge when the PR is a draft, or when the diff touches more than 400 changed lines.
- Hold the merge when the PR changes `.gitar/config/` (the criteria in these files should only change through a human-reviewed PR).
