# Vistamail

Vistamail is a lightweight email client providing an easier way of storing and signing into
multiple email accounts, vistamail uses a "tab bar" for storing accounts similar to web browser tabs.

---

## Libraries Used

| Library | Purpose |
|---|---|
| `keyring` | used for storing passwords locally using Windows Credential Manager |
| `json` | used for storing user accounts locally |
| `smtplib` | used in sending emails securely with TLS and SSL (based on provider, see more details below) |
| `imap-tools` | used for downloading inboxes and html content |
| `TK / CTK` | main ui library used for its simplicity, lightness, and ease of reading for user modifications |

---

## Extra Info

smtp will run on different ports as per email provider:

| Provider          | Port 465 (SSL) | Port 587 (TLS) |
|-------------------|----------------|----------------|
| Gmail             | yes            | yes            |
| Outlook / Hotmail | no             | yes            |
| Yahoo Mail        | yes            | yes            |
| iCloud Mail       | yes            | yes            |
| Zoho Mail         | yes            | yes            |


As for imap it uses the same for all providers (993).
