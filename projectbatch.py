

import json
import datetime
import os

from sklearn.linear_model import LinearRegression
import statistics as np

DATA_FILE = "habits.json"

# -----------------------------
# Load or create habit storage
# -----------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# -----------------------------
# Add a new habit
# -----------------------------
def add_habit():
    habit = input("Enter the habit name: ")
    data = load_data()
    
    if habit in data:
        print("Habit already exists!")
        return
    
    data[habit] = []
    save_data(data)
    print("Habit added successfully!")

# -----------------------------
# Mark today's habit status
# -----------------------------
def mark_habit():
    habit = input("Enter habit name: ")
    data = load_data()

    if habit not in data:
        print("Habit not found!")
        return
    
    status = input("Did you complete the habit today? (yes/no): ").strip().lower()
    today = str(datetime.date.today())
    
    data[habit].append({"date": today, "status": 1 if status == "yes" else 0})
    save_data(data)
    print("Habit updated successfully!")

# -----------------------------
# Show habit history
# -----------------------------
def show_history():
    habit = input("Enter habit name: ")
    data = load_data()

    if habit not in data:
        print("Habit not found!")
        return

    records = data[habit]
    print("\n--- Habit History ---")
    for r in records:
        print(f"{r['date']} : {'Completed' if r['status']==1 else 'Missed'}")
    print("---------------------")

# -----------------------------
# Predict future performance
# -----------------------------
def predict_habit():
    habit = input("Enter habit name: ")
    data = load_data()

    if habit not in data:
        print("Habit not found!")
        return
    
    records = data[habit]
    
    if len(records) < 3:
        print("Not enough data to predict. Track for at least 3 days.")
        return

    X = np.array([[i] for i in range(len(records))])
    y = np.array([r['status'] for r in records])

    model = LinearRegression()
    model.fit(X, y)

    tomorrow_index = len(records)
    prediction = model.predict([[tomorrow_index]])[0]

    probability = max(0, min(1, prediction)) * 100
    print(f"\nPredicted chance of completing '{habit}' tomorrow: {probability:.2f}%")

    if probability > 70:
        print("Great! You're consistent. Keep it up! 💪")
    elif probability > 40:
        print("You can still improve. Stay focused! 🙂")
    else:
        print("Try harder! You can do better! 🔥")

# -----------------------------
# Menu system
# -----------------------------
def menu():
    while True:
        print("\n===== Intelligent Habit Tracker =====")
        print("1. Add Habit")
        print("2. Mark Today's Habit")
        print("3. Show Habit History")
        print("4. Predict Future Performance")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_habit()
        elif choice == "2":
            mark_habit()
        elif choice == "3":
            show_history()
        elif choice == "4":
            predict_habit()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Try again.")

# -----------------------------
# Run the program
# -----------------------------
menu()