# Coordinator kit for Claude Code

Site: https://kamiqasi.github.io/claude-coordinator-kit/

Two Claude Code sessions, two jobs: a **coordinator** that plans, writes the spec and reviews, and a **worker** that builds.
They pass plain files through any shared folder; you approve and merge.
This kit is the coordinator's side of that loop, as nine skills and one setup file.

## The loop

```
  you ──► /send ──► request file ──► worker builds, opens a PR, writes a reply
                                                   │
          ┌─────────── /while-we-wait ◄────────────┤  (the coordinator works alone meanwhile)
          ▼                                        ▼
       /inbox ──► /review-pr ──► verdict ──► you merge ──► /merged ──► /next

  /wip, any time: everything in flight, and every link in one block
```

Every request carries a **check token**; the worker quotes it in its reply, so nothing is matched by guesswork.
The coordinator re-runs the checks itself instead of trusting the worker's account of them.

## Commands

| Command | Use it when |
| --- | --- |
| `/send` | you've agreed what to build: it writes the request (decisions, steps, a `Verify:` command, stop points) and hands it to the worker |
| `/inbox` | a reply may have landed: it reads it, reviews it, records a verdict and tells you what's waiting on you |
| `/review-pr` | a PR is up: it reads the diff before the worker's story, runs the checks itself, and says ready, fixes or blocked |
| `/merged` | you merged: it checks main holds what was reviewed, checks the rollout, and queues the next phase |
| `/next` | you're back and wonder what's next: it lists what waits on you and ranks the candidates |
| `/wip` | you want the whole picture: everything in progress, issue first, each request's state and age, all the links in one block |
| `/while-we-wait` | the worker is busy: it picks something the coordinator can do alone, and drops it when the reply lands |
| `/walkthrough` | you need to run a step yourself: plain words, trade-offs, copy-paste commands |
| `/handoff` | the session is ending: it writes a handoff for the next coordinator session |

Installed as a plugin, the commands are namespaced: `/coordinator-kit:send`, `/coordinator-kit:inbox`, and so on.

## Install

**As a plugin** (Claude Code's plugin marketplaces; this repo is both the marketplace and the plugin):

```sh
claude plugin marketplace add kamiqasi/claude-coordinator-kit
claude plugin install coordinator-kit@coordinator-kit
```

Inside a session, the same is `/plugin marketplace add kamiqasi/claude-coordinator-kit`, then
`/plugin install coordinator-kit@coordinator-kit`.

**Or copy the skills** (commands without the prefix: `/send`, `/inbox`, ...):

```sh
git clone https://github.com/kamiqasi/claude-coordinator-kit
cp -r claude-coordinator-kit/skills/* ~/.claude/skills/
```

## Setup

The skills hold no site facts. They read them from one file you write: copy the example and fill it in.

```sh
mkdir -p ~/.claude/skills/coordinator-setup
cp -n claude-coordinator-kit/coordinator-setup.example/SKILL.md ~/.claude/skills/coordinator-setup/SKILL.md
```

Put it in `.claude/skills/coordinator-setup/` inside a project instead, to give that project its own setup.
It covers:

- **transport:** where requests and replies go, and how to list, read and write them. A synced folder, a
  network share, a WebDAV server or a git repo all work;
- **lanes:** one coordinator/worker pair each, with their folders and file names. Run two to keep each
  session's context small;
- **protocol:** your rules for what the worker may do without asking;
- **labels** and **notices** (optional): the words that mark a step only you may run, and short notes
  between coordinators of different lanes;
- **tracker** (optional), **repos**, **GitHub limits**;
- **project checks:** your own commands, run at review, after a merge, and by `/next`;
- **priority weights** for `/next`.

## The worker

The worker is an ordinary Claude Code session started with a prompt that says: watch the requests folder,
work each request on the branch it names, open the PR, and write a reply that quotes the check token,
says what it ran, and lists its deviations. It never merges. The kit doesn't ship that prompt, since it
depends on what your worker may touch; write it next to your `protocol`.

## What it is not

Not a framework, not a server, and not agent hosting. It is Markdown that Claude Code reads. Nothing runs
unless a session runs it, and every merge is yours.

## Develop

```sh
python3 tests/check_kit.py      # frontmatter, names, setup keys, site links
claude plugin validate .        # the plugin and marketplace manifests
```

The site is `docs/` (static HTML and CSS, served by GitHub Pages from `main` `/docs`).

## Licence

MIT. See `LICENSE`.
