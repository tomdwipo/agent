# Summarization Prompt Set
# Use '---' separators between tasks. Each block will be parsed as one prompt entry by the harness.

Title: Summarize QR Authentication PRD
Context:
Summarize the QR Authentication PRD into an executive brief for engineering and leadership. Use docs/sdlc-phase/prd-example.md and docs/features/01-prd-generation-v1.md as grounding for style and sectioning.

Input:
- Provide a 10-12 bullet executive summary.
- Include Goals, Success Metrics, Key Requirements, Major Risks, and Milestones.
- Keep to <= 200 words, crisp and factual.

Output:
An executive summary with labeled bullets.

---
Title: Summarize Android TRD for QR Authentication
Context:
Summarize the Android TRD version into a concise handoff note for backend and QA. Use docs/sdlc-phase/trd-example.md and docs/features/02-trd-generation-android.md as grounding.

Input:
- 8-10 bullets covering Architecture, APIs, Data Models, Security, Performance targets, Telemetry, and Test Plan.
- Highlight any open questions or dependencies.
- Limit 180 words.

Output:
A concise, technically dense summary for cross-team alignment.

---
Title: Summarize Figma MCP Registration Notes
Context:
Summarize docs/features/figma-mcp/user-registration-summary.md into actionable items.

Input:
- Output a checklist of 12-15 items covering UI adjustments, flows, accessibility, localization, and KYC.
- Group items by category and mark high-priority with [P1].

Output:
A categorized checklist ready for Jira import.