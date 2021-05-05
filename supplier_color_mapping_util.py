import pandas as pd
import os

########################
# [流程-1] 製作 color_table_v2_1.csv
# => 將原始 `顏色名稱` 拆為「顏色分量」和「花紋」
#    「顏色分量」: 3 個單一顏色，「顏色-1」、「顏色-2」、「顏色-3」
#     (因為原始顏色名稱觀察過最多包含(可分解為)3種不同的單一顏色)
########################
def generate_structured_color_table():
    color_table_path = "D:/MyPrograms/Clothes2U/DB/供應商資訊 DB/Lativ_product_info/color_table.csv"
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
    stripes = get_stripes()
    for color_name in color_names:
        # 先判斷「是否具有」特殊條紋、花樣
        for stripe in stripes:
            if color_name.endswith(stripe):
                if "方格" in color_name and stripe=='格':
                    new_columns[stripe].append(0)
                elif "印花" in color_name and stripe=='花':
                    new_columns[stripe].append(0)
                else:
                    new_columns[stripe].append(1)
            else:
                new_columns[stripe].append(0)

        # 再判斷該 (原始)顏色名稱 的顏色
        for stripe in stripes:
            if stripe=='花' and "麻花" in color_name:
                continue
            color_name = color_name.replace(stripe, '')
        """
        if '底' in color_name:
            print(color_name)
            # 黑底白條, 白底藏青條, 白底藍條, 黑底桔邊, 黑底黃邊, 黑底粉花
        """
        if '底' in color_name:
            # Imply `color_name` must contain 2 or more colors, i.e.,`顏色分量`
            tmp_idx = color_name.index('底')
            new_columns["顏色-1"].append(color_name[:tmp_idx])
            new_columns["顏色-2"].append(color_name[tmp_idx+1:])
            new_columns["顏色-3"].append("X")
        else:
            # Suppose `color_name` has only 1 color 
            # i.e., If # of colors is more than 1, and the final result hasn't been formed, 
            #       `color_table_v2_2.csv` needs to be modified manually.
            new_columns["顏色-1"].append(color_name)
            new_columns["顏色-2"].append("X")
            new_columns["顏色-3"].append("X")
    #print(new_columns)
    df_out = pd.DataFrame.from_dict(new_columns)
    output_color_table_path = "D:/MyPrograms/Clothes2U/DB/供應商資訊 DB/Lativ_product_info/color_table_v2_1.csv"
    df_out = pd.concat([df, df_out], axis=1)
    df_out.to_csv(output_color_table_path, encoding="utf-8-sig", index=False)

########################
# [流程-2 util] 取得 "manual_def_colors" (手工增修的(階層式)顏色群組表)
# => 內容可視需要手動調整
########################
def get_manual_def_colors():
    return {"紅色": ["玫紅","深玫紅","磚紅",
                  "亮紅","紅色","深紅",
                  "酒紅","深酒紅","桃紅",
                  "暗紅","珊瑚紅","暮紅",
                  "紅"],
            "橙色": ["粉橘","桔","淺桔",
                  "磚桔","暗桔","桔色",
                  "亮桔","深桔","橘",
                  "麻花桔"],
            "黃色": ["鵝黃","淡黃","黃",
                  "芥黃","粉黃","黃色",
                  "淺黃","麻花黃","暖黃",
                  "亮黃","復古黃"],
            "粉紅色": ["淺粉","桃粉","粉色",
                  "粉","淡粉","亮粉",
                  "嫩粉","淺粉紅","粉紅",
                  "深粉","深粉紅","亮桃粉",
                  "麻花粉","藕粉","珊瑚粉"],
            "青色": ["藏青","深藏青","麻花藏青"],
            "藍色": ["天藍","湖綠藍","麻花藍",
                  "淺藍","藍","礦藍",
                  "丹寧藍","亮藍","藍色",
                  "湖藍","深藍","復古藍",
                  "淺麻花藍","水藍","寶藍",
                  "深麻花藍","淡藍","麻花淺藍",
                  "牛仔藍","麻花深藍"],
            "紫色": ["深紫","麻花紫","紫色",
                  "淺紫","淡紫","玫紫",
                  "紫"],
            "綠色": ["綠色","軍綠","水綠",
                  "淺綠","橄欖綠","湖綠",
                  "湖水綠","亮綠","暗綠",
                  "深綠","淺水綠","嫩綠",
                  "墨綠","淺湖綠","深軍綠",
                  "藏青綠","麻花綠","草綠",
                  "綠"],
            "灰色": ["黑麻灰","深灰色",
                  "深麻灰","深灰","灰色",
                  "暗灰","卡其灰","鐵灰",
                  "黑灰","麻灰","淺灰",
                  "麻花灰","淺麻灰","灰"],
            "黑色": ["黑","黑色","麻花黑"],
            "白色": ["白","米杏","白色",
                  "米色","麻灰白","白色02",
                  "米白","麻花米","淺杏",
                  "杏色","白色01","米"],
            "咖啡色": ["咖啡","深咖","淺咖",
                    "麻花咖","棕色","褐色",
                    "棕","淺棕"],
            "多色組": ["多色組","多色組01","多色組02",
                     "多色組03","多色組04","多色組05",
                     "多色組1","多色組2","多色組3"],
            "卡其色": ["卡其","淺卡其","深卡其",
                   "麻花卡其"],
            "膚色": ["膚色","淺膚"],
            "其它顏色": ["X", "駝色", "彩"] }

