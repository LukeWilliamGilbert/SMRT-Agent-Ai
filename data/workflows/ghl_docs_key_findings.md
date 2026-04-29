# HighLevel Documentation Key Findings

**Date:** 2026-04-29  
**Purpose:** Preserve browser-derived facts used for SMRT GoHighLevel boundary documentation.

The official HighLevel API documentation describes comprehensive API coverage for CRM contacts, conversations, calendar/events, opportunities, payments, and webhooks. It states that contacts manage leads and customer data; conversations handle SMS, email, and call communications; calendar/events schedule appointments and manage calendar events; and webhooks provide real-time notifications for platform events.

The official HighLevel `Get Appointments for Contact` documentation defines the endpoint `GET https://services.leadconnectorhq.com/contacts/:contactId/appointments`. It requires the `contacts.readonly` scope, accepts OAuth Access Token or Private Integration Token authentication, uses a Sub-Account Token, and returns appointment events for a specified `contactId`.

References:

[1]: https://marketplace.gohighlevel.com/docs/ "HighLevel API Documentation"
[2]: https://marketplace.gohighlevel.com/docs/ghl/contacts/get-appointments-for-contact/ "Get Appointments for Contact | HighLevel API"
