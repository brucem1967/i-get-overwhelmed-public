# i-get-overwhelmed

A Claude Code plugin that shapes Claude's replies for a non-technical reader who gets overwhelmed by too much information:
a calm first line, one thing at a time, plain words, click-by-click steps that say what you will see, Claude doing the work
itself where it can, and one easy question at the end.

Forked from [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) (MIT). Same plugin shape and always-on switch;
different rules (`skills/i-get-overwhelmed/SKILL.md`).

## Optional: a profile of the reader

Add `skills/i-get-overwhelmed/READER.md` in your own copy with what Claude should know about the person (for example: not technical, prefers voice to typing, works nights, never ask for their passwords). The hook prints it straight after the rules, and it wins where it differs. Keep it out of any public repo.

## Install

```
claude plugin marketplace add bamboostack/i-get-overwhelmed-public
claude plugin install i-get-overwhelmed@i-get-overwhelmed
```

Always on (every session): create the empty file `~/.claude/.i-get-overwhelmed-always`.
Off for one session: say "stop overwhelm mode". Off for good: delete that file.
One session only, without always-on: type `/i-get-overwhelmed`.

## Update

```
claude plugin marketplace update i-get-overwhelmed
claude plugin update i-get-overwhelmed@i-get-overwhelmed
```

## Test

`python3 tests/test_hook.py`
