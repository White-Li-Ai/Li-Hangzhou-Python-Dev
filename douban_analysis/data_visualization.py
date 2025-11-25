#将之前爬取并清洗的豆瓣top250数据可视化（生成柱状图和饼图）
import pandas as pd
from pyecharts.charts import Bar,Pie,Scatter
from pyecharts import options as opts

print("===数据可视化开始===")

#1 加载已处理好的数据
print("正在加载已处理的数据...")
df = pd.read_csv('douban_top250_processed.csv')
print(f"成功加载！数据形状：{df.shape}")
#数据质量检查
print(f"数据质量：缺失值{df.isnull().sum().sum()}个，重复值{df.duplicated().sum()}个")
#确保数值列正确
df['评分'] = pd.to_numeric(df['评分'],errors='coerce')
df['评价人数'] = pd.to_numeric(df['评价人数'],errors='coerce')

#2 数据基本信息
print("\n 数据概览：")
print(f"评分范围：{df['评分'].min():.1f} - {df['评分'].max():.1f}")
print(f"平均评分：{df['评分'].mean():.2f}")
print(f"数据类别分布：")
for category in df['数据类别'].unique():
    count = len(df[df['数据类别'] == category])
    print(f"{category}:{count}部")

#3 创建评分分布柱状图
print("创建评分分布柱状图...")
#计算各评分区间电影数量
rating_bins = [8.0,8.5,9.0,9.5,10.0]
rating_labels = ['8.0-8.4','8.5-8.9','9.0-9.4','9.5+']
df['评分区间'] = pd.cut(df['评分'],bins=rating_bins,labels=rating_labels,right=False)
#检查分箱成果
rating_dist = df['评分区间'].value_counts().sort_index()
print(f"评分分布:{dict(rating_dist)}")
#创建柱状图
bar = (Bar()
       .add_xaxis(rating_dist.index.tolist())
       .add_yaxis("电影数量",rating_dist.values.tolist())
       .set_global_opts(
           title_opts=opts.TitleOpts(title="豆瓣Top250-评分分布",pos_left="center"),
           xaxis_opts=opts.AxisOpts(name="评分区间"),
           yaxis_opts=opts.AxisOpts(name="电影数量"),
           #添加工具箱（缩放保存等）
           toolbox_opts=opts.ToolboxOpts(),
       )
       .set_series_opts(
           #显示数值标签
           label_opts=opts.LabelOpts(is_show=True)
       )
)
#保存图表
bar.render("rating_distribution.html")
print("评分分布图已保存至rating_distribution.html")

#4 创建数据类别饼图
print("\n创建数据类别饼图...")
category_mapping = {
    '优质电影':'优质电影',
    '高评分电影':'高评分电影',
    '原始数据（电影）================（筛选淘汰）================':'未满足筛选条件电影',
    '热门电影':'热门电影'
}
df['数据类别_简化'] = df['数据类别'].map(category_mapping)
category_dist = df['数据类别_简化'].value_counts()
#修复数据格式使用Python原生类型
data_pair = []
for category,count in category_dist.items():
    data_pair.append([category,int(count)]) #转换为普通整数

pie = (Pie()
       .add(
           series_name = "数据类别",
           data_pair = data_pair,
           # 内外半径
           radius = ["30%","75%"],
       )
       .set_global_opts(
           title_opts=opts.TitleOpts(title="数据类别分布",pos_left="center"),
           legend_opts=opts.LegendOpts(orient="vertical",pos_top="15%",pos_left="2%"),                            
       )
       .set_series_opts(
           #显示百分比
           label_opts=opts.LabelOpts(formatter="{b}:{c}({d}%)"),
       )
)

#保存图表
pie.render("category_distribution.html")
print("类别分布图已保存至category_distribution.html")

print("可视化任务已经成生成的文件为：")
print("---rating_distribution.html(评分分布柱状图)")
print("---category_distribution.html(类别分布饼图)")
print("在浏览器中打开html文件查看交互式图表.")
                    