########################
# [流程-2] 印出已歸類 & 尚未歸類顏色名稱，
# 輔助手工修改 "manual_def_colors"
########################
def manually_classify_colors():
    color_table_path = "D:/MyPrograms/Clothes2U/DB/供應商資訊 DB/Lativ_product_info/color_table_v2_2.csv"
    
    df = pd.read_csv(color_table_path)
    colors = df["顏色-1"], df["顏色-2"], df["顏色-3"]
    tmp = colors[0].append(colors[1])
    colors = set(tmp.append(colors[2]))
    
    manual_def_colors = get_manual_def_colors()
    print(manual_def_colors, '\n')
    classified_num, unclassified_num = 0, 0
    for color in colors:
        is_mapped = False
        for k, v in manual_def_colors.items():
            for def_color in v:
                if def_color == color:
                    is_mapped = True
        if not is_mapped:
            print(color, end=' ')
            unclassified_num += 1
        else:
            classified_num += 1
    print('\n已歸類顏色名稱:', classified_num, sep='')
    print('\n尚未歸類顏色名稱:', unclassified_num, sep='')

########################
# [流程-3 util] 列出顏色 icon 的商品頁連結
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
# [流程-3] 利用 get_color_icon_links() 依序將 顏色icons 補齊
########################
def complete_color_icons():
    csv_path = "D:/MyPrograms/Clothes2U/DB/供應商資訊 DB/Lativ_product_info/color_table_v2_3.csv"
    color_icon_dir = "D:/MyPrograms/Clothes2U/DB/服飾圖片 DB/Lativ/media2/color_icons"
    df = pd.read_csv(csv_path)
    color_icon_links = get_color_icon_links()
    for i, record in df.iterrows():
        color_num = record["color_number"]
        color_name = record["color_name"]
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

########################
# [流程-4 util] 取得「顏色聚類」
# => manual_def_colors (<dict>) 的 keys
########################
def get_color_cluster(uni_color_type):
    if uni_color_type == "X":
        return None
    manual_def_colors = get_manual_def_colors()
    for k, v in manual_def_colors.items():
        if uni_color_type in v:
            return k
    return None

