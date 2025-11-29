#task 1
grocery_list=["milk" ,"bread ","chocolate"]
grocery_list.append("sugar")
print(grocery_list)
grocery_list.remove("milk")
print(grocery_list)
# grocery_list.remove("milk")
# print(grocery_list)
grocery_list.sort()
print(grocery_list)
grocery_list.sort(reverse=True)
print(grocery_list)
#task 2
temperature=[27,30,31,32,33,28,29]
print(max(temperature))
print(min(temperature))
view=sum(temperature)/len(temperature)
print(view)
#task3"
students=["batman","spiderman","saktiman","superman","spiderman"]
print(students.count("spiderman"))
print(students.index('spiderman'))
students.insert(2,"caption america")
print(students)
x=students.pop()
print("the popped list is",students)
print("the poppped students",x)
#4
tasks=["bike repair","ac repair"," ,laundary","mobile purchase"]
completed_task=tasks.pop()
print(type(completed_task))
print(list(completed_task))
tasks.clear()
print(tasks)