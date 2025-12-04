# Creating a dictionary
students = {
    "Amit": 85,
    "Riya": 92,
    "Suresh": 78,
    "Priya": 88
}

# Display the dictionary
print("Students and their marks:")
for name, marks in students.items():
    print(name, ":", marks)

# Search a student's marks
search = input("Enter student name to see marks: ")

if search in students:
    print(search, "scored", students[search])
else:
    print("Student not found")
