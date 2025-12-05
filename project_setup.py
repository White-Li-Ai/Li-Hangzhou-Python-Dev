#创建项目基础文件

import os
#创建项目文件夹
project_dir = "hangzhou_jobs_analysis"
os.makedirs(project_dir,exist_ok=True)
os.chdir(project_dir)
#创建requirements.txt
with open('requirements.txt','w',encoding='utf-8') as f:
    f.write("""requests===2.31.0
            pandas==2.0.3
            pyecharts==2.0.3
            jupyter==1.0.0
            """)
print(f"项目文件夹'{project_dir}创建成功！")
print("项目结构已初始化")
