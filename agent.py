import os
import json
from dotenv import load_dotenv
from calendar_utils import get_available_slots, create_event
from dateutil.parser import parse
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

load_dotenv()
tz = ZoneInfo("Asia/Kolkata")

# Initialize Duckling

import dateparser
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

tz = ZoneInfo("Asia/Kolkata")

def extract_datetime(user_input):
    """
    Uses dateparser to extract start and end datetime from user input.
    Returns (start, end) in ISO format or (None, None) if not found.
    """
    # Parse start time
    start_dt = dateparser.parse(user_input, settings={'TIMEZONE': 'Asia/Kolkata', 'TO_TIMEZONE': 'Asia/Kolkata', 'RETURN_AS_TIMEZONE_AWARE': True})
    
    if start_dt:
        # If duration is not mentioned, default to +1 hour
        end_dt = start_dt + timedelta(hours=1)
        return start_dt.isoformat(), end_dt.isoformat()
    
    # ❌ If nothing parsed
    return None, None


def book_slot_agent(user_input):
    """
    Main agent function that:
    - Checks availability if user asks
    - Books meetings based on user input
    - Handles edge cases gracefully
    """
    user_input_lower = user_input.lower()

    # Check availability queries
    if any(word in user_input_lower for word in ["available", "free", "availability"]):
        events = get_available_slots()
        if not events:
            return "✅ You are completely free. No events scheduled."
        else:
            response = "📅 Here are your upcoming events:\n"
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                response += f"- {event['summary']} at {start}\n"
            response += "\nLet me know if you want to book a slot around these."
            return response

    # Booking intent
    elif any(word in user_input_lower for word in ["book", "schedule", "meeting", "call"]):
        start_time, end_time = extract_datetime(user_input)
        print("Parsed times:", start_time, end_time)
        if not start_time or not end_time:
            return "⚠️ Sorry, I couldn’t understand the time you want. Please try phrases like 'Book a call tomorrow 3-4 PM'."

        # Check for conflicting events
        events = get_available_slots()
        for event in events:
            existing_start_str = event['start'].get('dateTime', event['start'].get('date'))
            existing_end_str = event['end'].get('dateTime', event['end'].get('date'))

            try:
                existing_start = parse(existing_start_str).astimezone(tz)
                existing_end = parse(existing_end_str).astimezone(tz)
                desired_start = parse(start_time).astimezone(tz)
                desired_end = parse(end_time).astimezone(tz)

                # Check if existing event overlaps with desired time
                if existing_start < desired_end and desired_start < existing_end:
                    return f"❌ You already have '{event['summary']}' during this time. Please choose another slot."

            except Exception as e:
                print("Conflict check parsing error:", e)
                continue

        # No conflict, proceed to book
        link = create_event(start_time, end_time)
        return f"✅ Meeting booked successfully!\nHere’s your calendar link: {link}"

    # Fallback for unrecognized input
    else:
        return "👋 I can help you check your availability or book a slot. Please tell me what you’d like to do!"

