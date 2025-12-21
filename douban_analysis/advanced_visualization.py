#对之前爬取的豆瓣top250数据进行进一步的处理（Top10电影图、散点图、数据洞察分析）
#导入必要的库
import pandas as pd #数据处理库
from pyecharts.charts import Bar,Scatter,Page  #导入三种图表类型：柱状图、散点图、组合页面
from pyecharts import options as opts  #导入图表配置选项

print("===进一步数据可视化开始===")
#加载数据:读取之前处理并保存的数据文件
df = pd.read_csv('douban_top250_processed.csv')
#确保数值列的数据类型正确(防止csv读取时变成字符串)，pd.to_numeric()将列转换为数值类型；errors=coerce：转换失败的值设为NaN空值，而不是抛出异常
df['评分'] = pd.to_numeric(df['评分'],errors='coerce')
df['评价人数'] = pd.to_numeric(df['评价人数'],errors='coerce')
#提示用户数据处理阶段完成，开始可视化阶段
print("数据加载完成，开始创建可视化图表...")

#1 创建评分Top10电影柱状图
print("创建评分top10电影图表...")
#使用nlargest（）方法获取评分最高的10部电影，nlargest（10，评分）：按评分列降序排列，取前10个；[['电影名称','评分','评价人数']] 只选择需要的三列
top10_movies = df.nlargest(10,'评分')[['电影名称','评分','评价人数']]
# 缩短长电影名以便显示，.str[:8]截取电影名称前8个字符；+ '...'添加省略表示名称被阶段
top10_movies['显示名称'] = top10_movies['电影名称'].str[:8] + '...'
#创建柱状图对象
bar_top10 = (
    Bar()  #初始化柱状图
    #添加X轴的数据 使用处理后的显示名称列表
    .add_xaxis(top10_movies['显示名称'].tolist())
    #添加Y轴的数据 评分列表；使用列表推导式确保所有评分都是float类型；float（score）将pandas的float64转换为pyhton原生float
    .add_yaxis("评分",[float(score) for score in top10_movies['评分'].tolist()])
    #设置全局配置选项
    .set_global_opts(
        #对标题进行配置：标题居中显示
        title_opts = opts.TitleOpts(title="豆瓣TOP10高评分电影",pos_left="center"),
        #对X轴进行配置：旋转X轴标签45度，避免长名称重叠
        xaxis_opts = opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
        #对Y轴进行配置：name=评分：设置Y轴名称；min_=9.0 Y轴最小值从9.0开始，因为Top10评分都很高 这样可以更好地展示高评分之间的细微差异
        yaxis_opts = opts.AxisOpts(name="评分",min_=9.0), #从九分开始显示
    )
    #设置数据系列配置选项
    .set_series_opts(
        #标签配置：is_show=true 显示数值标签；formatter="{c}" 标签格式，{c}表示显示数据值（评分）
        label_opts=opts.LabelOpts(is_show=True,formatter="{c}"),
        #柱状图样式配置：color=#c23531 设置柱状图颜色为红色，十六进制颜色码#c23531是一种深红色
        itemstyle_opts=opts.ItemStyleOpts(color="#c23531") #设置颜色     
    )
)
#将图表渲染并保存为html文件，render（）生成html文件，可在浏览器中交互查看
bar_top10.render("top10_movies.html")
print("TOP10电影图已保存")

#2 创建评分vs评价人数散点图
print("创建评分vs评价人数散点图...")
# 准备散点图数据：创建一个包含评价人数、评分、电影名称的列表
scatter_data = [] #初始化空列表，用于存储散点图数据点
#遍历dataframe的每一行，iterrows()返回索引和行数据
#_表示索引不使用，row是包含该行数据的series对象
for _,row in df.iterrows():
    #将每部电影的数据作为一个列表添加到scatter_data中
    #格式：[评价人数，评分，电影名称]
    scatter_data.append([row['评价人数'],row['评分'],row['电影名称']])
# 按数据类别进行着色：定义不同类别对应的颜色
# 使用十六进制颜色码，为每个数据类别指定特定的颜色
colors = {
    '优质电影':'#c23531',         #深红色
    '高评分电影':'#2f4554',          #深蓝灰色
    '未满足筛选条件电影':'#61a0a8',   #青蓝色
    '热门电影':'#d48265'            #橙棕色
}    
#创建散点图对象
scatter = (
    Scatter()    #初始化散点图
    #添加x轴数据：所有电影的评价人数列表
    .add_xaxis(df['评价人数'].tolist())
    #添加Y轴数据系列
    .add_yaxis(
        "电影评分",      #数据系列名称
        df['评分'].tolist(),  #y轴数据：所有电影的评分列表
        # 散点大小设置：每个散点的大小为10像素
        symbol_size = 10, 
        #标签配置：不直接在散点上显示数值标签   
        label_opts = opts.LabelOpts(is_show=False),
    )
    #设置全局配置选项
    .set_global_opts(
        #标题配置：标题居中显示
        title_opts = opts.TitleOpts(title="评分vs评价人数关系",pos_left="center"),
        #x轴配置：name=“评价人数”设置x轴名称；type_="value指定为数值轴（连续性数据）
        xaxis_opts = opts.AxisOpts(name="评价人数",type_="value"),
        #y轴配置：name=“评分”设置y轴名称 type_="value"指定为数值轴
        yaxis_opts = opts.AxisOpts(name="评分",type_="value"),
        #工具提示配置（鼠标悬停时显示）
        tooltip_opts = opts.TooltipOpts(
            #格式化工具提示内容：{a}：第一个维度数据{x轴值：评价人数} {b}：第二个维度数据（y轴值：评分） {c}：第三个维度数据（自定义数据：电影名称） <br/>:html换行符
            formatter = "电影:{c}<br/>评分:{b}<br/>评价人数:{a}",
            #触发方式：item表示鼠标悬停在数据项上时显示
            trigger = "item"
        ),
    )
    #设置数据系列样式配置
    .set_series_opts(
        #散点样式配置 设置透明度为0.7（70%不透明），opacity=0.7让散点半透明，便于观察重叠的数据点 
        itemstyle_opts = opts.ItemStyleOpts(opacity=0.7) 
    )
)
#将散点图渲染并保存为html文件
scatter.render("rating_vs_popularity.html")
print("散点图已保存")

#3 数据洞察分析
print("\n数据洞察分析:")
#计算评分与评价人数的皮尔逊相关系数 .corr()：计算两列数据的相关系数（-1到1之间） :.3f格式化输出，保留3位小数
print(f"评分与评价人数的相关性：{df['评分'].corr(df['评价人数']):.3f}")
#相关系数解读：>0.7强正相关，评分越高评价人数越多；0.3-0.7中等正相关；-0.3-0.3弱相关或无相关；<-0.3 负相关；
#找出最高评分的电影 df['评分'].max()：获取评分列的最大值；df['评分'].idxmax()：获取最高评分的索引位置；df.loc[索引，‘电影名称’]：获取该索引对应的电影名称
print(f"最高评分：{df['评分'].max()} - {df.loc[df['评分'].idxmax(),'电影名称']}")
#找出最多评价的电影，:,格式化数字，添加千位分割符（如1，000，000）
print(f"最多评价：{df['评价人数'].max():,} - {df.loc[df['评价人数'].idxmax(),'电影名称']}")
#完成总结
print("\n===进一步可视化完成===")
print("新生成的文件：")
print("--top10_movies.html(TOP10高评分电影)")
print("--rating_vs_popularity.html(评分vs评价人数关系)")
print("在浏览器中交互查看图表")
