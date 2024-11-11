import pandas as pd
import matplotlib.pyplot as plt

# 读取 CSV 文件，指定第二行作为表头
df = pd.read_csv('gansu_land_use.csv', header=1)
import os


title = pd.read_csv('gansu_land_use.csv').columns[0]




# 将百分比字符串转换为浮动数字
for column in df.columns[1:]:
    df[column] = df[column].str.rstrip('%').astype(float)

# 绘制趋势图
import matplotlib
# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 或者 ['Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# 绘制每一列的数据
pic_folder = r"C:\Users\r\Desktop\ts_analysis\pic"

# 检查输出文件夹是否存在，不存在则创建
if not os.path.exists(pic_folder):
    os.makedirs(pic_folder)

# 绘制每一列的数据，并保存为 gansu_land_use_i.png
for i, column in enumerate(df.columns[1:len(df.columns)-1], start=1):
    plt.figure(figsize=(10, 6))

    # 绘制数据
    plt.plot(df['年份'], df[column], label=column)

    # 设置图形标题和标签
    plt.title(f'{title[:-6]}{column}面积变化情况(2001-2020)', fontsize=14)  # 动态设置标题
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('百分比(%)', fontsize=12)

    # 显示图例
    plt.legend()

    # 保存图像到本地，文件名为 gansu_land_use_i.png
    plt.savefig(f'{pic_folder}/gansu_land_use_{i}.png', dpi=300)

    # 显示图表
    plt.show()