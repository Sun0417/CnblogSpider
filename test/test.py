import re
import socket
import mysql.connector

mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    passwd='123456',
    database='test'
)
mycur = mydb.cursor()

sql = '''select * 
from tb_user '''

mycur.execute(sql)

re = mycur.fetchall()
print(type(re))
for x in re:
    print(x)


# line = "xxxxxx出生2001年12"
# # 贪婪模式 是从右边开始匹配 （）代用是字串
# reg_str = ".*出生(\d{4}[年/-]\d{1,2}([月/-]\d{1,2}|[月/-]$|$))"
# match_obj = re.match(reg_str, line)
# if match_obj:
#     print(match_obj.group(1))
#
# str = 'Python'
# for letter in 'python':
#     print(letter)
#
# fruits = ['banana', 'apple',  'mango']
# # for fruit in fruits:
# #     print(fruit)
#
# for num in range(10, 20):
#     for i in range(2, num):
#         if num%i == 0:
#             j = num/i
#             print('%d 等于 %d * %d' % (num,i,j))
#             break
#     else:
#       print("是一个质数", num)
#
# #*age 不定长参数默认传递的是元组
# def printinfo(name, *age):
#     "打印任何传入的字符串"
#     print("Name: ", name)
#     for i in age:
#         print(i)
#     print("Age ", age)
#     return
#
# printinfo("ddd",50, 1,60,70)


# def Foo(x):
#     if (x==1):
#         return 1
#     else:
#        print(x)
#        return x + Foo(x - 1)  #4  3  2 1
#
# print(Foo(4))
#
# list = []
# dic = {"K":"DDD","H":"EEEE"}
# list.append(dic)
# dic['K'] = 'NNN'
# for x in list:
#     print(x['K'])

k = set({'1','2','1','2'})
k.add(1)
print(k)

# numbers = [1, 3, 6]
# newNumbers = tuple(map(lambda x: x+1 , numbers))
# print(newNumbers)

# result = lambda x: x * x
# print(result(5))

# i = sum = 0
#
# while i <= 4:
#     sum += i  #0 1 3 6 10
#     print("sun" , sum)
#     i = i+1 #1 2 3 4 5
#     print("sun1", i)
#
# print(sum)
# s = socket.socket() #创建sokect对象
# host = 'localhost' #获取主机名称
# port = 6999 #设置端头
# s.bind((host, port)) #绑定端口
#
# s.listen(5) #等待5秒
# while True:
#     c,addr = s.accept() #建立连接
#     print('链接地址', addr)
#     data = s.recv(1024)  # 接收数据
#     print('recive:', data.decode())  # 打印接收到的数据
#     c.send(data.upper())  #发送
#     c.close() #关闭