########################
# [流程-4] 取得 `顏色分量`-`顏色名稱` 對應表 (<dict>)
# => 可利用 (欲上架 SKU 商品)`顏色分量` 找到 相對應的所有 (原始)`顏色名稱`
#    作為 <供應商-商品上傳-(SKU)顏色選擇> 的前置作業
#    即: 先選擇該 SKU 商品具有的「單一顏色」(任意/擇一)，再展開相關 `顏色名稱`，
#    最後完成「SKU 商品顏色屬性」的設定
# [註] 原始 `顏色名稱` 有包含「花紋」和「1至多種單一顏色」(最多有3種)
########################
def get_color_cluster_to_color_name_mapping():
    csv_path = "D:/MyPrograms/Clothes2U/DB/供應商資訊 DB/Lativ_product_info/color_table_v2_2.csv"
    df = pd.read_csv(csv_path)
    
    color_cluster_to_color_name_mapping = dict()
    for i, record in df.iterrows():
        uni_color_types = [record[f"顏色-{i}"] for i in range(1, 4)]
        color_name = record["color_name"]
        for uni_color_type in uni_color_types:
            color_cluster = get_color_cluster(uni_color_type)
            if color_cluster is not None:
                color_cluster_to_color_name_mapping.setdefault(color_cluster, set())
                color_cluster_to_color_name_mapping[color_cluster].add(color_name)
    #print(color_cluster_to_color_name_mapping)
    ''' 
    for k, v in color_cluster_to_color_name_mapping.items():
        print(k)
    print(len(color_cluster_to_color_name_mapping.keys()))
    '''
    return color_cluster_to_color_name_mapping

########################
# [流程-5 util] 取得「花紋」
########################
def get_stripes():
    # [註] "方格" 必先於 '格', "印花" 必先於 '花'
    #      (因為 '花' 可能包含 "印花"，必須置於 "印花" 之後)
    return ['條', '邊', "方格", "印花", '格', '花']

########################
# [流程-5] 取得 `花紋`-`顏色名稱` 對應表 (<dict>)
# => 可利用 (若欲上架 SPU 商品具有)`花紋` 找到 相對應的所有 (原始)`顏色名稱`
#    作為 <供應商-商品上傳-(SPU)花紋匹配> 的前置作業
#    即: 先選擇該 SPU 商品 (包括底下所有SKU) 具有的「花紋」，
#    再展開相關 `顏色名稱`，最後完成「SKU 商品顏色屬性」的設定
# [註] 原始 `顏色名稱` 有包含「花紋」和「1至多種單一顏色」(最多有3種)
########################
def get_stripe_to_color_name_mapping():
    csv_path = "D:/MyPrograms/Clothes2U/DB/供應商資訊 DB/Lativ_product_info/color_table_v2_2.csv"
    df = pd.read_csv(csv_path)
    
    stripe_to_color_name_mapping = dict()
    [stripe_to_color_name_mapping.setdefault(stripe, list(df[df[stripe]==1]["color_name"])) 
     for stripe in get_stripes()]
    return stripe_to_color_name_mapping

if __name__ == "__main__":
    # [流程-1] 製作 color_table_v2_1.csv
    # => 將原始 `顏色名稱` 拆為「顏色分量」和「花紋」
    ''' generate_structured_color_table() '''
    
    # [流程-2] 印出已歸類 & 尚未歸類顏色名稱，
    # 輔助手工修改 "manual_def_colors"
    ''' manually_classify_colors() '''
    
    # [流程-3] 利用 get_color_icon_links() 依序將 顏色icons 補齊
    ''' complete_color_icons() '''
    
    # [流程-4] 取得 `顏色分量`-`顏色名稱` 對應表 (<dict>)
    '''
    color_cluster_name_mapping = get_color_cluster_to_color_name_mapping()
    # ===test===
    color_cluster = "紅色" # <-- supplier 從 前端/UI 選取的 `顏色聚類` 
    print(f"supplier 前端/UI選取顏色: {color_cluster}")
    print("\n列出相關 `原始顏色名稱`(準備進入下一流程): ")
    print(color_cluster_name_mapping[color_cluster]) # <-- 下一頁(步) / 顯示相關顏色名稱 & 顏色 icons
    '''
    
    # [流程-5] 取得 `花紋`-`顏色名稱` 對應表 (<dict>)
    '''
    stripe_to_color_name_mapping = get_stripe_to_color_name_mapping()
    # ===test===
    # print(stripe_to_color_name_mapping)
    stripe = "印花" # <-- supplier 從 前端/UI 選取的 `花紋` 
    print(f"supplier 前端/UI選取花紋: {stripe}")
    print("\n列出相關 `原始顏色名稱`(準備進入下一流程): ")
    print(stripe_to_color_name_mapping[stripe]) # <-- 下一頁(步) / 顯示相關顏色名稱 & 顏色 icons
    '''
    
    pass