---
name: wip
description: Everything in progress, one line each, issue first — what waits on you, what's out with the worker and in what state, what waits for review — with every link at the end in one block. Read-only.
argument-hint: "[all] (all = also list the other lanes' work in progress from the tracker)"
disable-model-invocation: true
---

# /wip $ARGUMENTS

**Read the setup file first:** `.claude/skills/coordinator-setup/SKILL.md` in this project if it exists,
else `~/.claude/skills/coordinator-setup/SKILL.md`. If neither exists, stop and say how to make one (the
kit's README, "Setup"). Work out this session's lane.

**Read-only:** change nothing, send nothing, write no file. Respect `setup.transport.limits` (stop on the first refusal).

## 1. Gather
- **Requests out:** this lane's requests in `setup.lanes.folders.requests` from the last 7 days
  (`setup.transport.list`). A request is open when no reply in `setup.lanes.folders.replies` quotes its
  check token: search the replies, one read each (`setup.transport.read`). Read the top of each open
  request for its token, its issue and one line of what it does.
  - **State,** read from the files, never guessed:
    - `queued`: no sign of work;
    - `uploading`: files for it exist in the replies folder (a bundle, screenshots), but no reply quoting the token;
    - `reply in`: the reply exists, and no review note of yours in `setup.lanes.folders.notes` names the token.
  - **Age** comes from the transport's upload time, not the filename, since a filename's time can be off.
    If `setup.transport.list_has_times` is false, use the filename's time and mark the age `~`.
  - **Queue position** is by upload time: the oldest open request is `#1`.
- **Replies to review:** replies with no review note of yours in `setup.lanes.folders.notes` naming their token.
- **Tracker** (skip if `setup.tracker.kind` is `none`): this lane's open work in progress or in review,
  with `setup.tracker.list` and `setup.tracker.label`. With `all`, the other lanes in `setup.lanes.names`
  too, listed separately, titles and links only.
- **Waiting on you** (`setup.people.approver`): from this conversation and the tracker. PRs to merge,
  commands to run, decisions. Each gets its URL and the exact action.
- **No extra GitHub calls** just for this. Use PR states you already know from this session, and mark
  them "as of HH:MM".

## 2. Report
Keep it tight. Each line starts with the issue id (or `—`). Use these sections in this order, and leave out an empty one:

1. **Waiting on you:** `ISSUE · what · the action · URL`
2. **With the worker:** `ISSUE · what · token · state · age · #position`
3. **Waiting for my review:** `ISSUE · what · reply file`
4. **In progress, nothing out:** `ISSUE · title · the next step and who owns it`
5. **Other lanes** (only with `all`): `ISSUE · title · URL`

End with **Links**: one fenced block, one URL per line, every issue and PR named above, de-duplicated,
in the order above, so they can all be opened at once.

No closing question unless something is stuck: a request out more than 2 hours, a reply waiting more
than 30 minutes, or a decision blocking two or more items. Then name it in one line.
