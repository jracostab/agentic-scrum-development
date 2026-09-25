# Comment commands (type on the GitHub issue)

| Command | Who acts | What |
|---------|----------|------|
| `/plan` | Developer or PO | Plan comment only. No code. |
| `/rca` | Developer | RCA comment only. No code. |
| `/implement` | Developer | Take ticket; still stop at G3. |
| `/assign po` `/assign tech-lead` `/assign developer` | Named hat / agent | That agent is next. |
| `approved` `proceed` `handle` | Founder | Pass gate. |
| `sprint yes` | Founder | Pass G2. |
| `send back` | Founder | Revise; still no code. |

Day-1 automation: none. You paste `/implement` then tell the Developer agent “issue #N”.

Day-2 optional Action (does not run the LLM): on issue_comment containing `/implement`, the Action comments:

```
Assigned Developer. Waiting G3 (plan/RCA + approved).
```

See github-action-stub.yml. Enable only if you want a visible checklist.
