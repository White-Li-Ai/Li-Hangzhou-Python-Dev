#将之前爬取并清洗的豆瓣top250数据可视化（生成柱状图和饼图）
#导入必要的数据处理和可视化库
import pandas as pd #数据处理库
from pyecharts.charts import Bar,Pie,Scatter #导入pyecharts图表类型
from pyecharts import options as opts #导入图表配置选项

print("===数据可视化开始===")

#1 加载已处理好的数据
print("正在加载已处理的数据...")
#读取之前清洗并保存的CSV文件
df = pd.read_csv('douban_top250_processed.csv')
print(f"成功加载！数据形状：{df.shape}")
#数据质量检查 统计缺失值和重复值数量
print(f"数据质量：缺失值{df.isnull().sum().sum()}个，重复值{df.duplicated().sum()}个")
#确保数值列正确数据类型正确（防止读取时类型错误）
df['评分'] = pd.to_numeric(df['评分'],errors='coerce')#errors=coerce 将错误值转为NAN
df['评价人数'] = pd.to_numeric(df['评价人数'],errors='coerce')

#2 数据基本信息
print("\n 数据概览：")
#显示评分范围 保留一位小数
print(f"评分范围：{df['评分'].min():.1f} - {df['评分'].max():.1f}")
#显示平均评分 保留两位小数
print(f"平均评分：{df['评分'].mean():.2f}")
print(f"数据类别分布：")
#遍历每个唯一的数据类别 统计数量
for category in df['数据类别'].unique():
    count = len(df[df['数据类别'] == category])#统计该类别电影数量
    print(f"{category}:{count}部")

#3 创建评分分布柱状图
print("创建评分分布柱状图...")
#计算各评分区间电影数量
#定义评分区间边界
rating_bins = [8.0,8.5,9.0,9.5,10.0]
#对应的区间标签
rating_labels = ['8.0-8.4','8.5-8.9','9.0-9.4','9.5+']
#将连续评分离散化为区间 right=false表示区间左闭右开
df['评分区间'] = pd.cut(df['评分'],bins=rating_bins,labels=rating_labels,right=False)
#检查分箱成果 统计每个区间的电影数量并按区间排序
rating_dist = df['评分区间'].value_counts().sort_index()
print(f"评分分布:{dict(rating_dist)}")
#创建柱状图对象
bar = (Bar()
       #添加X轴数据：评分区间标签列表
       .add_xaxis(rating_dist.index.tolist())
       #添加Y轴数据：各区间电影数量列表，系列名称为电影数量
       .add_yaxis("电影数量",rating_dist.values.tolist())
       #设置全局配置
       .set_global_opts(
           #标题配置：标题居中
           title_opts=opts.TitleOpts(title="豆瓣Top250-评分分布",pos_left="center"),
           #x轴配置：轴名称
           xaxis_opts=opts.AxisOpts(name="评分区间"),
           #y轴配置：轴名称
           yaxis_opts=opts.AxisOpts(name="电影数量"),
           #添加工具箱（包含缩放保存为图片等功能）
           toolbox_opts=opts.ToolboxOpts(),
       )
       #设置系列配置
       .set_series_opts(
           #显示数值标签在柱子上
           label_opts=opts.LabelOpts(is_show=True)
       )
)
#保存图表为html文件
bar.render("rating_distribution.html")
print("评分分布图已保存至rating_distribution.html")

#4 创建数据类别饼图
print("\n创建数据类别饼图...")
#定义类别名称映射，简化过长的类别名称
category_mapping = {
    '优质电影':'优质电影',
    '高评分电影':'高评分电影',
    '原始数据（电影）================（筛选淘汰）================':'未满足筛选条件电影',
    '热门电影':'热门电影'
}
#创建新的简化类别列
df['数据类别_简化'] = df['数据类别'].map(category_mapping)
#统计各类别数量
category_dist = df['数据类别_简化'].value_counts()
#修复数据格式使用Python原生类型 避免pandas类型问题
data_pair = [] #存储饼图数据的列表，格式为[[类别1，数量1]，[类别2，数量2]，...]
for category,count in category_dist.items():
    data_pair.append([category,int(count)]) #转换为普通整数
#创建饼图对象
pie = (Pie()
       .add(
           #系列名称
           series_name = "数据类别",
           #饼图数据
           data_pair = data_pair,
           # 内外半径：30%内半径，75%外半径，形成环形饼图效果
           radius = ["30%","75%"],
       )
       .set_global_opts(
           #标题配置
           title_opts=opts.TitleOpts(title="数据类别分布",pos_left="center"),
           #图列配置：垂直排列，位置在顶部15%、左侧2%
           legend_opts=opts.LegendOpts(orient="vertical",pos_top="15%",pos_left="2%"),                            
       )
       .set_series_opts(
           #标签格式：显示类别名称、数量、百分比
           label_opts=opts.LabelOpts(formatter="{b}:{c}({d}%)"),
       )
)

#保存图表
pie.render("category_distribution.html")
print("类别分布图已保存至category_distribution.html")
#总结输出
print("可视化任务已经成生成的文件为：")
print("---rating_distribution.html(评分分布柱状图)")
print("---category_distribution.html(类别分布饼图)")
print("在浏览器中打开html文件查看交互式图表.")
                    