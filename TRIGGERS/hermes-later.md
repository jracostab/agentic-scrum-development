# Hermes later

When you move Developer / tech-lead agents to Hermes:

1. `hermes profile create pe --clone-from <po-profile>` (snapshot, not inherit). Team role is still DE/PE/CTO in the sidecar.
2. Pin skills: `agentic-scrum-po` on the Co-Founder profile; `agentic-scrum-tech-lead` on CTO/DE/PE; `agentic-scrum-developer` where they implement.
3. Optional: Hermes skill that shells out to `claude` if you still want Claude Code for implementation.

Do not do this on day 1. Co-Founder stays Hermes until one story has merged.
