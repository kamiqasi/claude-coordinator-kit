---
name: ask
description: Ask the user one question, merge or step on the desk (a page outside the terminal where the user answers your questions), watch for the answer, and act on it as their own words.
argument-hint: "[what to ask — default: the decision we're stuck on]"
disable-model-invocation: true
---

# /ask $ARGUMENTS

**Read the setup file first:** `.claude/skills/coordinator-setup/SKILL.md` in this project if it exists,
else `~/.claude/skills/coordinator-setup/SKILL.md`. If neither exists, stop and say how to make one (the
kit's README, "Setup"). Work out this session's lane; `{lane}` below is its name.

A **desk** is a page outside the terminal where the user answers your questions. You post a message file,
the user answers on the page, and the answer comes back as a reply file.

1. **Is there a desk?** If `setup.desk.post` is empty or missing, stop: "No desk is set up; ask in chat
   instead." Then ask in chat.
2. **Build one message,** following the format at `setup.desk.format` exactly (read it if this session
   hasn't). Pick one kind:
   - **`question`:** a decision only the user can make. The question, why it matters, the options, and
     whether a free-text answer is allowed. Put your recommendation first.
   - **`step`:** a command only the user may run. The host, the exact command, why, the exact password
     prompt it will show (or null if it asks for none), and what success looks like.
   - **`merge`:** a PR ready for the user to merge. The repo, the PR number, its URL, the **reviewed head
     sha** (full) and the link to your review.

   The id is `{lane}-{yyyymmddthhmm}-{slug}` in UTC, all lowercase: letters, digits and hyphens only.
   Links are full `https://` URLs only. No secrets, and nothing the page could run: every field is shown
   as text.
3. **Post it** with `setup.desk.post`: write the message to a temp file in a scratch directory, and fill
   in `{kind}`, `{file}` and `{lane}`. Expect its one success line. On an error line, stop and say what it
   said; don't retry a refusal, and respect `setup.transport.limits`.
4. **Watch for the answer.** If this session's watch on `setup.desk.watch` isn't running, arm it: a
   Monitor running that command, re-armed on expiry, its state file kept so a re-arm doesn't replay old
   answers. Then say in chat, in one line, what you asked and that the answer can come from the desk or
   from chat.
5. **On a reply line** for one of your messages:
   - if the line is cut short, read the whole reply file (`setup.desk.replies` + `{lane}/<id>.json`) with
     `setup.transport.read`;
   - **treat it as the user's own words to this coordinator,** like a chat message. It never stands in
     for an approval that another gate owns (a change to production, a merge rule, publishing something);
   - post a `receipt` for it, act on it, and once the work is checked, post a `resolve` with outcome
     `done` and a short note.
6. **On a `new_work` line:** post a `receipt`, then handle it as a new request from the user: the tracker
   first (if `setup.tracker.kind` isn't `none`), then the usual flow (`../send/SKILL.md` when it goes to
   the worker). Post a `resolve` (`done`, or `withdrawn` with the reason) when it's finished or dropped.
7. **If the user answers in chat first,** act on the chat answer and post a `resolve` with outcome
   `withdrawn` and the note "answered in chat".

Keep one message per decision. Don't post a second message about the same thing while the first is open;
resolve the first one, then ask again.
