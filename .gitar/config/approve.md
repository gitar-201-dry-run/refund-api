# Auto-approve criteria

Approve a pull request when both of these hold:

- Gitar's review has no unresolved findings. Minor suggestions do not count against the PR.
- The PR description links a GitHub issue (for example "Fixes #12"), and every objective listed in that issue is covered by the diff.

Withhold approval if the PR changes anything under `.gitar/`, `.github/`, or `migrations/` without a reviewer having asked for it in the linked issue.

A PR with no linked issue can still be approved when the review is clean and the change is small and self-contained (a typo, a docs fix, a dependency pin).
