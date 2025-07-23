

### **Product Requirements Document: Passwordless QR Authentication**

*   **Document Version:** 1.0
*   **Date:** July 23, 2025
*   **Author:** team
*   **Status:** Draft
*   **Stakeholders:** Head of Digital Banking, Lead Mobile Engineer, Lead Web Engineer, Head of Security, Head of Customer Support

---

### **1. Introduction & Problem Statement**

**1.1. Problem:** The reliance on traditional passwords for our internet banking web portal presents a significant and growing liability. This model exposes customers to common cyber threats like phishing and credential stuffing, results in a frustrating user experience (forgotten passwords, account lockouts), and increases operational costs through high volumes of customer support calls.

**1.2. Vision:** To create a secure, seamless, and modern authentication experience for our web portal that delights users and eliminates the password as a point of failure.

**1.3. Proposed Solution:** We will implement a passwordless login system where users authenticate by scanning a QR code on the web portal with their already-authenticated mobile banking app. This shifts the security locus to the user's trusted mobile device, leveraging its inherent multi-factor capabilities (possession of the device + biometrics).

### **2. Goals & Objectives**

*   **Goal 1: Enhance Account Security.**
    *   **Objective:** Reduce account takeover incidents related to compromised passwords by over 90% within 12 months of launch.
*   **Goal 2: Improve User Experience.**
    *   **Objective:** Decrease the average time to log in on the web by at least 50%.
    *   **Objective:** Achieve a user satisfaction score (CSAT) of 4.5/5 or higher for the new login feature.
*   **Goal 3: Reduce Operational Costs.**
    *   **Objective:** Reduce the number of password-related support tickets by 75% within 6 months of launch.
*   **Goal 4: Drive Strategic Engagement.**
    *   **Objective:** Increase the adoption rate of the new login method to 60% of active web users within 12 months.

### **3. Scope**

**3.1. In Scope (Minimum Viable Product - MVP):**
*   A new "Login with Mobile App" button on the web portal login page.
*   Generation and display of dynamic, short-lived QR codes.
*   A QR code scanning function within the existing mobile app.
*   An approval/denial screen on the mobile app that displays contextual information (browser, location).
*   Real-time communication between the web and backend to reflect the login status.
*   The ability for a user to successfully log in to the web portal without a password.

**3.2. Out of Scope (Future Enhancements):**
*   "Number Matching" as an additional security challenge.
*   A user-facing "Trusted Device Management" dashboard.
*   Support for third-party authenticators or hardware keys.
*   Evolving the system to support FIDO2/Passkeys standard (slated for a future major release).
*   Password-based login will remain as a fallback option for the MVP but will be de-emphasized in the UI.

### **4. User Stories**

*   **US-1 (Happy Path):** As a bank customer, I want to log into the website by scanning a QR code with my phone, so that I can access my account quickly and without having to remember my password.
*   **US-2 (Security Context):** As a security-conscious user, I want to see details about the login attempt (like browser and location) on my phone before I approve it, so that I can be confident it's a legitimate request from me.
*   **US-3 (Expired Code):** As a user, if I take too long to scan the QR code, I want the system to inform me that it has expired and automatically provide a new one, so that I understand what happened and can easily try again.
*   **US-4 (Denial):** As a user, if I see a login request on my phone that I didn't initiate, I want to be able to easily deny it, so that I can prevent unauthorized access to my account.

### **5. Functional Requirements**

#### **5.1. Web Client Requirements**
*   **WR-1:** The main login page MUST prominently feature a "Login with Mobile App" button.
*   **WR-2:** Clicking this button MUST trigger a request to the backend for a `sessionToken` and display the returned token as a QR code.
*   **WR-3:** A visual countdown timer (e.g., 60 seconds) MUST be displayed next to the QR code.
*   **WR-4:** When the timer expires, the QR code MUST become visually invalid, and a new code MUST be automatically fetched and displayed.
*   **WR-5:** Upon successful scan by the mobile app, the UI MUST update in real-time to a state that says "Check your mobile to approve."
*   **WR-6:** Upon receiving final approval from the backend, the user MUST be securely authenticated and redirected to their account dashboard.
*   **WR-7:** If the login is denied or times out, the user MUST be returned to the initial login screen with a clear, user-friendly error message.

#### **5.2. Mobile Client Requirements**
*   **MR-1:** The mobile app MUST have a clearly accessible entry point to the QR scanner function.
*   **MR-2:** The scanner MUST be able to quickly and accurately read the QR code displayed on a web screen.
*   **MR-3:** Upon a successful scan, the app MUST send the `sessionToken` to the backend for verification.
*   **MR-4:** If the token is valid, the app MUST display a full-screen approval prompt. This screen MUST include:
    *   The application name ("Bank Internet Banking").
    *   Browser and OS information (e.g., "Chrome on Windows").
    *   Approximate geographic location (e.g., "Jakarta, Indonesia").
    *   Clear "Deny" and "Approve" buttons.
*   **MR-5:** Tapping "Approve" MUST require biometric confirmation (Face ID/Fingerprint) if enabled on the device.
*   **MR-6:** Upon user action (Approve/Deny), the decision MUST be sent to the backend.
*   **MR-7:** If an invalid or expired QR code is scanned, the app MUST display a clear error message (e.g., "This QR code has expired. Please refresh the web page.").

#### **5.3. Backend System Requirements**
*   **BR-1:** MUST expose a public, unauthenticated endpoint (`/qr-session`) to generate a unique, cryptographically random `sessionToken`.
*   **BR-2:** Each `sessionToken` MUST have a TTL of 60 seconds or less and be stored in a temporary cache.
*   **BR-3:** MUST expose an authenticated endpoint (`/verify`) for the mobile app to validate a `sessionToken` and associate it with the authenticated user's ID.
*   **BR-4:** MUST expose an authenticated endpoint (`/approve`) for the mobile app to confirm the login.
*   **BR-5:** MUST use a real-time communication channel (preferably WebSockets) to push status updates (`SCANNED`, `APPROVED`, `DENIED`) to the waiting web client.
*   **BR-6:** Upon final approval, the backend MUST create a secure web session (e.g., via a secure, HttpOnly cookie) for the originating web browser.

### **6. Non-Functional Requirements (NFRs)**

*   **NFR-1 (Performance):**
    *   The `/qr-session` API response time MUST be < 100ms.
    *   The end-to-end login process (from scan to web redirect) MUST complete in under 3 seconds.
*   **NFR-2 (Security):**
    *   All communication MUST use TLS 1.2 or higher.
    *   The `/qr-session` endpoint MUST be protected by IP-based rate limiting to prevent DoS attacks.
    *   The system must be protected against OWASP Top 10 vulnerabilities.
*   **NFR-3 (Reliability):**
    *   The authentication system MUST have an uptime of 99.9% or higher.
*   **NFR-4 (Usability & Accessibility):**
    *   The feature must be intuitive and require no user training.
    *   All web components MUST comply with WCAG 2.1 AA accessibility standards.
*   **NFR-5 (Scalability):**
    *   The system MUST be able to handle a load of at least 500 concurrent login attempts without performance degradation.

### **7. Success Metrics**

*   **Adoption Rate:** Percentage of web logins initiated via QR code vs. password.
*   **Login Success Rate:** Percentage of initiated QR logins that are successfully completed.
*   **Average Login Time:** `time(scan_start)` to `time(web_dashboard_load)`.
*   **Support Ticket Volume:** Number of tickets categorized as "Forgot Password" or "Login Issues."
*   **CSAT Score:** User satisfaction ratings collected via in-app surveys after a successful login.