import pandas as pd
import os

########################
# 製作 color_table_v2_1.csv
# ※ 主要顏色 有些尚未完全分離
#    (有 >= 2 種顏色在 `主要顏色` 欄位)
########################
def generate_structured_color_table():
    color_table_path = "D:/MyPrograms/Clothes2U/DB/供應商資訊 DB/Lativ_product_info/color_table_v2.csv"
    df = pd.read_csv(color_table_path)
    color_names = df["color_name"]
    
    new_columns = {"顏色-1": list(),
                   "顏色-2": list(),
                   "顏色-3": list(),
                   '條': list(), 
                   '邊': list(), 
                   '花': list(),
                   '格': list(),
                   "印花": list(),
                   "方格": list()}
    features = ['條', '邊', "方格", "印花", '格', '花']
    
    for color_name in color_names:
        # 先判斷「是否具有」特殊條紋、花樣
        for feature in features:
            if color_name.endswith(feature):
                if "方格" in color_name and feature=='格':
                    new_columns[feature].append(0)
                elif "印花" in color_name and feature=='花':
                    new_columns[feature].append(0)
                else:
                    new_columns[feature].append(1)
            else:
                new_columns[feature].append(0)

        # 再判斷該 (原始)顏色名稱 的顏色
        for feature in features:
            if feature=='花' and "麻花" in color_name:
                continue
            color_name = color_name.replace(feature, '')
        """
        if '底' in color_name:
            print(color_name)
            # 黑底白條, 白底藏青條, 白底藍條, 黑底桔邊, 黑底黃邊, 黑底粉花
        """
        if '底' in color_name:  # 有 "輔色"
            tmp_idx = color_name.index('底')
            new_columns["顏色-1"].append(color_name[:tmp_idx])
            new_columns["顏色-2"].append(color_name[tmp_idx+1:])
            new_columns["顏色-3"].append("X")
        else:  # 無 "輔色"
            new_columns["顏色-1"].append(color_name)
            new_columns["顏色-2"].append("X")
            new_columns["顏色-3"].append("X")
    
    #print(new_columns)
    df_out = pd.DataFrame.from_dict(new_columns)
    output_color_table_path = "D:/MyPrograms/Clothes2U/DB/供應商資訊 DB/Lativ_product_info/color_table_v2_1.csv"
    df_out = pd.concat([df, df_out], axis=1)
    df_out.to_csv(output_color_table_path, encoding="utf-8-sig", index=False)

