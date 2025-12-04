def prime(a):
    if(a<=1):
        return print('the number is not prime')
    for i in range(2,a):
        if a%i==0:
             print("the number is not prime")
             return
        else:
             print("The number is prme")
a=int(input("enter a number to find is it prime or not :"))
prime(a)        