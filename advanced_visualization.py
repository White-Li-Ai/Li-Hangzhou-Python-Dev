#对之前爬取的豆瓣top250数据进行进一步处理（Top10电影图、散点图、数据洞察分析）

import pandas as pd
from pyecharts.charts import Bar,Scatter,Page
from pyecharts import options as opts

print("===进一步数据可视化开始===")

#加载数据
df = pd.read_csv('douban_top250_processed.csv')
df['评分'] = pd.to_numeric(df['评分'],errors='coerce')
df['评价人数'] = pd.to_numeric(df['评价人数'],errors='coerce')
print("数据加载完成，开始创建可视化图表...")

#1 创建评分Top10电影柱状图
print("创建评分top10电影图表...")
top10_movies = df.nlargest(10,'评分')[['电影名称','评分','评价人数']]
# 缩短长电影名以便显示
top10_movies['显示名称'] = top10_movies['电影名称'].str[:8] + '...'

bar_top10 = (
    Bar()
    .add_xaxis(top10_movies['显示名称'].tolist())
    #确保float类型
    .add_yaxis("评分",[float(score) for score in top10_movies['评分'].tolist()])
    .set_global_opts(
        title_opts = opts.TitleOpts(title="豆瓣TOP10高评分电影",pos_left="center"),
        xaxis_opts = opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
        yaxis_opts = opts.AxisOpts(name="评分",min_=9.0), #从九分开始显示
    )
    .set_series_opts(
        label_opts=opts.LabelOpts(is_show=True,formatter="{c}"),
        itemstyle_opts=opts.ItemStyleOpts(color="#c23531") #设置颜色     
    )
)

bar_top10.render("top10_movies.html")
print("TOP10电影图已保存")

#2 创建评分vs评价人数散点图
print("创建评分vs评价人数散点图...")
# 准备散点图数据
scatter_data = []
for _,row in df.iterrows():
    scatter_data.append([row['评价人数'],row['评分'],row['电影名称']])
# 按数据类别着色
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
        itemstyle_opts = opts.ItemStyleOpts(opacity=0.7) #设置透明度
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
