import string

password = input("Enter a password to check: ")

upper_case = any([1 if c in string.ascii_uppercase else 0 for c in password])
lower_case = any([1 if c in string.ascii_lowercase else 0 for c in password])
special_case = any([1 if c in string.punctuation else 0 for c in password])
digits = any([1 if c in string.digits else 0 for c in password])

print("uppercase >>>",upper_case)
print("lowercase >>>",lower_case)
print("special characters >>>",special_case)
print("digits >>>",digits)

characters = [upper_case, lower_case, special_case, digits]

print("len carachters >>>",len(characters))

length = len(password)

score = 0




with open("common.txt", "r") as f:
    common = f.read().splitlines()

if password in common:
    print("Password found in common words list. Score: 0/7")
    exit()    



if length >= 8:
    score += 1
if length >= 12:
    score += 1
if length >= 16:
    score += 1
if length >= 20:
    score += 1

    

print(f"password length is {str(length)},adding {str(score)} points")


if sum(characters) > 1:
    score += 1
if sum(characters) > 2:
    score += 1
if sum(characters) > 3:
    score += 1
if sum(characters) > 4:
    score += 1        

print(f"password has {str(sum(characters))} different character types,adding {sum(characters) - 1} points")   


if score < 4:
    print(f"Password is weak. Score: {score}/7")
elif score == 4:
    print(f"Password is moderate. Score: {score}/7")
elif score > 4 and score < 7 :
    print(f"Password is strong. Score: {score}/7")