---
name: review-pr
description: Review a PR as the coordinator — form your own view from the request and the diff, weigh AI-review comments, run the checks yourself, record a verdict and say if it's ready to merge.
argument-hint: "<pr> [repo]   (no args: the PRs this lane's worker just opened)"
disable-model-invocation: true
---

# /review-pr $ARGUMENTS

**Read the setup file first:** `.claude/skills/coordinator-setup/SKILL.md` in this project if it exists,
else `~/.claude/skills/coordinator-setup/SKILL.md`. If neither exists, stop and say how to make one (the
kit's README, "Setup"). Work out this session's lane.

With no arguments, review every open PR this lane's worker opened since the last review: the PR URLs in its
replies (`setup.lanes.folders.replies`), or the open PRs on `setup.repos`.

For each PR:
1. **Context:** the request it answers (by check token) and its decisions; the tracker issue, if any; and
   the PR's head commit, state, files, comments and reviews (`setup.github.cli`, e.g.
   `gh pr view <n> --repo <owner/repo> --json headRefOid,state,files,comments,reviews`).
2. **AI reviews:** read every automated review comment. For each, decide: real and needs fixing, already
   handled, or a false positive.
3. **The diff, before the worker's reply.** Form your own view first; the reply's story and its checks are
   claims to compare against afterwards.
   - fetch, then `git diff origin/main...<head>`, reading every changed file;
   - check it against the request's decisions and hard rules;
   - check the listed deviations, and look for unlisted ones;
   - look for secrets, scope creep, and files the request said not to touch.
4. **Run it yourself** in a detached worktree in a scratch directory: the repo's own tests and linters, then
   `setup.project_checks.review`.
   - **If the request has a `Verify:` line, run exactly that at the PR's head.** A failure means not ready,
     whatever the reply says. If you can't run it, say so; never count the worker's run as yours.
   - **UI:** render it (`setup.project_checks.render`) and look at the screenshots.
   - **Config and infrastructure:** load what you can (parse the YAML, build the manifests), and check for
     changes that replace or delete live resources.
5. **Verdict:** *ready to merge*, *ready after fixes*, or *blocked*. For fixes, write one request to this
   lane's worker (`../send/SKILL.md`): a new token; new commits on the same branch, no force-push.
6. **Record** the review in `setup.lanes.folders.notes` (`setup.lanes.names_of.review`). Comment on the PR
   only if the user asks you to post it.
7. **Report:** the verdict first, then the reasons and the PR URL. Remove the worktree.
