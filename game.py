""" 用python设计第一个游戏 """
temp = input("不妨猜一下小平平现在心里想的是哪个数字？")
guess = int(temp)

if guess == 8:
    print("你是小平平肚子里的蛔虫吗")
    print("猜中也没奖励！")
else:
    print("猜错啦，小平平现在心里想的是8！")

print("游戏结束，不玩啦^_^")
