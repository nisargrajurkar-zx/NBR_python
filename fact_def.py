def fact(a):
    fact=1
    for i in range(1,a+1):
        fact=fact*i
    print("the factorial of the number is :",fact)
a=int(input("Enter a number to find the factorial of the number:"))
fact(a)        