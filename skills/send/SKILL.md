---
name: send
description: Go with the recommendations and send the work to this lane's worker as a written request — decisions, steps, checks and stop points — then confirm it arrived intact.
argument-hint: "[item, issue or phase to send — default: what we just agreed]"
disable-model-invocation: true
---

# /send $ARGUMENTS

**Read the setup file first:** `.claude/skills/coordinator-setup/SKILL.md` in this project if it exists,
else `~/.claude/skills/coordinator-setup/SKILL.md`. If neither exists, stop and say how to make one (the
kit's README, "Setup"). Work out this session's lane; the request goes **only** to its
`setup.lanes.folders.requests`.

1. **What to send:** `$ARGUMENTS`, or the item just discussed.
   - Take your own recommendations as the decisions, unless the user overrode them in this conversation.
   - If something is still genuinely the user's call (cost, security posture, deleting data), ask that one
     question first instead of sending.
2. **Write the request,** following `setup.protocol` if it sets a format:
   - a title line;
   - **`Check token: \`<word>-<slug>-<4 chars>\``**, unique across every lane (search the requests
     folders first). The worker quotes it in its reply;
   - context, with issue and PR links;
   - **decisions**, numbered, so the worker follows them and lists deviations instead of stopping to ask;
   - the repo (one of `setup.repos`) and the branch name;
   - numbered steps, each with its check;
   - **`Verify: \`<command>\``** for code: one POSIX `sh` command that must exit 0 at the PR's head on a
     clean checkout. You run it yourself at review; the worker's own run is a claim, not the check. Leave
     it out for docs-only or read-only work, and say why;
   - **hard rules:** repo scope, no merge, no force-push, list deviations rather than stopping, no secrets;
   - **`Approver step:`** on every step the worker may not do alone under `setup.protocol` (privileged
     commands, merges, deletes, new dependencies, other repos), so it knows where to stop before it starts.
     Don't add "confirm first" to steps it may do (commit, push, PR, reply);
   - stop conditions and a rollback;
   - the exact reply filename (`setup.lanes.names_of.reply`) and what the reply must contain.
3. **Upload** it to `setup.lanes.folders.requests`, named as `setup.lanes.names_of.request`, with
   `setup.transport.write`. Respect `setup.transport.limits`. Read it back to confirm it's intact.
4. **Tracker:** if `setup.tracker.kind` isn't `none`, comment on the issue (`setup.tracker.comment`) that the
   work went to the worker, with the token.
5. **Report in three lines:**
   - what was sent, with the token and where it is;
   - how the user starts or nudges the worker (`setup.lanes.worker_start`);
   - whether a watch is running for the reply.
