import arcpy
import pandas as pd
# 定义栅格文件路径
tif_file = r"C:\Users\r\Desktop\ts_analysis\gansu\extracted\extracted_gansu_idgp_2001.tif"

# 检查栅格文件是否存在
if arcpy.Exists(tif_file):
    # 获取字段列表
    fields = arcpy.ListFields(tif_file)
    print(f"栅格文件的字段列表：")
    for field in fields:
        print(f"字段名称: {field.name}, 字段类型: {field.type}")
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
        print("\n按像素计数从大到小排序后的前 4 个 SymLab 分类名称：")
        top_4_values.insert(0, 'year')
        df = pd.DataFrame(columns=top_4_values)
        print(df)
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

for raster_path in raster_files:
    year = raster_path.split('_')[-1].split('.')[0]
    sym_lab_field = "Value"
    value_count_dict = {}
    print(year)
    # 使用 SearchCursor 遍历数据
    with arcpy.da.SearchCursor(raster_path, [sym_lab_field, "Count"]) as cursor:
        for row in cursor:
            # 如果 SymLab 字段的值在 top_4_values 中，保存对应的 Count 值

            value_count_dict[row[0]] = row[1]

    # 输出字典，查看提取结果
    print(value_count_dict)
