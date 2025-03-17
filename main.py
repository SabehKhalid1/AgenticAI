import json
import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

def load_events():
    """ Load events from JSON file """
    try:
        with open("events.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_events(events):
    """ Save events to JSON file """
    with open("events.json", "w") as f:
        json.dump(events, f, indent=4)

def add_event(event_name, event_time):
    """ Add a new event """
    events = load_events()
    event = {"name": event_name, "time": event_time}
    events.append(event)
    save_events(events)
    return f"Event '{event_name}' scheduled for {event_time}!"

def list_events():
    """ Retrieve all events """
    events = load_events()
    return events if events else "No events scheduled."

def modify_event(old_name, new_name, new_time):
    """ Modify an existing event """
    events = load_events()
    for event in events:
        if event["name"].lower() == old_name.lower():
            event["name"] = new_name
            event["time"] = new_time
            save_events(events)
            return f"Updated event: '{new_name}' on {new_time}."
    return "Event not found."

def delete_event(event_name):
    """ Delete an event """
    events = load_events()
    updated_events = [event for event in events if event["name"].lower() != event_name.lower()]
    if len(updated_events) == len(events):
        return "Event not found."
    save_events(updated_events)
    return f"Deleted event '{event_name}'."

@app.route("/ask", methods=["POST"])
def chat():
    user_input = request.json.get("message").lower()

    if "schedule" in user_input:
        event_name = "Project Deadline"
        event_time = (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat()
        return jsonify({"response": add_event(event_name, event_time)})

    elif "list" in user_input:
        return jsonify({"response": list_events()})

    elif "modify" in user_input:
        return jsonify({"response": modify_event("Project Deadline", "Updated Project", (datetime.datetime.now() + datetime.timedelta(days=2)).isoformat())})

    elif "delete" in user_input:
        return jsonify({"response": delete_event("Project Deadline")})

    else:
        return jsonify({"response": "Sorry, I don't understand. Please use 'schedule', 'list', 'modify', or 'delete'."})

if __name__ == "__main__":
    app.run(debug=True)

