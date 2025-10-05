from mp_api.client import MPRester
import pandas as pd
import time

API_KEY = "gK5ERf7UjETZINqTPzlLRTSpW8Th92Uk"   # ← 填上自己的Key
mpr = MPRester(API_KEY)

metal_list = ["W", "Mo", "Nb", "V", "Ni", "Co", "Fe", "Mn", "Ti", "Sn", "Zn", "Al"]

all_data = []

for m in metal_list:
    print(f"正在下载 {m}-O 系统数据 …")
    try:
        # ✅ 关键修改：elements 用列表，不用字符串
        docs = mpr.materials.summary.search(
            elements=[m, "O"],        # 二元体系
            num_elements=(2, 3),
            fields=[
                "material_id",
                "formula_pretty",
                "band_gap",
                "formation_energy_per_atom",
                "energy_above_hull",
                "density",
                "volume",
                "nsites",
                "elements",
            ],
        )

        df_temp = pd.DataFrame([d.dict() for d in docs])
        df_temp["metal"] = m
        all_data.append(df_temp)

    except Exception as e:
        print(f"{m} 查询失败：{e}")
        continue

    time.sleep(0.5)  # 防止触发访问频率限制

# === 合并结果 ===
if all_data:
    df = pd.concat(all_data, ignore_index=True)
    print("总下载条目数：", len(df))
    df.to_csv("electrochromic_oxides_raw.csv", index=False, encoding="utf-8-sig")
    print("数据保存为 electrochromic_oxides_raw.csv")
else:
    print("没有成功获取到任何数据，请检查网络或 API key。")