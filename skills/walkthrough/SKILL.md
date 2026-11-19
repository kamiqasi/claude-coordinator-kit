---
name: walkthrough
description: Walk the user through the current step — the point in plain words, any real trade-off, and copy-paste commands for the host they run them on.
argument-hint: "[topic — default: the last thing discussed]"
disable-model-invocation: true
---

# /walkthrough $ARGUMENTS

**Read the setup file first:** `.claude/skills/coordinator-setup/SKILL.md` in this project if it exists,
else `~/.claude/skills/coordinator-setup/SKILL.md`. If neither exists, stop and say how to make one (the
kit's README, "Setup"). It names the user's hosts (`setup.people.hosts`).

Explain `$ARGUMENTS`, or the last step discussed, so the user can act on it without guessing.

1. **The point first:** one or two sentences, in plain words, on what it does and why it matters now. Skip
   settled background.
2. **The trade-offs,** only if there's a real choice: the options, what each costs, and your recommendation.
3. **The steps.** Number them, and give each one:
   - **where it runs:** which of `setup.people.hosts`, or which web UI, and as which user;
   - **the exact command,** in its own block, ready to paste. No placeholders to work out; if a value is
     unknown, give the command that finds it;
   - **what success looks like,** and what to paste back if it doesn't.
4. **Safety:**
   - call out anything destructive or hard to reverse, and put the check before it (plan before apply,
     stopped before destroy);
   - never ask the user for a secret value; read it from a file, or prompt for it with `read -s`.
5. If you're unsure of a fact (a hostname, a menu name, a flag), check it first, or say you haven't.
