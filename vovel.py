def cv(a):
    c={"A","E","I","O","U","a","e","i","o","u"}

    if a in c:
      print("The word is vowel")
    else:
      print("The word is not vowel")
a=input("Enter a letter to find is it vowel or not")
cv(a)       