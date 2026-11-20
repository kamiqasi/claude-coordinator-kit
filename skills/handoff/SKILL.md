---
name: handoff
description: Wrap up the session — write and upload this lane's coordinator handoff, save durable facts to memory, and give the command that starts the next session.
argument-hint: "[notes to include]"
disable-model-invocation: true
---

# /handoff $ARGUMENTS

**Read the setup file first:** `.claude/skills/coordinator-setup/SKILL.md` in this project if it exists,
else `~/.claude/skills/coordinator-setup/SKILL.md`. If neither exists, stop and say how to make one (the
kit's README, "Setup"). Work out this session's lane.

1. **Re-check before writing:** the inbox listing (`../inbox/SKILL.md`, step 1, including notices if
   `setup.notices.folder` is set), open PRs, and the state of each in-flight token. The handoff must describe
   now, not an hour ago. Name any notice still waiting for your reply.
2. **Write the handoff:** under about 80 lines, addressed to the next session of the same role and lane:
   - **done,** with links;
   - **in flight:** each item's exact next step and its check token;
   - **waiting on the user,** with full URLs and exact commands;
   - **the agreed backlog order;**
   - **open decisions;**
   - **quirks and known false positives;**
   - anything in `$ARGUMENTS`.
3. **Upload** it to `setup.lanes.folders.handoffs`, named as `setup.lanes.names_of.handoff`, with
   `setup.transport.write`, and read it back.
4. **Memory:** save the durable facts learned this session (not the in-flight state; that belongs in the
   handoff).
5. **Tell the user** where the handoff is, and the start command for the next session
   (`setup.lanes.start_command`). Remind them that the worker writes its own handoff if it has work in flight.
