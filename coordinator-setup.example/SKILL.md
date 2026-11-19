---
name: coordinator-setup
description: Your site's facts for the coordinator kit — transport, lanes, tracker, repos, checks and limits. Reference only; the other coordinator skills read it first.
disable-model-invocation: true
---

# Coordinator setup

**This is the one file you write.** Every other skill in the kit is generic and reads its facts from here.
Copy this folder to `~/.claude/skills/coordinator-setup/` (all your projects) or to
`.claude/skills/coordinator-setup/` in one project (that copy wins), drop the `.example` from the folder
name, and fill in the block below. Delete the lines you don't use; a skill skips a step whose key is missing.

The skills refer to a key as `setup.<key>`, e.g. `setup.lanes.folders.requests`. `{lane}` in a value is
replaced by the session's lane name.

```yaml
transport:                     # how the coordinator and the worker pass files. Any shared folder works.
  kind: shared folder          # a synced folder, a network share, a WebDAV server, a git repo of notes...
  root: ~/coordination         # where the folders below live (a path, or a URL)
  list: ls -t {folder}         # how to list a folder, newest first
  list_has_times: true         # the listing gives each file's upload time; false: /wip falls back to filenames
  read: cat {file}             # how to read one file
  write: cp {local} {file}     # how to upload one file; must fail rather than overwrite someone else's
  overwrite: cp {local} {file} # how to replace a file you wrote yourself
  limits: ""                   # e.g. "stop on the first 403: repeated failures ban the host"
  secret: ""                   # where a password or token is read from (a file path); never print it

lanes:                         # a lane is one coordinator/worker pair; run several to keep contexts small
  names: [main]                # e.g. [main, second]
  default: main                # used when the session can't tell
  how_to_tell: ""              # e.g. "the start prompt names the lane", or "the folder the session runs in"
  folders:
    requests: requests/{lane}/          # requests the coordinator writes for the worker
    replies: replies/{lane}/            # the worker's replies
    notes: notes/{lane}/                # the coordinator's reviews and notes
    handoffs: handoffs/{lane}/          # handoffs between coordinator sessions
  names_of:
    request: "{UTC}-{slug}.md"                  # {UTC} is YYYY-MM-DDTHHMM
    reply: "{UTC}-worker-{lane}-{slug}.md"
    review: "{UTC}-coordinator-{lane}-{slug}-review.md"
    handoff: "{UTC}-coordinator-{lane}.md"
  monitor:
    state: ~/.cache/coordinator-kit/seen-{lane}  # what the inbox watch has already reported
    command: ""                # the command your start prompt arms to watch the replies folder, if any
  start_command: ""            # how the user starts the next coordinator session for this lane
  worker_start: ""             # how the user starts or nudges this lane's worker

protocol: ""                   # path to your rules: what the worker may do without asking (its standing
                               # go-ahead), and what always needs you. Requests point the worker at it.

people:
  approver: you                # who merges, approves and runs privileged steps
  hosts: []                    # where the user runs commands, e.g. ["laptop", "build server (ssh build)"]

tracker:                       # the issue tracker; leave kind: none to skip every tracker step
  kind: none                   # GitHub Issues, Linear, Jira, none
  label: ""                    # the label that marks this lane's work; {lane} is replaced, e.g. "lane-{lane}"
  comment: ""                  # how to comment on an issue, e.g. "gh issue comment {n} --body-file {file}"
  list: ""                     # how to list open work in order, e.g. "gh issue list --label {label}"

repos:                         # the repos the worker may change; the coordinator only reads them
  - owner/repo

github:
  cli: gh                      # the GitHub CLI to use (some setups wrap it)
  poll_minutes: 10             # poll GitHub no more often than this
  limits: ""                   # e.g. "a shared hourly token cap: stop on the first refusal"
  git_prefix: ""               # anything git over HTTPS needs in front, e.g. a group wrapper

project_checks:                # your own checks; each skill runs the list for its step, if present
  review: []                   # run at a PR's head when reviewing, e.g. ["make test", "kubectl kustomize overlays/staging"]
  render: ""                   # how to screenshot UI changes, e.g. "headless Chromium at 1280 and 375 px"
  rollout: []                  # after a merge, per repo, e.g. ["app: the deploy job for the merge commit passed"]
  next: []                     # extra state for /next, e.g. ["unhealthy pods", "open alerts"]

priority:                      # /next and /while-we-wait rank with these lenses (1-5 each, higher is better)
  weights: {impact: 3, urgency: 2, lightness: 1.5, drive: 1.5, safety: 1}
```

When this file is run on its own (it shouldn't be), print the lane names and their four folders in two lines.
