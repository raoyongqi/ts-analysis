import arcpy
import pandas as pd
# 定义栅格文件路径
tif_file = r"C:\Users\r\Desktop\ts_analysis\gansu\extracted\extracted_gansu_idgp_2001.tif"

# 检查栅格文件是否存在
if arcpy.Exists(tif_file):
    # 获取字段列表
    fields = arcpy.ListFields(tif_file)
    # 检查 SymLab 字段是否存在
    sym_lab_field = "SymLab"
    if sym_lab_field in [field.name for field in fields]:
        # 使用 SearchCursor 获取 SymLab 字段和 Count 字段的值
        value_count = {}
        with arcpy.da.SearchCursor(tif_file, [sym_lab_field, "Count"]) as cursor:
            for row in cursor:
                sym_lab_value = row[0]
                count_value = row[1]
                
                # 将每个 SymLab 分类及其对应的计数值存储在字典中
                if sym_lab_value not in value_count:
                    value_count[sym_lab_value] = count_value
                else:
                    value_count[sym_lab_value] += count_value  # 如果有重复的值，累加计数
        
        # 按照 Count 值降序排序
        sorted_value_count = sorted(value_count.items(), key=lambda x: x[1], reverse=True)

        # 获取前4个最大的分类
        top_4 = sorted_value_count[:4]

        # 输出前4个按像素计数从大到小排序的 SymLab 分类名称，不包含 Count 值
        top_4_values = [sym_lab_value for sym_lab_value, count in top_4]
        top_4_values.insert(0, 'year')
        # 在列表末尾添加 '其他'
        top_4_values.append('Other')
        df = pd.DataFrame(columns=top_4_values)
    else:
        print(f"栅格文件中没有找到 'SymLab' 字段。")
else:
    print(f"栅格文件 {tif_file} 不存在。")


import os
import glob
# 定义栅格文件夹路径
raster_folder = r"C:\Users\r\Desktop\ts_analysis\gansu\extracted"

# 获取文件夹中所有的 .tif 文件
raster_files = glob.glob(os.path.join(raster_folder, "*.tif"))


year_list = [raster_path.split('_')[-1].split('.')[0] for raster_path in raster_files]


for raster_path in raster_files:
    year = raster_path.split('_')[-1].split('.')[0]
    year_list.append(year)
    sym_lab_field = "SymLab"
    value_count_dict = {}
    total_count = 0
    other_count = 0
    # 使用 SearchCursor 遍历数据
    with arcpy.da.SearchCursor(raster_path, [sym_lab_field, "Count"]) as cursor:
        for row in cursor:
            # 如果 SymLab 字段的值在 top_4_values 中，保存对应的 Count 值
            total_count += row[1]
            if row[0] in top_4_values[1:]:
                value_count_dict[row[0]] = row[1]

            else:
                other_count += row[1]  # 累加不在 top_4_values 中的 Count



        # 如果 total_count 大于 0，计算每个类别的百分比
        if total_count > 0:
            # 计算每个分类的百分比
            percentage_list = [year]  # 初始化列表，第一个是年份
            for class_name in top_4_values[1:5]:
                count_value = value_count_dict.get(class_name, 0)
                percentage = (count_value / total_count) * 100  # 计算百分比
                
                # 将百分比转为字符串并添加 '%' 符号
                percentage_with_sign = f"{percentage:.2f}%"  # 保留两位小数并添加百分号
                percentage_list.append(percentage_with_sign)

        other_percentage = (other_count / total_count) * 100
        other_percentage_with_sign = f"{other_percentage:.2f}%"
        percentage_list.append(other_percentage_with_sign)

        # 将数据添加到 DataFrame 中
        df.loc[len(df)] = percentage_list

# 英文到中文的转换字典
header_translation = {
    "year": "年份",
    "Barren_or_Sparsely_Vegetated": "荒地或稀疏植被",
    "Grasslands": "草地",
    "Croplands": "耕地",
    "Deciduous_Broadleaf_Forests": "落叶阔叶林",
    "Other": "其他"  # 添加“其他”类别的翻译
}


# 使用字典转换表头
translated_columns = [header_translation.get(col, col) for col in df.columns]

# 将转换后的表头赋值给 DataFrame
df.columns = columns = translated_columns
level_1 = ['甘肃省的土地利用情况'] * len(df.columns)

# 创建多级表头 (一级和二级)
multi_index = pd.MultiIndex.from_tuples([(level_1[i], columns[i]) for i in range(len(columns))], names=['一级表头', '二级表头'])

# 更新 DataFrame 的列为多级索引
df.columns = multi_index
# from pandasgui import show
# # 输出 DataFrame 查看
df.to_csv('gansu_land_use.csv', index=False)
df = df.to_string(index=False)
print(df)



