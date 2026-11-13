---
name: create-individual-calendar-events-from-earnings-dates-list
description: "Create individual calendar events from an earnings dates list, one event per ticker with company name and reminder."
version: 1.0.0
author: DracieVajko
tags: [calendar, automation, parsing, earnings, reminders]
category: productivity
source_repository: https://github.com/DracieVajko/Dracievajko-SkillsSet
source_file: skills/original/create-individual-calendar-events-from-earnings-dates-list/SKILL.md
license: MIT
local_modifications: original
verification_status: verified
authorship: original
---

# Create Individual Calendar Events from Earnings Dates List

Create individual calendar events from an earnings dates list, one event per ticker with company name and reminder.

## When to Use

- The user has a list of earnings call dates with multiple tickers per day and needs each ticker entered as a separate calendar event with the company name and an alert.

## Procedure

1. Copy the email/text and extract each date line and the tickers listed beneath it.
2. For each ticker, look up the full company name (if not provided) and build an event title like "Earnings Call – TICKER (Company)".
3. Convert the human-readable date to an ISO-8601 timestamp in the desired timezone.
4. Call the calendar service to create an event with the title, start date, all-day flag and a reminder (e.g., 30 minutes before).
5. Repeat for every ticker, handling rate-limit or error responses.
6. Optionally verify the events were created by listing upcoming events for the target dates.

## Pitfalls

- Ambiguous dates or timezones.
- Rate limits on the calendar API.
- Missing company name lookup.

## Verification

- One event per ticker exists on the correct date.
- Each event has a reminder set.
