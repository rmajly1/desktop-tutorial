import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8-paper")

# === Step 1: 读取数据 ===
df = pd.read_csv("electrochromic_oxides_raw.csv")
print("原始数据量：", len(df))
print(df.columns)

# === Step 2: 删除缺失值 ===
df = df.dropna(subset=["band_gap", "formation_energy_per_atom", "energy_above_hull"])
print("清洗后剩余：", len(df))

# === Step 3: 保留热稳定化合物 ===
df = df[df["energy_above_hull"] < 0.05]
print("稳定材料条目：", len(df))

# === Step 4: 带隙合理区间（过滤异常）===
df = df[(df["band_gap"] >= 0) & (df["band_gap"] < 6)]
print("筛选后条目：", len(df))

# === 保存清洗后的数据 ===
df.to_csv("electrochromic_oxides_clean.csv", index=False)
print("已保存清洗后文件 electrochromic_oxides_clean.csv")

# === Step 5: 快速统计 ===
group_mean = df.groupby("metal")["band_gap"].mean().sort_values(ascending=False)
print("\n各金属体系平均带隙(eV)：\n", group_mean)