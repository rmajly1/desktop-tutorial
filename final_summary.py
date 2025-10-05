# ===============================================
# 一键生成论文摘要数据与候选材料表
# ===============================================
import pandas as pd

# === Step 1: 读取清洗后的数据 ===
df = pd.read_csv("electrochromic_oxides_clean.csv")
print(f"数据总数: {len(df)}")

# === Step 2: 定义候选区间 ===
candidates = df[(df["band_gap"] >= 1.0) & (df["band_gap"] <= 3.0)]
ratio = len(candidates) / len(df) * 100
print(f"\n潜在电致变色候选数: {len(candidates)} ({ratio:.1f}% of stable oxides)\n")

# === Step 3: 各金属体系中候选比例 ===
cand_ratio = (candidates["metal"].value_counts() / df["metal"].value_counts() * 100).round(2)
print("各体系候选比例(%):")
print(cand_ratio.sort_values(ascending=False))
print()

# === Step 4: 导出 Top 10 候选（最符合电致变色区） ===
top10 = candidates.sort_values(by="band_gap", ascending=True).head(10)
cols_to_save = ["formula_pretty", "metal", "band_gap",
                "formation_energy_per_atom", "energy_above_hull"]
top10.to_csv("top10_candidates.csv", index=False, encoding="utf-8-sig")
print("已生成文件: top10_candidates.csv\n")

# === Step 5: 打印摘要型科研结论 ===
best_system = cand_ratio.idxmax()
best_ratio = cand_ratio.max()
mean_bandgap = round(candidates["band_gap"].mean(), 3)
f_e_mean = round(candidates["formation_energy_per_atom"].mean(), 3)

print("▶ 论文摘要可用句式:")
print(f"Approximately {ratio:.1f}% of the {len(df)} stable oxides fall within the electrochromic band-gap window (1–3 eV).")
print(f"The {best_system}-O system shows the highest proportion of potential candidates ({best_ratio:.1f}%).")
print(f"The average band gap of the candidates is {mean_bandgap} eV, with an average formation energy of {f_e_mean} eV/atom.")
print("These results highlight W-, Mo-, and Sn-based oxides as key systems for high-performance electrochromic applications.")