#1
students_info=("nisarg","18","python+genAI","2025")
# students_info=("nisarg","18","python+genAI","2025")
# students_info=("nisarg","18","python+genAI","2025")
print("name:",students_info[0])
print("age:",students_info[1])
print("enrole coursed:",students_info[2])
print("year:",students_info[3])
z=list(students_info)
print(z)
z.append([1,2,3])
print(z)
#2
# students_info=("nisarg","18","python+ai")
# students_info[2]=("sanju")
# print(students_info)
#3
tupple=("python",30,"bigginer")
print(tupple)
print("name:",tupple[0])
print("duration:",tupple[1])
print("level:",tupple[2])
#4
var=[20,30,34,500]
var.append(39)
print(var)
b=tuple(var)
print(b)
#5
student=("pavan",("python","GENAI"))
v=student[1][1]
print(v)
#6
a=24
b=34
a,b=b,a
print(a,b)
#7
topics=("python","sql","python","python")
z=topics.count("python")
print(z)