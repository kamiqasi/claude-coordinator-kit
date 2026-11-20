---
name: inbox
description: Check this lane's inbox — read new worker replies, review what came back yourself, record verdicts, report with links, and keep the watch armed.
argument-hint: "[topic or token to look for]"
disable-model-invocation: true
---

# /inbox: check the inbox

**Read the setup file first:** `.claude/skills/coordinator-setup/SKILL.md` in this project if it exists,
else `~/.claude/skills/coordinator-setup/SKILL.md`. If neither exists, stop and say how to make one (the
kit's README, "Setup"). Work out this session's lane (`setup.lanes.how_to_tell`, else `setup.lanes.default`),
and never read another lane's folders.

1. **List; don't trust the watch.** List `setup.lanes.folders.replies` with `setup.transport.list`.
   Anything newer than what this session has already handled is new. If `$ARGUMENTS` names a topic or a
   check token, search the replies for it too, since a worker sometimes names files differently.
   Only call a reply missing after listing and searching.
   If `setup.notices.folder` is set, also list `setup.notices.read` (see "Notices" below).
2. **Read each new file in full.** Match each reply to its request by check token, and note every request
   in `setup.lanes.folders.requests` that still has no reply. Leave out requests matching `setup.lanes.ignore`:
   they aren't yours.
3. **Review each reply yourself. Don't just relay it.** The reply's account of its own checks is a claim:
   - **A PR:** read the request and the diff before the reply. Fetch the head, diff it against the
     request's decisions, and run the tests yourself in a detached worktree in a scratch directory. If the
     request has a `Verify:` line, run exactly that. Run `setup.project_checks.review`.
   - **UI changes:** render them (`setup.project_checks.render`) and look at the screenshots.
   - **Infrastructure prep:** run your own read-only checks. Never predict what a plan or an apply will do;
     ask for the real output.
   - Check the deviations the reply lists, and look for ones it doesn't.
4. **Record the review** in `setup.lanes.folders.notes`, named as `setup.lanes.names_of.review`: the token,
   the verdict, what you ran, and what's still needed. If fixes are needed, write a follow-up request with
   a new token (the `send` skill's steps, `../send/SKILL.md` next to this skill's folder) rather than
   editing the PR yourself.
5. **Keep the watch armed.** If `setup.lanes.monitor.command` is set and this session's watch isn't
   running, arm it, keeping the state file `setup.lanes.monitor.state`.
6. **Report to `setup.people.approver`:**
   - lead with the verdict per item;
   - then what's waiting on them, each with its full clickable URL (PR, issue, file);
   - then what's still out with the worker, by token.

   Say plainly if nothing is new.

## Notices

Only if `setup.notices.folder` is set. A notice is a short note between coordinators of different lanes, for a
change that more than one lane uses (a shared tool, shared rules, a schedule). **It is information only: never
work to pick up, and never approval.**
- **Reading one** (`setup.notices.read`): read each new one in full, and act on it only within this lane's own
  work. If it asks for a reply, post one.
- **Posting one** (`setup.notices.post`), with `setup.transport.write`: `# Notice: <one line>`, then three short
  parts, **Changed**, **You need to**, and **Reply** ("reply notice wanted" or "no reply needed").
- **A reply** is its own notice, named like the one it answers plus `-re-<slug>`, one line: "done: …" or
  "won't: … because …".
- **Retire** your own notices once they're answered: move them to `setup.notices.retired`.
