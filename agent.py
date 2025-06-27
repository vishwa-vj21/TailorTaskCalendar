import os
import json
from dotenv import load_dotenv
from calendar_utils import get_available_slots, create_event
from dateutil.parser import parse
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

load_dotenv()
tz = ZoneInfo("Asia/Kolkata")


from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from dateparser.search import search_dates
import re
import dateparser
from datetime import timedelta
from zoneinfo import ZoneInfo

tz = ZoneInfo("Asia/Kolkata")
# Broad time keywords mapping
time_keywords = {
    "morning": ("09:00 AM", "10:00 AM"),
    "afternoon": ("01:00 PM", "02:00 PM"),
    "evening": ("06:00 PM", "07:00 PM"),
    "night": ("09:00 PM", "10:00 PM"),
}

def extract_datetime(user_input):
    print("\n📝 User input:", user_input)

    # 1. Handle phrases like "next week"
    if "next week" in user_input.lower():
        next_week = datetime.now(tz) + timedelta(days=7)
        base_date_str = next_week.strftime("%A")
        print("📅 Detected 'next week', base_date_str:", base_date_str)
        user_input = user_input.replace("next week", base_date_str)

    # 2. Extract date keywords
    date_match = re.search(r"(tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday)", user_input, re.IGNORECASE)
    date_word = date_match.group(1) if date_match else ""
    print("📅 Date keyword extracted:", date_word)

    date_only = dateparser.parse(
        date_word if date_word else "today",
        settings={
            'TIMEZONE': 'Asia/Kolkata',
            'TO_TIMEZONE': 'Asia/Kolkata',
            'RETURN_AS_TIMEZONE_AWARE': True,
            'PREFER_DATES_FROM': 'future',
        }
    )
    print("📅 Parsed date_only:", date_only)

    date_str = date_only.strftime('%Y-%m-%d')

    # 3. Check broad time keywords
    for key, (start_time, end_time) in time_keywords.items():
        if key in user_input.lower():
            start_str = f"{date_str} {start_time}"
            end_str = f"{date_str} {end_time}"

            start_dt = dateparser.parse(start_str, settings={'TIMEZONE': 'Asia/Kolkata', 'TO_TIMEZONE': 'Asia/Kolkata', 'RETURN_AS_TIMEZONE_AWARE': True})
            end_dt = dateparser.parse(end_str, settings={'TIMEZONE': 'Asia/Kolkata', 'TO_TIMEZONE': 'Asia/Kolkata', 'RETURN_AS_TIMEZONE_AWARE': True})

            if start_dt and end_dt:
                return start_dt.isoformat(), end_dt.isoformat()

    # 4. Regex time range extraction
    match = re.search(r'(\d{1,2})(?:[:.](\d{2}))?\s*(am|pm|AM|PM)?\s*(?:to|-)\s*(\d{1,2})(?:[:.](\d{2}))?\s*(am|pm|AM|PM)?', user_input)
    print("⏰ Regex match:", match)

    if match:
        hour1, min1, meridian1, hour2, min2, meridian2 = match.groups()
        min1 = min1 or "00"
        min2 = min2 or "00"

        # Handle missing meridian
        if not meridian1 and meridian2:
            meridian1 = meridian2
        if not meridian2 and meridian1:
            meridian2 = meridian1

        # Default to AM if still missing
        meridian1 = meridian1 or "am"
        meridian2 = meridian2 or "am"

        # Build datetime strings
        start_str = f"{date_str} {hour1}:{min1} {meridian1}"
        end_str = f"{date_str} {hour2}:{min2} {meridian2}"

        # Fix 12 AM confusion for end time specifically
        if hour2 == "12" and meridian2.lower() == "am":
            end_str = end_str.replace("12:00 am", "12:00 pm")

        print("🔧 Start string:", start_str)
        print("🔧 End string:", end_str)

        start_dt = dateparser.parse(start_str, settings={'TIMEZONE': 'Asia/Kolkata', 'TO_TIMEZONE': 'Asia/Kolkata', 'RETURN_AS_TIMEZONE_AWARE': True})
        end_dt = dateparser.parse(end_str, settings={'TIMEZONE': 'Asia/Kolkata', 'TO_TIMEZONE': 'Asia/Kolkata', 'RETURN_AS_TIMEZONE_AWARE': True})

        print("✅ Parsed start_dt:", start_dt)
        print("✅ Parsed end_dt:", end_dt)

        if start_dt and end_dt:
            return start_dt.isoformat(), end_dt.isoformat()

    # 5. Fallback: parse single time with +1 hour
    single_time = dateparser.parse(user_input, settings={'TIMEZONE': 'Asia/Kolkata', 'TO_TIMEZONE': 'Asia/Kolkata', 'RETURN_AS_TIMEZONE_AWARE': True})
    print("🔁 Fallback single_time:", single_time)

    if single_time:
        end_dt = single_time + timedelta(hours=1)
        return single_time.isoformat(), end_dt.isoformat()

    return None, None

# # ✅ **Test cases**
# tests = [
#     "Book a calendar slot from 8-9 am",
#     "Schedule a meeting tomorrow 3-4 pm",
#     "Book a call Sunday 11-12 am",
#     "Schedule meeting Tuesday afternoon",
#     "Book a call evening",
#     "Hey, I want to schedule a call for tomorrow afternoon.",
#     "Do you have any free time this Friday?",
#     "Book a meeting between 3-5 PM next week." 
# ]

# for t in tests:
#     start, end = extract_datetime(t)
#     print(f"🎯 [{t}] Parsed times:", start, end)
    


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
    
    
        if not start_time or not end_time:
            return "⚠️ Please let me know what time you prefer on that day so I can book it for you."

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

