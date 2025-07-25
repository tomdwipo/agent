# TRD - Quality Assurance: "Glass Box" Test Plan v1.1 (On-the-Fly)

| | |
| :--- | :--- |
| **Document ID:** | TRD-QA-01 |
| **Version:** | 1.1 |
| **Status:** | Ready for Testing |
| **Author:** | Goose AI (QA) |
| **Related Docs:**| PRD, TRD-BE-01 (v1.1), TRD-FE-01 (v1.1) |

---

### **1. Introduction & Objective**

This document outlines the quality assurance strategy and test plan for the "Glass Box" Traceability Feature, updated for the "on-the-fly" workflow. Its purpose is to provide the QA team with a comprehensive set of test cases to ensure the feature is high-quality, stable, and meets all requirements.

### **2. Scope of Testing**

#### **In-Scope Features:**
-   End-to-end flow of generating a document with traceability from raw text input.
-   API validation for the `/generateDocument` endpoint.
-   UI functionality of the input form, document viewer, and source-link modal.
-   Interaction logic, including icon clicks, hover states, and modal behavior.
-   Error handling for both API and UI states.
-   Basic performance and security validation.

#### **Out-of-Scope Features:**
-   User ability to edit or create traceability links.
-   AI model accuracy (we are testing that the *system works*, not that the *AI's writing is perfect*).
-   Sentence-level traceability.
-   AI Confidence Scoring.

### **3. Testing Environments**

-   **Local:** Developers will test locally using the Firebase Emulator Suite.
-   **Staging:** QA will perform the bulk of their testing on a dedicated staging environment, which mirrors production and connects to live Firebase services and the OpenAI API.
-   **Production:** A final smoke test will be performed on the live production environment immediately after release.

### **4. Testing Strategy**

-   **Unit & Integration Testing (Developer-Led):** Backend and Frontend developers are responsible for writing and maintaining a suite of automated tests for their respective codebases.
-   **API Testing (QA-Led):** QA will independently test the `/generateDocument` endpoint using an API client (e.g., Postman, Insomnia) to verify its contract and error handling.
-   **Manual & Exploratory Testing (QA-Led):** QA will perform all the test cases outlined below on the staging environment and conduct exploratory testing to find edge cases not covered in the scripts.

---

### **5. Test Cases**

#### **5.1 API Test Cases (`/generateDocument`)**

| Test Case ID | Description | Steps | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **API-01** | **Happy Path** | Send a `POST` request with a valid `source_title`, `source_content`, and auth token. | `200 OK`. Response body matches the API contract. Check Firestore/Storage to confirm both documents were created. | P0 |
| **API-02** | **Invalid Body (Missing Field)**| Send request with no `source_content`. | `400 Bad Request`. Error message indicates missing field. | P1 |
| **API-03** | **Invalid Body (Empty Content)** | Send request with `source_content` as an empty string. | `400 Bad Request`. | P2 |
| **API-04** | **Auth (No Token)** | Send request without an `Authorization` header. | `401 Unauthorized`. | P0 |
| **API-05** | **Auth (Invalid Token)** | Send request with an invalid or expired token. | `401 Unauthorized`. | P1 |

#### **5.2 Frontend UI & Functional Test Cases**

| Test Case ID | Description | Steps | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **FE-01** | **Form Validation** | 1. Go to the generation page. 2. Leave title or content empty. | The "Generate" button should be disabled. | P1 |
| **FE-02** | **Loading State** | 1. Fill out the form. 2. Click "Generate". | A loading spinner or skeleton screen appears immediately. The form is hidden/disabled. | P1 |
| **FE-03** | **Success State** | 1. Wait for successful generation. | The `DocumentView` appears, displaying the generated text. The loading spinner and form are gone. | P0 |
| **FE-04** | **API Error State** | 1. Trigger a backend error. | A user-friendly error message is displayed *within the form context*. The form remains visible and editable. | P1 |
| **FE-05** | **Icon Visibility** | 1. View a successfully generated document. | The `🔗` icon appears next to sections that have a source link. | P0 |
| **FE-06** | **Icon Hover State** | 1. Hover the mouse over the `🔗` icon. | Icon changes color and a tooltip appears ("View Source in PRD"). | P2 |
| **FE-07** | **Modal Open** | 1. Click the `🔗` icon. | The `SourceLinkModal` appears over the main content. | P0 |
| **FE-08** | **Modal Close** | 1. Open the modal. 2. Click the 'X' button. 3. Re-open. 4. Click outside the modal. | The modal closes in both cases. | P1 |
| **FE-09** | **Modal Content & Highlighting**| 1. Open the modal. | The correct source document is displayed, and the correct source paragraphs are highlighted with a distinct background color. | P0 |
| **FE-10**| **Modal Auto-Scroll** | 1. Open the modal for a source deep within a long document. | The modal content automatically scrolls down to the first highlighted paragraph. | P1 |


#### **5.3 End-to-End (E2E) Test Cases**

| Test Case ID | Description | Steps | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **E2E-01** | **Full Happy Path** | 1. As a logged-in user, navigate to the "Generate" page. 2. Enter a title and paste PRD content. 3. Click "Generate". 4. Wait for completion. 5. Click a `🔗` icon. | The TRD is generated and displayed. The modal opens and shows the correct, highlighted source from the content entered in step 2. Both documents now exist in the database. | P0 |
| **E2E-02** | **Short Document** | Perform E2E-01 with `source_content` containing only one or two paragraphs. | The process completes successfully without errors. | P1 |
| **E2E-03** | **Long Document** | Perform E2E-01 with `source_content` containing 20+ paragraphs. | The process completes successfully. Modal scrolling works correctly. | P1 |
| **E2E-04** | **No Relevant Context** | Perform E2E-01 with content that has no relevant text for one of the target sections. | The generated text for that section should indicate that context was insufficient. The system does not crash. | P2 |

#### **5.4 Non-Functional Test Cases**

| Test Case ID | Description | Steps | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **NFR-01** | **Frontend Performance** | 1. Open browser dev tools. 2. Click a `🔗` icon. 3. Measure time until modal is rendered and scrolled. | The interaction must complete in **< 500ms** on a standard broadband connection. | P1 |

### **6. Defect Management**

-   All bugs found during testing will be logged in Jira (or the project's designated bug tracker).
-   Defects will be assigned a priority level (P0-P3).
-   All P0 ("Showstopper") and P1 ("Critical") bugs must be fixed and verified before the feature can be approved for release.

### **7. Exit Criteria**

The "Glass Box" feature will be considered **QA Approved** and ready for production release when the following conditions are met:
1.  All P0 and P1 bugs have been resolved and closed.
2.  All test cases in this plan have been executed, with a pass rate of 100% for P0 and P1 test cases.
3.  Any open P2 or P3 bugs have been reviewed with the Product Owner and consciously deferred to a future release.
4.  A final E2E smoke test has been successfully performed on the staging environment.
