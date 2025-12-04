the_python="ptyhonrocks"
print(the_python)
print(the_python[6:])
print(the_python[-5::])
print(the_python[-5:-10:])
print(the_python[1:5:-1])
print(the_python[-5:])
print(the_python[0:-5])
print(the_python[1:-5:1])
print(the_python[::2])
print("reverse",the_python[::-1])
phone="9764148795"
var=phone[6:]
print('*'*6+var)
#movie
movie="Dil wale dulhaniya le jayege"
movie1=movie.split("  ")
print(movie1)


#reverse
sentence="python is powerful"
print(sentence[::-1])

word="malayalam"
print(word[::-1])


#split
var="nisargrajurkar@gmail.com"
print(var.split("@"))



#alternate
x="Datascience"
print(x[0::2])


#date
date=input("Enetr your date of birth (DD-MM-YYYY)")
print("today is date is ",date[0:2],"of month",date[3:5],"of the year",date[6:] )