# PRD Prompt Set
# Use '---' separators between tasks. Each block will be parsed as one prompt entry by the harness.

Title: PRD for QR Authentication Feature
Context:
You are a product manager creating a Product Requirements Document (PRD) for a "QR Authentication" feature for a mobile banking app. Follow the 8-section PRD template from docs/features/01-prd-generation-v1.md and docs/sdlc-phase/prd-example.md, covering: Overview, Goals/Non-Goals, Success Metrics, User Stories, Requirements, Assumptions/Dependencies, Risks, and Milestones.
Provide structured, concise, and actionable content.

Input:
Key points:
- Allow login via scanning a dynamic QR code on web that authorizes the mobile banking session
- Must mitigate phishing and replay attacks
- Aligns with existing SSO and device binding
- Success metric: 95% completion rate within 8 seconds
- Target platforms: iOS/Android for mobile app, modern browsers for web
- Requires backend token service and secure QR generation
- Compliance: PCI and bank security policies
- Integration with notification service for fallback

Output:
A complete PRD with the 8 sections as headings (H2 or H3), bullets where helpful, and crisp acceptance criteria, reflecting the constraints above.
---
Title: PRD for Bill Payment Reminders
Context:
Produce a PRD for "Bill Payment Reminders" using the same 8-section structure. Ground it in the approach and style in docs/features/01-prd-generation-v1.md.

Input:
Key points:
- Users can set reminders for utility bills; ingest due dates from providers or manual entry
- Cross-channel reminders: push notifications and email
- Smart snooze and auto-pay suggestions
- KPI: Increase on-time payments by 15%
- Constraints: Respect notification quiet hours, opt-in required, multi-language support

Output:
A complete PRD with clear goals, requirements, success metrics, and risks.
---
Title: PRD for Figma MCP User Registration Summary
Context:
Using docs/features/figma-mcp/user-registration-summary.md as grounding, produce a PRD summarizing the requirements for "User Registration" improvements extracted from Figma via MCP workflow.

Input:
Key points (derive from doc and assume standard banking KYC):
- Streamlined signup with progressive disclosure
- Support passwordless option via email magic link
- KYC document capture with edge case handling
- KPI: Drop-off reduction at step 2 by 20%

Output:
A complete PRD with the 8 sections and explicit assumptions/dependencies tied to Figma MCP extraction.