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
        #标题配置：标题居中显示
        title_opts = opts.TitleOpts(title="豆瓣TOP10高评分电影",pos_left="center"),
        #X轴配置：旋转X轴标签45度，避免长名称重叠
        xaxis_opts = opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
        #Y轴配置：name=评分：设置Y轴名称；min_=9.0 Y轴最小值从9.0开始，因为Top10评分都很高 这样可以更好地展示高评分之间的细微差异
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
# 准备散点图数据
scatter_data = []
for _,row in df.iterrows():
    scatter_data.append([row['评价人数'],row['评分'],row['电影名称']])
# 按数据类别进行着色
colors = {
    '优质电影':'#c23531',
    '高评分电影':'#2f4554',
    '未满足筛选条件电影':'#61a0a8',
    '热门电影':'#d48265'
}    
scatter = (
    Scatter()
    .add_xaxis(df['评价人数'].tolist())
    .add_yaxis(
        "电影评分",
        df['评分'].tolist(),
        symbol_size = 10,
        label_opts = opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts = opts.TitleOpts(title="评分vs评价人数关系",pos_left="center"),
        xaxis_opts = opts.AxisOpts(name="评价人数",type_="value"),
        yaxis_opts = opts.AxisOpts(name="评分",type_="value"),
        tooltip_opts = opts.TooltipOpts(
            formatter = "电影:{c}<br/>评分:{b}<br/>评价人数:{a}",
            trigger = "item"
        ),
    )
    .set_series_opts(
        itemstyle_opts = opts.ItemStyleOpts(opacity=0.7) #设置透明度为0.7
    )
)

scatter.render("rating_vs_popularity.html")
print("散点图已保存")

#3 数据洞察分析
print("\n数据洞察分析:")
print(f"评分与评价人数的相关性：{df['评分'].corr(df['评价人数']):.3f}")
print(f"最高评分：{df['评分'].max()} - {df.loc[df['评分'].idxmax(),'电影名称']}")
print(f"最多评价：{df['评价人数'].max():,} - {df.loc[df['评价人数'].idxmax(),'电影名称']}")

print("\n===进一步可视化完成===")
print("新生成的文件：")
print("--top10_movies.html(TOP10高评分电影)")
print("--rating_vs_popularity.html(评分vs评价人数关系)")
print("在浏览器中交互查看图表")
