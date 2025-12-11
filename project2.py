import json
import os
from datetime import datetime

FILE = "records.json"

# ------------------------------
# 1. SAVE & LOAD FUNCTIONS
# ------------------------------

def load_records():
    """Load all saved health records."""
    if not os.path.exists(FILE):
        return []
    try:
        return json.load(open(FILE))
    except:
        return []

def save_records(data):
    """Save health records to JSON file."""
    json.dump(data, open(FILE, "w"), indent=2)


# ------------------------------
# 2. HEALTH EVALUATION FUNCTION
# ------------------------------

def evaluate(record):
    """Check temperature, heart rate, SpO2 and symptoms.
       Then calculate a score and risk level."""
    
    messages = []
    score = 0

    temp = record.get("temp")
    hr = record.get("hr")
    spo2 = record.get("spo2")
    symptoms = [s.lower() for s in record.get("symptoms", [])]

    # --- Temperature ---
    if temp is None:
        messages.append("Temperature missing")
    else:
        if temp >= 39:
            messages.append(f"High fever: {temp}°C")
            score += 30
        elif temp >= 37.5:
            messages.append(f"Mild fever: {temp}°C")
            score += 15
        elif temp < 35:
            messages.append(f"Low temperature: {temp}°C")
            score += 10
        else:
            messages.append(f"Normal temp: {temp}°C")

    # --- Heart Rate ---
    if hr is None:
        messages.append("Heart rate missing")
    else:
        if hr >= 130:
            messages.append(f"Very high HR: {hr} bpm")
            score += 25
        elif hr >= 100:
            messages.append(f"High HR: {hr} bpm")
            score += 15
        elif hr < 50:
            messages.append(f"Low HR: {hr} bpm")
            score += 20
        else:
            messages.append(f"Normal HR: {hr} bpm")

    # --- Oxygen (SpO2) ---
    if spo2 is None:
        messages.append("SpO2 missing")
    else:
        if spo2 < 90:
            messages.append(f"Low oxygen: {spo2}%")
            score += 35
        elif spo2 < 95:
            messages.append(f"Mildly low oxygen: {spo2}%")
            score += 15
        else:
            messages.append(f"Normal oxygen: {spo2}%")

    # --- Symptoms ---
    red_flags = ["chest pain", "shortness of breath", "loss of consciousness"]
    serious = ["dizziness", "confusion", "severe headache"]
    mild = ["fever", "cough", "fatigue", "nausea"]

    for word in red_flags:
        if any(word in s for s in symptoms):
            messages.append(f"Red flag: {word}")
            score += 40

    for word in serious:
        if any(word in s for s in symptoms):
            messages.append(f"Serious symptom: {word}")
            score += 20

    for word in mild:
        if any(word in s for s in symptoms):
            score += 5

    # Cap score at 100
    score = min(score, 100)

    # Risk category
    if score >= 70:
        risk = "High"
    elif score >= 30:
        risk = "Medium"
    else:
        risk = "Low"

    # --- Suggestions ---
    suggestions = []
    if any(m.startswith("Red flag") for m in messages):
        suggestions.append("Seek immediate care.")
    if spo2 and spo2 < 95:
        suggestions.append("Monitor breathing.")
    if temp and temp >= 37.5:
        suggestions.append("Rest and stay hydrated.")
    if not suggestions:
        suggestions.append("No urgent issues.")

    return {
        "messages": messages,
        "risk": risk,
        "score": score,
        "suggestions": suggestions
    }


# ------------------------------
# 3. USER INPUT HELPER
# ------------------------------

def read_number(msg):
    """Reads a number or returns None if input is empty."""
    val = input(msg).strip()
    return float(val) if val else None


# ------------------------------
# 4. FEATURES (Add, List, View, Delete, Plot)
# ------------------------------

def add_record():
    """Collect user data, evaluate, and save record."""
    print("\n--- Add New Record ---")

    name = input("Name: ") or "Unknown"
    temp = read_number("Temperature °C: ")
    hr = read_number("Heart rate bpm: ")
    spo2 = read_number("SpO2 %: ")
    symptoms = input("Symptoms (comma separated): ").split(",")

    # Create record dictionary
    record = {
        "id": int(datetime.now().timestamp()),
        "time": datetime.now().isoformat(timespec="seconds"),
        "name": name,
        "temp": temp,
        "hr": hr,
        "spo2": spo2,
        "symptoms": [s.strip() for s in symptoms if s.strip()]
    }

    # Evaluate record
    record["eval"] = evaluate(record)

    # Save
    data = load_records()
    data.append(record)
    save_records(data)

    # Print summary
    print("\n--- Evaluation Result ---")
    print(f"Risk Level: {record['eval']['risk']}")
    print(f"Score: {record['eval']['score']}")
    for m in record["eval"]["messages"]:
        print("-", m)
    print("Suggestions:")
    for s in record["eval"]["suggestions"]:
        print("-", s)
    print("\nRecord saved.\n")


def list_records():
    """List saved health records briefly."""
    data = load_records()
    if not data:
        print("No records found.")
        return

    print("\n--- All Records ---")
    for r in data:
        print(f"{r['id']} | {r['time']} | {r['name']} | Risk: {r['eval']['risk']}")


def view_record():
    """Show full details of a record by ID."""
    rid = input("Enter ID: ")
    try:
        rid = int(rid)
    except:
        print("Invalid ID number.")
        return

    data = load_records()
    record = next((x for x in data if x["id"] == rid), None)

    if not record:
        print("Record not found.")
        return

    print("\n--- Full Record ---")
    print(json.dumps(record, indent=2))


def delete_record():
    """Delete a record using its ID."""
    rid = input("Enter ID to delete: ")
    try:
        rid = int(rid)
    except:
        print("Invalid ID.")
        return

    data = load_records()
    updated = [r for r in data if r["id"] != rid]

    if len(updated) == len(data):
        print("Record not found.")
    else:
        save_records(updated)
        print("Record deleted successfully.")


def plot_history():
    """Plot history of temperature, heart rate, and SpO2."""
    try:
        import matplotlib.pyplot as plt
    except:
        print("Install matplotlib to use plotting.")
        return

    data = load_records()
    if not data:
        print("No data to plot.")
        return

    times = [datetime.fromisoformat(r["time"]) for r in data]

    def do_plot(values, title):
        if all(v is None for v in values):
            return
        plt.figure()
        plt.plot(times, values)
        plt.title(title)
        plt.show()

    do_plot([r["temp"] for r in data], "Temperature")
    do_plot([r["hr"] for r in data], "Heart Rate")
    do_plot([r["spo2"] for r in data], "SpO2")


# ------------------------------
# 5. MAIN MENU LOOP
# ------------------------------

def main():
    while True:
        print("""
Smart Health Monitoring
1. Add new record
2. List all records
3. View a record
4. Plot history
5. Delete a record
0. Exit
""")
        choice = input("Choose an option: ")

        if choice == "1":
            add_record()
        elif choice == "2":
            list_records()
        elif choice == "3":
            view_record()
        elif choice == "4":
            plot_history()
        elif choice == "5":
            delete_record()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")


# Start program
if __name__ == "__main__":
    main()
