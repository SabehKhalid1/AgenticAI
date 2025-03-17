import json
import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

def save_event(event_name, event_time):
    """ Saves an event in a JSON file instead of using Google Calendar API """
    try:
        with open("events.json", "r") as f:
            events = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        events = []

    event = {"name": event_name, "time": event_time}
    events.append(event)

    with open("events.json", "w") as f:
        json.dump(events, f, indent=4)

    return f"Event '{event_name}' saved for {event_time}!"

@app.route("/ask", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if "schedule" in user_input.lower():
        event_name = "Project Deadline"
        event_time = (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat()
        return jsonify({"response": save_event(event_name, event_time)})
    else:
        return jsonify({"response": "Sorry, I can only schedule events for now."})

if __name__ == "__main__":
    app.run(debug=True)

