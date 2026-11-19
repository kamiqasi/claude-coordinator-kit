---
name: merged
description: The user merged PR(s) — verify the merge landed what you reviewed, check the rollout, check the inbox, and queue the next phase.
argument-hint: "<pr numbers, optionally repo> e.g. 406 or app#406 infra#39"
disable-model-invocation: true
---

# /merged: merged $ARGUMENTS

**Read the setup file first:** `.claude/skills/coordinator-setup/SKILL.md` in this project if it exists,
else `~/.claude/skills/coordinator-setup/SKILL.md`. If neither exists, stop and say how to make one (the
kit's README, "Setup"). Work out this session's lane.

1. **Resolve each PR.** A bare number means the repo of the work in flight. If that's ambiguous, look it up
   on `setup.repos` with `setup.github.cli`.
2. **Verify the merge.** For each PR:
   - it's `MERGED`; note the merge commit;
   - main now contains the head you reviewed (compare trees). If main has commits you never reviewed,
     review them now;
   - if it merged before your review, review what landed on main, and put any fixes in a new request.
3. **Check the rollout** with `setup.project_checks.rollout`, by repo. Where nothing applies itself (a
   plan, an apply, a deploy someone runs by hand), give `setup.people.approver` the exact command and what
   to expect, and say where to stop (a replace or delete it didn't ask for).
4. **Check the inbox** (`../inbox/SKILL.md`) for replies that arrived meanwhile.
5. **Close the loop:**
   - if `setup.tracker.kind` isn't `none`, comment on the issue with what shipped;
   - delete merged branches only if the user has asked for that in this session;
   - if a next phase is agreed and specified, send it to this lane's worker (`../send/SKILL.md`).
     Otherwise propose it in one line.
6. **Report:** what's live and verified, what the user still has to run (exact commands), and what's next,
   with full URLs.
