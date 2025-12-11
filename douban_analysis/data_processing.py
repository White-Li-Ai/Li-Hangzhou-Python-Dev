#对之前爬取的豆瓣t250做数据处理

import pandas as pd #导入pandas库，这是python数据分析和处理的核心库，通常简写为pd
import json #导入json模块，用于json数据的编码和解码

print("===豆瓣t250数据处理开始===") #打印程序开始标志
print("使用的数据文件为：douban_top250.csv")#显示正在使用的数据文件名称
print("=" * 60)#美化输出界面

#1 用pandas读取CSV文件
print("步骤一：读取CSV数据...")
#使用try-except结构处理文件读取可能出现的异常
try:
    #使用pandas的read_csv函数读取csv文件
    #默认参数：逗号分隔，第一行为列名utf-8编码
    df = pd.read_csv('douban_top250.csv')
    #成功读取后显示数据形状 df.shape返回（行数，列数）的元组
    print(f"成功读取该文件！数据形状：{df.shape}")
    #显示数据列名df.colums是列名索引，转换为列表显示
    print(f"列名：{list(df.columns)}")
#捕获文件不存在的异常
except FileNotFoundError: #
    print("错误：找不到douban_top250.csv文件")
    print("请确保文件在正确目录下")
    exit() #文件不存在，程序退出
#捕获其他异常
except Exception as e:
    print(f"读取文件时出错：{e}")#打印错误信息
    exit()#发生错误 程序退出

#2 数据预览（数据查看）
print("\n步骤2：数据预览")
print("前3行数据为：")#显示前三行
#df.head（3）返回dataframe的前三行，默认显示所有列
print(df.head(3))

#3 数据信息检查
print("\n数据基本信息")
#df.info()显示dataframe的详细信息 每列的非空值数量、每列的数据类型、内存使用量
print(df.info())

#4 数据清洗与转换（数据处理核心步骤）
print("\n 数据清洗与转换...")

#检查并转换数据类型 先查看原始数据类型
print("转换前的数据类型：")
#df.dtypes返回每列的数据类型（series对象）
print(df.dtypes)

#将评分转换为数值类型 原csv中可能是字符串、pd.to_numeric()将参数转换为数值类型
#errors=coerce表示转换失败时设为none空值，而不是抛出异常
df['评分'] = pd.to_numeric(df['评分'],errors='coerce')

#将评价人数转换为数值类型（处理可能的字符串）
if df['评价人数'].dtype == 'object':
    df['评价人数'] = df['评价人数'].astype(str).str.replace('人评价','').str.strip()
df['评价人数'] = pd.to_numeric(df['评价人数'],errors='coerce')

print("\n转换后的数据类型：")
print(df.dtypes)

#检查清洗结果
print(f"\n数据质量检查：")
print(f" -缺失值数量:{df.isnull().sum().sum()}")
print(f" -重复值数量:{df.duplicated().sum()}")

#5 数据筛选（验收标准核心）
print("\n数据筛选(验收标准)")

#筛选一：高评分电影(>=9.0)
high_rating_movies = df[df['评分'] >=9.0]
print(f"一. 评分9.0及以上的电影：{len(high_rating_movies)}部:")
print(high_rating_movies[['电影名称','评分']].head())

#筛选二:热门电影（评价人数超100万）
if '评价人数' in df.columns:
    popular_movies = df[df['评价人数'] > 1000000]
    print(f"\n二. 评价人数过百万的电影有{len(popular_movies)}部:")
    print(popular_movies[['电影名称','评价人数']].head())

#筛选三：多重条件筛选
if '评价人数' in df.columns:
    top_quality_movies = df[(df['评分'] >= 8.5) & (df['评价人数'] > 500000)]
    print(f"\n三. 评分超8.5评价人数超五十万的电影有{len(top_quality_movies)}部：")
    print(top_quality_movies[['电影名称','评分','评价人数']].head(10))

#6 JSON数据处理(JSON库解析)
print("\n JSON数据处理:")
#将筛选结果转换为JSON
#取前五条作为示例
sample_data = df.head(5)[['电影名称','评分']]
json_data = sample_data.to_json(orient = 'records',force_ascii = False,indent = 2) 
print("将前五条记录转换为JSON格式:")
print(json_data)
print("\n解析JSON数据:")
try:
    parsed_data = json.loads(json_data)
    print(f"解析后获得{len(parsed_data)}条记录")
    for i,item in enumerate(parsed_data,1):
        print(f"记录{i}:{item}")
except Exception as e:
    print(f"解析JSON出错:{e}")

#7.保存处理过的数据
print("\n保存处理后的数据")
#创建清洗后的副本（添加清洗标志）
df_processed = df.copy()
df_processed['数据类别'] = '原始数据（电影）================（筛选淘汰）================'
#标记高评分电影、热门电影、优质电影
df_processed.loc[high_rating_movies.index,'数据类别'] = '高评分电影'
df_processed.loc[popular_movies.index,'数据类别'] = '热门电影'
df_processed.loc[top_quality_movies.index,'数据类别'] = '优质电影'

# #进行数据类型转换
df_processed['评分'] = pd.to_numeric(df_processed['评分'],errors='coerce')
df_processed['评价人数'] = pd.to_numeric(df_processed['评价人数'],errors='coerce')
# #添加清洗相关的列体现差异
df_processed['数据状态'] = '已清洗'
df_processed['评分类别'] = pd.cut(df_processed['评分'],
                              bins = [0,7,8,9,10],
                              labels=['一般','良好','优秀','极好'])
try:
    df_processed.to_csv('douban_top250_processed.csv',index=False,encoding = 'utf-8-sig')
    print("处理后的数据已保存至：douban_top250_processed.csv")
except Exception as e:
    print(f"文件保存时出错:{e}")
print("\n" + "=" * 60)
print("数据处理任务已完成！")
print("验收标准达成：")
print("已用pandas读写CSV文件")
print("已进行数据清洗和类型转换") 
print("已使用pandas进行数据筛选")
print("已用json库解析数据")
print("已将在豆瓣爬取的数据用pandas进行筛选")