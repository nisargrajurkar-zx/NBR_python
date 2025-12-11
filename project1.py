import json, os
from datetime import datetime

FILE = "records.json"

def load():
    if not os.path.exists(FILE): return []
    try: return json.load(open(FILE))
    except: return []

def save(data):
    json.dump(data, open(FILE, "w"), indent=2)

# ----- Evaluation (SHORT VERSION) -----
def evaluate(r):
    msg, score = [], 0

    t = r.get("temp"); h = r.get("hr"); s = r.get("spo2")
    sym = [x.lower() for x in r.get("symptoms", [])]

    # Temperature
    if t is None: msg.append("Temperature missing")
    else:
        if t >= 39: msg.append(f"High fever: {t}°C"); score += 30
        elif t >= 37.5: msg.append(f"Mild fever: {t}°C"); score += 15
        elif t < 35: msg.append(f"Low temperature: {t}°C"); score += 10
        else: msg.append(f"Normal temp: {t}°C")

    # Heart Rate
    if h is None: msg.append("Heart rate missing")
    else:
        if h >= 130: msg.append(f"Very high HR: {h} bpm"); score += 25
        elif h >= 100: msg.append(f"High HR: {h} bpm"); score += 15
        elif h < 50: msg.append(f"Low HR: {h} bpm"); score += 20
        else: msg.append(f"Normal HR: {h} bpm")

    # SpO2
    if s is None: msg.append("SpO2 missing")
    else:
        if s < 90: msg.append(f"Low oxygen: {s}%"); score += 35
        elif s < 95: msg.append(f"Mildly low oxygen: {s}%"); score += 15
        else: msg.append(f"Normal oxygen: {s}%")

    # Symptoms
    red = ["chest pain", "shortness of breath", "loss of consciousness"]
    serious = ["dizziness", "confusion", "severe headache"]
    mild = ["fever", "cough", "fatigue", "nausea"]

    for w in red:
        if any(w in x for x in sym): msg.append(f"Red flag: {w}"); score += 40
    for w in serious:
        if any(w in x for x in sym): msg.append(f"Serious symptom: {w}"); score += 20
    for w in mild:
        if any(w in x for x in sym): score += 5

    score = min(score, 100)
    risk = "High" if score >= 70 else "Medium" if score >= 30 else "Low"

    sug = []
    if any(x.startswith("Red flag") for x in msg): sug.append("Seek immediate care.")
    if s and s < 95: sug.append("Monitor breathing.")
    if t and t >= 37.5: sug.append("Rest and stay hydrated.")
    if not sug: sug.append("No urgent issues.")

    return {"messages": msg, "risk": risk, "score": score, "suggestions": sug}

# ----- Input helper -----
def fnum(txt):
    v = input(txt).strip()
    return float(v) if v else None

# ----- Features -----
def add_record():
    name = input("Name: ") or "Unknown"
    temp = fnum("Temperature °C: ")
    hr = fnum("Heart rate bpm: ")
    spo2 = fnum("SpO2 %: ")
    sym = input("Symptoms (comma separated): ").split(",")

    rec = {
        "id": int(datetime.now().timestamp()),
        "time": datetime.now().isoformat(timespec="seconds"),
        "name": name,
        "temp": temp,
        "hr": hr,
        "spo2": spo2,
        "symptoms": [x.strip() for x in sym if x.strip()]
    }

    rec["eval"] = evaluate(rec)
    data = load(); data.append(rec); save(data)

    print("\n--- Evaluation ---")
    print(f"Risk: {rec['eval']['risk']} | Score: {rec['eval']['score']}")
    for m in rec["eval"]["messages"]: print("-", m)
    print("Suggestions:")
    for s in rec["eval"]["suggestions"]: print("-", s)
    print("\nRecord saved.\n")

def list_records():
    data = load()
    if not data: print("No records."); return
    for r in data:
        print(f"{r['id']} | {r['time']} | {r['name']} | Risk: {r['eval']['risk']}")

def view_record():
    rid = input("ID: ")
    try: rid = int(rid)
    except: return print("Invalid ID")
    data = load()
    rec = next((x for x in data if x["id"] == rid), None)
    if not rec: print("Not found"); return
    print(json.dumps(rec, indent=2))

def plot_history():
    try: import matplotlib.pyplot as plt
    except: return print("Install matplotlib first")

    data = load()
    if not data: return print("No data")

    t = [datetime.fromisoformat(r["time"]) for r in data]
    def plot(y, lbl):
        if all(v is None for v in y): return
        plt.figure(); plt.plot(t, y); plt.title(lbl); plt.show()

    plot([r["temp"] for r in data], "Temperature")
    plot([r["hr"] for r in data], "Heart Rate")
    plot([r["spo2"] for r in data], "SpO2")

def delete_record():
    rid = input("Delete ID: ")
    try: rid = int(rid)
    except: return print("Invalid")
    data = load()
    new = [r for r in data if r["id"] != rid]
    if len(new) == len(data): print("Not found")
    else: save(new); print("Deleted")

# ----- Menu -----
def main():
    menu = """
Smart Health Monitoring (Short Version)
1. Add new record
2. List records
3. View record
4. Plot vitals history
5. Delete a record
0. Exit
"""
    while True:
        print(menu)
        c = input("Choice: ")
        if c == "1": add_record()
        elif c == "2": list_records()
        elif c == "3": view_record()
        elif c == "4": plot_history()
        elif c == "5": delete_record()
        elif c == "0": break
        else: print("Invalid")

if __name__ == "__main__":
    main()