########################
# 複製一份 color_table_v2_1.csv，取名為 color_table_v2_2.csv
# 將 color_table_v2_2.csv 中，主要顏色大於一種的資料，
# 手動拆到輔色。並利用 manual_def_colors 製作 color_table_v2_3.csv
# 如: (主色)藏青粉紅 => (主色)藏青 (輔色)粉紅
########################
def manually_classify_colors():
    color_table_path = "D:/MyPrograms/Clothes2U/DB/供應商資訊 DB/Lativ_product_info/color_table_v2_2.csv"
    
    df = pd.read_csv(color_table_path)
    main_colors, sub_colors_1, sub_colors_2 = df["主要顏色"], df["輔色-1"], df["輔色-2"]
    tmp = main_colors.append(sub_colors_1)
    colors = set(tmp.append(sub_colors_2))
    
    manual_def_colors = {"紅": ["玫紅","深玫紅","磚紅",
                               "亮紅","紅色","深紅",
                               "酒紅","深酒紅","桃紅",
                               "暗紅","珊瑚紅","暮紅",
                               "紅"],
                         "橙": ["粉橘","桔","淺桔",
                               "磚桔","暗桔","桔色",
                               "亮桔","深桔","橘",
                               "麻花桔"],
                         "黃": ["鵝黃","淡黃","黃",
                               "芥黃","粉黃","黃色",
                               "淺黃","麻花黃","暖黃",
                               "亮黃","復古黃"],
                         "粉": ["淺粉","桃粉","粉色",
                               "粉","淡粉","亮粉",
                               "嫩粉","淺粉紅","粉紅",
                               "深粉","深粉紅","亮桃粉",
                               "麻花粉","藕粉","珊瑚粉"],
                         "青": ["藏青","深藏青","麻花藏青"],
                         "藍": ["天藍","湖綠藍","麻花藍",
                               "淺藍","藍","礦藍",
                               "丹寧藍","亮藍","藍色",
                               "湖藍","深藍","復古藍",
                               "淺麻花藍","水藍","寶藍",
                               "深麻花藍","淡藍","麻花淺藍",
                               "牛仔藍","麻花深藍"],
                         "紫": ["深紫","麻花紫","紫色",
                               "淺紫","淡紫","玫紫",
                               "紫"],
                         "綠": ["綠色","軍綠","水綠",
                               "淺綠","橄欖綠","湖綠",
                               "湖水綠","亮綠","暗綠",
                               "深綠","淺水綠","嫩綠",
                               "墨綠","淺湖綠","深軍綠",
                               "藏青綠","麻花綠","草綠",
                               "綠"],
                         "灰": ["黑麻灰","深灰色",
                               "深麻灰","深灰","灰色",
                               "暗灰","卡其灰","鐵灰",
                               "黑灰","麻灰","淺灰",
                               "麻花灰","淺麻灰","灰"],
                         "黑": ["黑","黑色","麻花黑"],
                         "白": ["白","米杏","白色",
                               "米色","麻灰白","白色02",
                               "米白","麻花米","淺杏",
                               "杏色","白色01","米"],
                         "咖啡": ["咖啡","深咖","淺咖",
                                 "麻花咖","棕色","褐色",
                                 "棕","淺棕"],
                         "多色組": ["多色組","多色組01","多色組02",
                                  "多色組03","多色組04","多色組05",
                                  "多色組1","多色組2","多色組3"],
                         "卡其": ["卡其","淺卡其","深卡其",
                                "麻花卡其"],
                         "膚色": ["膚色","淺膚"],
                         "其它": ["X", "駝色", "彩"]
                         }
    print(manual_def_colors, '\n')
    n=0; c=0
    for color in colors:
        is_mapped = False
        for k, v in manual_def_colors.items():
            #if k in color:
            for def_color in v:
                if def_color==color:
                    is_mapped = True
        if not is_mapped:
            print(color, end=' ')
            c += 1
        else:
            n += 1
    print('\n已歸類顏色名稱:', n, sep='')
    print('\n未歸類顏色名稱:', c, sep='')

########################
# 列出顏色 icon 的商品頁連結
########################
def get_color_icon_links():
    csv_path = "D:/MyPrograms/Clothes2U/DB/供應商資訊 DB/Lativ_product_info/tier_2_v6_3.csv"
    color_icon_links = dict()
    df = pd.read_csv(csv_path)
    prod_links = df["product_link"]
    color_nums = df["color_num"]
    for color_num, prod_link in zip(color_nums, prod_links):
        color_icon_links.setdefault(color_num, set())
        color_icon_links[color_num].add(prod_link)
    #print(sorted(color_icon_links.items(), key=lambda k_v:k_v[0]))
    return color_icon_links

########################
# 利用 get_color_icon_links() 依序將 顏色icons 補齊
########################
def complete_color_icons():
    csv_path = "D:/MyPrograms/Clothes2U/DB/供應商資訊 DB/Lativ_product_info/color_table_v2_3.csv"
    color_icon_dir = "D:/MyPrograms/Clothes2U/DB/服飾圖片 DB/Lativ/media2/color_icons"
    df = pd.read_csv(csv_path)
    color_icon_links = get_color_icon_links()
    for i, record in df.iterrows():
        color_num = record["color_number"]
        color_name = record['color_name']
        prod_links = color_icon_links.get(color_num)
        color_icon_path = f"{color_icon_dir}/{color_num}.jpg"
        if os.path.exists(color_icon_path):
            print(f"[ALERT] 顏色編號:{color_num} 的顏色icon 已存在")
        else:
            print(f"\n需取得`顏色編號`為 {color_num} 的顏色 icon")
            print(f"`顏色名稱`: {color_name}")
            print("\n顏色 icon可造訪以下連結取得:")
            print(*(link for link in prod_links), sep='\n')            
            ans = input(f"請將 {color_name} 的顏色icon 放置到以下路徑:\n{color_icon_path}\n(press 'q' to exit): ")
            if ans == 'q':
                break

if __name__ == "__main__":
    generate_structured_color_table()
    #manually_classify_colors()
    #complete_color_icons()
