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

#将评价人数转换为数值类型是否为‘object’（处理可能的字符串）
#pandas中object类型通常表示字符串或混合类型
if df['评价人数'].dtype == 'object':
    #对评价人数列进行字符串清洗 1.astype(str) 确保所有值为字符串类型；.str.replace('人评价','')移除文本中人评价字样（100人评价==100）；3.str.srtip（）去除首尾空白字符 
    df['评价人数'] = df['评价人数'].astype(str).str.replace('人评价','').str.strip()
#将清洗后的‘评价人数’转换为数值类型（整数或浮点数）pd.to_numeric()：将参数转换为数值；errors=coerce 转换失败时设为none空值，而不是抛出异常
df['评价人数'] = pd.to_numeric(df['评价人数'],errors='coerce')
#打印转换后的各列数据类型，确认转换成功
print("\n转换后的数据类型：")
#df.dtypes返回一个series，显示每列的数据类型
print(df.dtypes)

#检查清洗结果 数据质量检查 评估数据完整性
print(f"\n数据质量检查：")
#df.isnull().sum().sum() df.isnull返回布尔dataframe（true表示空值）.sum（）按列统计控制数量（第一次）.sum（）再对所有列求和（第二次）得到总空值数
print(f" -缺失值数量:{df.isnull().sum().sum()}")
#df.duplicated().sum()  df.duplicated()返回布尔series true表示重复行  .sum（）统计true的数量，即重复行总数
print(f" -重复值数量:{df.duplicated().sum()}")

#5 数据筛选（验收标准核心）
print("\n数据筛选(验收标准)")

#筛选一：高评分电影(>=9.0)
#df[df['评分'] >=9.0]布尔索引，选择评分列>=9.0的行
high_rating_movies = df[df['评分'] >=9.0]
print(f"一. 评分9.0及以上的电影：{len(high_rating_movies)}部:")
#显示筛选结果的前几行，只选取电影名称和评分两列
print(high_rating_movies[['电影名称','评分']].head())

#筛选二:热门电影（评价人数超100万）
#先检查评价人数列是否存在，避免keyerror
if '评价人数' in df.columns:
    #df[df['评价人数'] > 1000000] 布尔索引，选择>1000000的行
    popular_movies = df[df['评价人数'] > 1000000]
    print(f"\n二. 评价人数过百万的电影有{len(popular_movies)}部:")
    #显示前几行，只选取电影名称和评价人数两列
    print(popular_movies[['电影名称','评价人数']].head())

#筛选三：多重条件筛选（优质电影 评分大于等于8.5且评价人数大于50万）
#使用括号分组条件，&表示逻辑与（and）
if '评价人数' in df.columns:
    #df[(df['评分'] >= 8.5) & (df['评价人数'] > 500000)]：复合条件
    top_quality_movies = df[(df['评分'] >= 8.5) & (df['评价人数'] > 500000)]
    print(f"\n三. 评分超8.5评价人数超五十万的电影有{len(top_quality_movies)}部：")
    #显示前十行，选择三列信息
    print(top_quality_movies[['电影名称','评分','评价人数']].head(10))

#6 JSON数据处理(JSON库解析)将dataframe转换为json格式
print("\n JSON数据处理:")
#将筛选结果转换为JSON格式 取前五条记录 df.head（5）表示取dataframe的前五行 只选择 电影名称和评分这两列
sample_data = df.head(5)[['电影名称','评分']]
#将dataframe转换为json字符串 sample_data.to_json：dataframe转json的方法；orient=records ：json格式为记录数组，[{"col1":val1,"col2":val2,...}]；force_ascii=false：允许非ascii字符如中文原样输出；indent=2：缩进2空格，美化输出格式
json_data = sample_data.to_json(orient = 'records',force_ascii = False,indent = 2) 
print("将前五条记录转换为JSON格式:")
print(json_data) #打印json字符串
print("\n解析JSON数据:")#打印提示操作
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