import csv
import os
from datetime import datetime

EVENT_FILE = "events.csv"


def load_events():
    if not os.path.exists(EVENT_FILE):
        return []

    with open(EVENT_FILE, "r") as f:
        return list(csv.DictReader(f))


def current_status(events):
    if not events:
        return "I don't have any camera events yet."

    last_event = events[-1]

    if last_event["event"] == "PERSON ENTERED":
        entered = datetime.strptime(
            last_event["timestamp"],
            "%Y-%m-%d %H:%M:%S"
        )

        duration = datetime.now() - entered
        minutes = int(duration.total_seconds() / 60)

        return (
            f"Yes. A person is currently in the room. "
            f"They entered at {entered.strftime('%I:%M %p')} "
            f"and have been present for about {minutes} minutes."
        )

    return "The room is currently empty."


def last_entry(events):
    entries = [
        event for event in events
        if event["event"] == "PERSON ENTERED"
    ]

    if not entries:
        return "I haven't detected anyone entering yet."

    last = entries[-1]

    timestamp = datetime.strptime(
        last["timestamp"],
        "%Y-%m-%d %H:%M:%S"
    )

    return (
        f"The last person entered at "
        f"{timestamp.strftime('%I:%M %p')}."
    )


def today_summary(events):
    today = datetime.now().strftime("%Y-%m-%d")

    today_events = [
        event for event in events
        if event["timestamp"].startswith(today)
    ]

    entries = [
        event for event in today_events
        if event["event"] == "PERSON ENTERED"
    ]

    exits = [
        event for event in today_events
        if event["event"] == "PERSON LEFT"
    ]

    total_seconds = 0

    for event in exits:
        if event["duration_seconds"]:
            total_seconds += int(event["duration_seconds"])

    minutes = total_seconds // 60

    return (
        f"Today I detected {len(entries)} room entries. "
        f"Recorded occupied time is approximately {minutes} minutes."
    )


print("\nTAPO AI CHATBOT")
print("----------------")
print("Ask me about your camera.")
print("Type 'quit' to exit.\n")


while True:
    question = input("You: ").lower().strip()

    if question == "quit":
        print("Tapo AI: Goodbye!")
        break

    # Reload events every time so chatbot sees latest camera activity
    events = load_events()

    # Check specific historical questions first
    if (
        "last" in question
        or "last enter" in question
        or "last entered" in question
    ):
        answer = last_entry(events)

    elif (
        "today" in question
        or "summary" in question
    ):
        answer = today_summary(events)

    elif (
        "anyone" in question
        or "someone" in question
        or "room" in question
        or "happening" in question
    ):
        answer = current_status(events)

    else:
        answer = (
            "I don't understand that question yet. "
            "Try asking if anyone is in the room, "
            "when someone last entered, "
            "or what happened today."
        )

    print(f"Tapo AI: {answer}\n")
