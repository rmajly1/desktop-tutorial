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

plt.figure(figsize=(8,5))
sns.boxplot(data=df, x="metal", y="band_gap", palette="coolwarm")
plt.xticks(rotation=45)
plt.title("Band Gap Distribution of Metal Oxides (Stable Compounds)")
plt.xlabel("Metal")
plt.ylabel("Band Gap (eV)")
plt.tight_layout()
plt.savefig("boxplot_bandgap_by_metal.png", dpi=300)
plt.show()

plt.figure(figsize=(6,4))
sns.scatterplot(data=df,
                x="formation_energy_per_atom",
                y="band_gap",
                hue="metal",
                palette="tab10", alpha=0.7)
plt.xlabel("Formation Energy (eV/atom)")
plt.ylabel("Band Gap (eV)")
plt.title("Relationship between Formation Energy and Band Gap")
plt.legend(bbox_to_anchor=(1.05,1), loc="upper left")
plt.tight_layout()
plt.savefig("scatter_formation_vs_bandgap.png", dpi=300)
plt.show()

plt.figure(figsize=(6,4))
sns.histplot(df["band_gap"], bins=40, color="steelblue", kde=True)
plt.xlabel("Band Gap (eV)")
plt.ylabel("Count")
plt.title("Overall Band Gap Distribution of Electrochromic Oxides")
plt.tight_layout()
plt.savefig("hist_bandgap_distribution.png", dpi=300)
plt.show()

pivot_df = df.groupby("metal")[["formation_energy_per_atom","band_gap"]].mean().reset_index()

plt.figure(figsize=(5,4))
sns.heatmap(pivot_df.set_index("metal"),
            annot=True, fmt=".2f", cmap="RdYlBu_r")
plt.title("Average Formation Energy & Band Gap by Metal System")
plt.tight_layout()
plt.savefig("heatmap_energy_bandgap.png", dpi=300)
plt.show()

# =============================
# Step 6: 电致变色候选材料筛选
# =============================
candidates = df[(df['band_gap'] >= 1.0) & (df['band_gap'] <= 3.0)]
share = len(candidates) / len(df) * 100
print(f"潜在电致变色候选材料数量：{len(candidates)}，占稳定氧化物的 {share:.1f}%")

# 保存候选列表
candidates.to_csv("electrochromic_candidates.csv", index=False, encoding="utf-8-sig")
print("已保存 electrochromic_candidates.csv")

# =============================
# Step 7: 形成能-带隙 拟合趋势图
# =============================
sns.lmplot(data=df, x="formation_energy_per_atom", y="band_gap",
           hue="metal", height=5, aspect=1.2, scatter_kws={"alpha":0.4})
plt.xlabel("Formation Energy (eV/atom)")
plt.ylabel("Band Gap (eV)")
plt.title("Formation Energy vs Band Gap (Linear Fit)")
plt.tight_layout()
plt.savefig("lmplot_formation_vs_bandgap.png", dpi=300)
plt.show()

# =============================
# Step 8: 热密度分布图
# =============================
sns.kdeplot(
    data=df, x="formation_energy_per_atom", y="band_gap",
    fill=True, cmap="mako", thresh=0.05)
plt.xlabel("Formation Energy (eV/atom)")
plt.ylabel("Band Gap (eV)")
plt.title("Density Map of Stable Metal Oxides")
plt.tight_layout()
plt.savefig("density_map_energy_bandgap.png", dpi=300)
plt.show()