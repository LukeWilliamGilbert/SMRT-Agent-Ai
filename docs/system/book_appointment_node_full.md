# Full `bookAppointment` Node Evidence

Workflow: **🧠 SMRT Brain Engine** (`mlR5dZuzXxP_JYGaqrqpu`)

Type: `@n8n/n8n-nodes-langchain.toolCode`

## Description

```text
Book a consultation appointment.

INPUT (required JSON):
- selected_slot: string - ISO datetime from getAvailableSlots
- ghl_api_key: string - from system context
- calendar_id: string - from system context
- ghl_user_id: string - from system context
- contact_id: string - CONTACT_ID from context
- location_id: string - from context
- first_name: string - lead first name

Call getAvailableSlots first.
```

## JavaScript

```javascript
let input = {};
if (typeof query === 'string') { try { input = JSON.parse(query); } catch(e) { input = {selected_slot:query}; } } else if (typeof query === 'object' && query !== null) { input = query; }
const ctx = $('Assemble System Prompt').first().json;
const apiKey = ctx.ghlApiKey;
const calendarId = ctx.calendarId;
const ghlUserId = ctx.ghlUserId;
const locationId = ctx.locationId;
const contactId = ctx.contactId || input.contact_id;
const firstName = ctx.firstName || input.first_name || 'Lead';
const channel = ctx.channel || input.channel || 'sms';
const slot = input.selected_slot;
if (!slot || !apiKey) return 'Error: selected_slot required and GHL credentials not configured.';
const body = {calendarId,locationId,contactId,startTime:slot,title:'Consultation - '+firstName,appointmentStatus:'confirmed',assignedUserId:ghlUserId};
try {
  const r = await fetch('https://services.leadconnectorhq.com/calendars/events/appointments',{method:'POST',headers:{'Authorization':'Bearer '+apiKey,'Version':'2021-07-28','Content-Type':'application/json'},body:JSON.stringify(body)});
  const data = await r.json();
  // Write to Supabase appointments table
  try {
    const sbKey = ctx.supabaseServiceKey;
    const sbUrl = ctx.supabaseUrl;
    if (sbKey && sbUrl && data.id) {
      const endTime = data.endTime || new Date(new Date(slot).getTime() + 30 * 60000).toISOString();
      await fetch(sbUrl + '/rest/v1/appointments', {
        method: 'POST',
        headers: {
          'apikey': sbKey,
          'Authorization': 'Bearer ' + sbKey,
          'Content-Type': 'application/json',
          'Prefer': 'return=minimal'
        },
        body: JSON.stringify({
          agent_id: ctx.agentId || null,
          lead_id: ctx.leadId || null,
          contact_id: contactId,
          location_id: locationId,
          ghl_event_id: data.id,
          calendar_id: calendarId,
          start_time: slot,
          end_time: endTime,
          duration_minutes: 30,
          appointment_type: input.appointment_type || input.lead_intent || 'general',
          status: 'scheduled',
          booked_via: 'ai'
        })
      });
    }
  } catch (sbErr) { /* Supabase write is best-effort - GHL booking already succeeded */ }
  return JSON.stringify(data);
} catch(e) { return 'Error: '+e.message; }
```
