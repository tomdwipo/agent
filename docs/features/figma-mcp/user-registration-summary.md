# Figma Design Summary: Create Account - Confirm Data

This document summarizes the components and user flow of the "Create Account - Confirm Data" screen from the provided Figma design.

## Screen Overview

The screen is designed for user registration and is composed of two main parts:
1.  A registration form for users to input their data.
2.  A confirmation dialog to verify the entered information before finalizing the account creation.

## Components

### 1. Top Navigation Bar
-   **Title:** "Buat Akun" (Create Account)
-   **Left Icon:** Back arrow for navigation.
-   **Right Icon:** Support Agent icon.

### 2. Registration Form
This form is contained within a card with a shadow effect.
-   **Required Fields Indicator:** A text label `* Wajib Diisi` (* Required) at the top.
-   **Input Fields:**
    -   **Nama Lengkap (Full Name):** Text input with a placeholder.
    -   **E-mail:** Text input for email address.
    -   **Nomor Handphone (Phone Number):** Text input with a `+62` prefix for the country code.
    -   **Password:** Password input field with a show/hide icon. It includes a helper text: "Min. 8 karakter dari huruf besar, kecil & angka" (Min. 8 characters from uppercase, lowercase letters & numbers).
    -   **Konfirmasi Password (Confirm Password):** Another password input field for confirmation.
-   **"Buat Akun" (Create Account) Button:** A primary button to submit the form.
-   **Login Link:** A link for users who already have an account: "Sudah memiliki akun? Masuk Akun" (Already have an account? Log In).

### 3. Confirmation Dialog
This dialog appears as a modal overlay on top of the registration form.
-   **Icon:** An alert triangle icon.
-   **Title:** "Konfirmasi Data Anda" (Confirm Your Data).
-   **Message:**
    -   "Pastikan nomor HP Anda benar dan aktif" (Make sure your phone number is correct and active).
    -   "Nomor Handphone: +62 87876754***" (partially masked phone number).
    -   "Anda akan registrasi sebagai bagian dari:[Nama Perusahaan]" (You will register as part of: [Company Name]).
-   **Buttons:**
    -   **"Kembali" (Back) Button:** A secondary button to return to the form.
    -   **"Konfirmasi" (Confirm) Button:** A primary button to finalize the registration.

### 4. Footer
-   A text stating the user agrees to the Terms & Conditions and Privacy Policy upon registration.

## User Flow

1.  The user lands on the "Buat Akun" screen.
2.  The user fills in the registration form with their full name, email, phone number, and password.
3.  The user clicks the "Buat Akun" button.
4.  The "Konfirmasi Data Anda" dialog appears, showing the partially masked phone number and the company they are joining.
5.  If the user clicks "Kembali", the dialog closes, and they can edit the form.
6.  If the user clicks "Konfirmasi", the account is created, and they would proceed to the next step in the application (e.g., OTP verification or login).

This summary provides a high-level understanding of the screen's design and functionality. The next step will be to create a detailed Technical Requirement Document (TRD).