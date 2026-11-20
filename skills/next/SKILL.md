---
name: next
description: Where did we leave off and what's next — what's waiting on you, what's in flight, and a weighted ranking of the candidates with one recommended next item.
argument-hint: "[minutes available] [clear] [weights e.g. impact=2 urgency=3] [score overrides e.g. 'login bug: urgency=5']"
disable-model-invocation: true
---

# /next $ARGUMENTS

**Read the setup file first:** `.claude/skills/coordinator-setup/SKILL.md` in this project if it exists,
else `~/.claude/skills/coordinator-setup/SKILL.md`. If neither exists, stop and say how to make one (the
kit's README, "Setup"). Work out this session's lane.

## 1. Gather the state (read-only)
- this conversation, and this lane's newest handoff in `setup.lanes.folders.handoffs`;
- the inbox: the `inbox` skill's listing step only (`../inbox/SKILL.md`), without the reviews;
- open PRs on `setup.repos`, polling no more often than `setup.github.poll_minutes`;
- the tracker, if `setup.tracker.kind` isn't `none`: this lane's open work in its agreed order (`setup.tracker.list`);
- each item in `setup.project_checks.next`.

## 2. Rank the candidates
**Candidates** are the work items that could be next: 3 to 7 of them. Don't rank items that only wait on the
user; those go under "Waiting on you". Mention other lanes' big items only as context, never to take them over.

**Score each candidate 1–5 on every lens,** higher is better. The weights are `setup.priority.weights`, or these:

| Lens | Weight | 5 means |
| --- | --- | --- |
| Impact | ×3 | clearly advances a goal the user cares about |
| Urgency | ×2 | time-sensitive, or unblocks other work |
| Lightness | ×1.5 | little total effort to done |
| I can drive | ×1.5 | the coordinator and the worker can finish it without the user's hands |
| Safety | ×1 | small blast radius, reversible |

**Total** = Σ score × weight; the maximum is 5 × Σ weights (45 with these).

**Adjust from `$ARGUMENTS`, and say what you changed:**
- `clear`, or a time budget under 60 minutes: Lightness ×3 and I can drive ×2.5 (clear-the-plate mode);
- `lens=value`: set that weight, 0 to 3 in steps of 0.5;
- `<item>: lens=n`: the user's own score, which beats your guess. Impact and Urgency are theirs to set;
  mark your own guesses for those with `~`.

Reuse scores the user gave earlier in this conversation, or saved in memory, rather than guessing again.

## 3. Report, in this order
1. **Waiting on you:** each item with its full clickable URL and the exact action (merge, approve, run this
   command). Put first what unblocks the most.
2. **In flight:** worker requests by token and how long each has been out. Flag one with no reply for over two hours.
3. **Ranking:** a compact table of each candidate's five scores and its total out of the maximum, sorted.
   Mark the leader; call it a tie if the top two are within 2 points.
4. **Next:** the leader, the one or two lenses that decide it, and its size. If `$ARGUMENTS` gives minutes,
   say what fits, and what to send the worker while the user is away.

Keep it short. End with one question that lets the user say go or retune: "Change a weight or a score?"
