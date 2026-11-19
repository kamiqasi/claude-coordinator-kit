---
name: while-we-wait
description: A worker has a request out. Pick the highest-priority thing the coordinator can do alone meanwhile, start it, and come back to the reply as soon as it lands.
argument-hint: "[item to do instead] [minutes]"
disable-model-invocation: true
---

# /while-we-wait $ARGUMENTS

**Read the setup file first:** `.claude/skills/coordinator-setup/SKILL.md` in this project if it exists,
else `~/.claude/skills/coordinator-setup/SKILL.md`. If neither exists, stop and say how to make one (the
kit's README, "Setup"). Work out this session's lane.

## 1. What we're waiting on
- List this lane's requests with no reply yet: compare `setup.lanes.folders.requests` with
  `setup.lanes.folders.replies`, and search the replies for each check token.
- Note how long each has been out and the expected wait: about 20 minutes for a small change, about 45 for
  a feature with tests, unless the request or past replies say otherwise.
- If nothing is out, say so in one line and run the `next` skill's steps (`../next/SKILL.md`) instead.

## 2. Candidates (filters first)
Start from `next`'s candidate list: this lane's tracker work (`setup.tracker.label`), what you owe from this
conversation, and the handoff's open items. Then drop, in this order, saying which went and why:
1. anything blocked by an in-flight request: the same branch or files, or it needs that result;
2. anything that needs the user's hands before it can move (those go under "Waiting on you");
3. other lanes' work;
4. anything that needs the busy worker. Queueing a **new request** for it is fine, if it touches other files.

What's left is work the coordinator can do alone: investigate, specify, review, read-only checks, tracker
upkeep, its own docs.

## 3. Rank (tuned for a wait)
Score with `next`'s five lenses (`setup.priority.weights`), reusing scores already given, but while waiting:
- **Lightness ×2.5** (it should fit the wait, or stop cleanly at a step);
- **I can drive ×2.5** (it must not need the user);
- the other lenses as usual.

Break a tie within 2 points by the smaller context switch: the same repo or topic as the work in flight wins.
If `$ARGUMENTS` names an item, take it and skip the ranking. If it gives minutes, use those as the wait.

## 4. Go
Say it in two lines, then start at once; the user can say stop:
`While we wait (<token>, out <n> min, ~<m> to go): <item>, because <the lens that decided it>. Next best: <item>.`

## 5. When the reply lands
A new reply for the awaited token comes first:
1. Finish the current step only; don't start another.
2. Park the side task in three lines: where it stopped, its exact next step, and the files it touched.
3. Review the reply as `inbox` does (`../inbox/SKILL.md`), and report.
4. End with one question: back to the parked task, or move on?
