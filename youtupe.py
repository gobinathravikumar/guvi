''' print("hi gobi")
name="gobi"
print(name)--single line comment
print("hi "+name)'''
'''gobinkjdytfkjbjf-----multi line comment
cf6hkhfiyt'''
# string methods fllow the link--https://www.programiz.com/python-programming/methods/string/maketrans
'''count=21.8
print(int(float(count)+1))
otp=434511
otp=str(otp)
print("your otp is \t" +otp)
name, days, year='gobi', str(15), str(2021)
print('dear '+name+',\n'+'you have '+days+' leave balance for this \nyear('+year+').' )
input from user
name=input('what is you name : ')
email=input('please insert your mail :')
phone=input(str(('give your contact :')))
print('name :'+name+'\nmail id :'+email+'\ncontact :'+phone)'''
# import math--------mathematical need to flow link--https://docs.python.org/3/library/math.html
'''num=int(input())
print(math.log2(num))
print(math.cos(num))
print(6**num)
print(math.pow(2,num))'''
# if else and elif ladder
'''user=input('enter your user name :')
passw=int(input('please enter password :'))
log=len(str(passw))
if log >=10:
    print (user +'   logeed')
elif log >=8:
    print(user + '   logeed')
else:
    print('incorrect password')'''

#codecata learning
'''line1=input().split(' ')
print(line1)
gobi='gobinath'
print('\n'.join(gobi))
print(','.join(gobi))
print(' '.join(gobi))'''
# a=int(input())
# for a in a*2:
#     print(a)
# WHILE LOOP
# letter = ' '
# while not letter.isalpha():
#     letter = input("enter a alphapet : ")
# print("your letter is : "+letter)
# print 1 to 100
# num= 1
# while  num <= 100:
#     print(num)
#     num += 1  # num = num + 1
# for i in range (1,100):#in for loop range argument can't take 2 argument value in function
#     print(i)
# for i in range (1,101):
#     print(i)
# for i in range(100,0,-2):
#     print(i)
# else:
#     print('over')
# list=[1,2,3,4,5,6]
# for i in list:
#     print(i)
#     print(i*i)
# import random
# num=random.randint(1,20)
#
# attempt='0'
# while attempt >= 4:
#     guess = int(input("guess what number is in num max is 20 : "))
#     attempt = attempt + i
#     print('you loose')
#     if guess > num:
#         print('your guess is high')
#     else:
#         print('your guess is low')
#     guess=int(input('guess again : '))
#
#
#
# print('you won')
# for i in range(1,7):
#     for j in range(1,6):
#         print(i,end=' ')
#     print(' ')
#
# for i in range(1,7):---control the number of rows
#     for j in range(1,6):----control the number of columns
#         print(j,end=' ')
#     print(' ')

# for i in range(1,6):
#     for j in range(1,i+1):
#         print('*',end=' ')
#     print(' ')

# a = 8
# for i in range(0, 5):
#     for j in range(0, a):
#         print(end=" ")
#     a = a - 2
#     for j in range(0, i+1):
#         print("* ", end="")
#     print()
# triangle patten makking
# for i in range(5):
#     for j in range((5 - i) - 1):
#         print(end=" ")
#     for j in range(i + 1):
#         print("*", end=" ")
#     print()
# a='1'
# b='0'
# for i in a:
#     for j in range(1,5):
#         print(i,end=' ')
#     print(' ')
#     for i in b:
#         for j in range(1,5):
#             print(i,end=' ')
#     print(' ')
# use break
# list_num=[]
# while True:
#     inp=input()
#     if inp=='z':
#         break
#     list_num.append(int(inp))
# print(list_num)
# use continus
# str="a,s,d,f,g"
# str2=' '
# for i in str:
#     if str == ',':
#         continue
#     str2=str+i
#
# print(str2)
# # use pass
# str="a,s,d,f,g"
# str2=' '
# for i in str:
#     if str == ',':
#         pass
#     else:
#         str2=str+i
#
# print(str2)
# assingment
# num='1,2,3,4,5'
# num2=''
# for i in num:
#     if i==',':
#         continue
#     num2=num2+i
#
# print(num2)
# split & join
# str_in='abc bvc nbv nmn'
# str_list=str_in.split(' ')
# print(str_list)
#
# str_join='-'.join(str_list)
# print(str_join)
# nested list
# tn=['erode','chennai','madurai','salem']
# kl=['kochi','munnar''udupy','thiru']
# ka=['bangalor','whitefiled','mysore']
# india=[tn,kl,ka]
# print(india[0][2])
# tup=(9,8,10)
# print(tup)
# disnory
dis={'name':'gobi','age':27,'gender':'male'}
