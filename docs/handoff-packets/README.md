# Handoff Packets

A handoff packet is a short Markdown artifact that turns an Agent Gym experiment into a reusable prompt/ticket/run brief for Codex, Claude Code, or a future Agent Lab workflow.

This first slice is docs-only. The repo does not need a CLI yet because the useful behavior is the packet format itself: copy the template, fill in the fields, attach links to evidence, and hand it to the next agent or reviewer.

## When to use one

Use a handoff packet when a task needs more structure than a one-off prompt:

- A Codex or Claude Code run should start from known repo context.
- A future Agent Lab ticket needs reusable prompt material.
- IT Pro Direct work needs clear constraints before an agent edits files.
- Claims/legal demo work needs fake-data boundaries and non-goals stated up front.
- A reviewer needs to see the expected PR summary and scorecard target before work starts.

## How to create one

1. Copy [template.md](template.md) to `examples/handoff-packets/<short-name>.md`.
2. Fill in the project, objective, context, files to inspect first, constraints, validation commands, and stopping condition.
3. Link to a scorecard or leave the placeholder until the run is complete.
4. Keep the packet local and reviewable. Do not add cloud services, auth, databases, GitHub API calls, or Agent Lab coupling.

## Included example

- [Claims Demo Data Factory plan handoff](../../examples/handoff-packets/claims-demo-data-factory-plan.md)
- [Agent Lab issue #65: runs records page](../../examples/handoff-packets/agent-lab-issue-65-runs-records-page.md)

The claims example shows how a replayable bootstrap plan can become a safe Agent Lab seed for Agent Lab, IT Pro Direct, `claims-intelligence-foundation`, policy-dispute tools, and future sales demos without using real client data or production integrations.

The issue #65 example shows how to copy a local Agent Gym handoff packet into Codex or Claude Code for an Agent Lab implementation run while keeping Agent Gym local-only.
