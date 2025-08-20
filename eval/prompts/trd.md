# TRD Prompt Set
# Use '---' separators between tasks. Each block will be parsed as one prompt entry by the harness.

Title: TRD for QR Authentication Feature (Android)
Context:
You are a senior Android engineer writing a Technical Requirements Document (TRD) for the "QR Authentication" feature referenced in the PRD. Follow TRD sections from docs/features/02-trd-generation-android.md and docs/sdlc-phase/trd-example.md, covering: Introduction, Architecture Overview, Data Models, API Contracts, Flows/Sequence Diagrams (describe textually), Security/Privacy, Performance/Telemetry, Testing Strategy, Risks/Mitigations, and Delivery Plan. Include JSON examples for request/response and any config.

Input:
Key points:
- Dynamic QR generated on web encodes a short-lived nonce; mobile app scans via CameraX
- Mobile calls Token Service to exchange nonce for session token bound to device
- OIDC/SSO alignment required; PKCE where applicable
- Anti-replay: single-use nonce, 30s TTL, server invalidates post-use
- Phishing mitigation with signed QR payload and issuer domain check
- Platforms: Android 8+; ensure camera permissions and fallback PIN auth
- Telemetry: scan duration, success/failure reason codes
- Performance target: end-to-end under 8s p95 including network

Output:
Produce a complete Android-focused TRD with the sections above. Provide API JSON examples, data model definitions, and a clear sequence of calls.

---
Title: TRD for Bill Payment Reminders (Android)
Context:
Create an Android TRD for the "Bill Payment Reminders" feature. Use the same TRD section structure and style in docs/features/02-trd-generation-android.md.

Input:
Key points:
- Reminder sources: provider feeds (pull) and manual user entry
- Local scheduling using WorkManager; push notifications originate from backend
- Quiet hours and locale-aware formatting
- Deep links to bill details and “Pay Now”
- Performance: notification trigger jitter <= 1 minute
- Telemetry: opt-in rate, notification delivery vs open, conversion to payment

Output:
A complete TRD with architecture diagram description, WorkManager scheduling strategy, data schema, API contracts, and testing matrix.

---
Title: TRD for Figma MCP User Registration Improvements (Android)
Context:
Using docs/features/figma-mcp/user-registration-summary.md as grounding, write an Android TRD for "User Registration" improvements extracted via MCP pipeline.

Input:
Key points:
- Progressive disclosure for signup; screens and components informed by Figma nodes
- Passwordless magic link option with email verification
- KYC capture: document scan with edge cases (glare, crop, blur)
- Accessibility and localization from Figma tokens
- Telemetry: funnel events per step

Output:
A detailed TRD with data models, API flows, UI navigation graph, KYC error handling paths, and logging schema.