# -*- coding: utf-8 -*-
"""04_visuals.py 可视化：模板复现类 fig01–fig12 + 业务模型类 fig13–fig18
统一风格：Microsoft YaHei、150dpi、figXX_名称.png 命名，输出至 outputs/figures/"""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
FIG = BASE / "outputs" / "figures"
TAB = BASE / "outputs" / "tables"
FIG.mkdir(parents=True, exist_ok=True)
CLEAN = BASE / "data" / "clean"

# 全局风格
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 150
PALETTE = ["#2E6FB7", "#E8833A", "#4CAF7D", "#C0504D", "#9B59B6",
           "#16A085", "#F1C40F", "#7F8C8D", "#E74C3C", "#34495E"]
sns.set_palette(PALETTE)

df = pd.read_csv(CLEAN / "encounters_clean.csv")

def save(fig, name):
    fig.tight_layout()
    fig.savefig(FIG / name, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("saved", name)

# ---------- fig01 模板复现：分组柱状图（各入院途径的就诊量与再入院人数） ----------
g = df.groupby("admission_type").agg(就诊量=("encounter_id", "count"), 再入院人数=("readmit_30d", "sum"))
fig, ax = plt.subplots(figsize=(7, 4.2))
x = np.arange(len(g)); w = 0.38
ax.bar(x - w / 2, g["就诊量"], w, label="就诊量", color=PALETTE[0])
ax.bar(x + w / 2, g["再入院人数"], w, label="30天再入院人数", color=PALETTE[1])
ax.set_xticks(x, g.index); ax.set_ylabel("人次"); ax.set_title("图1 各入院途径就诊量与再入院（分组柱状图）")
ax.legend(); save(fig, "fig01_入院途径就诊量_分组柱状图.png")

# ---------- fig02 模板复现：饼图（种族构成） ----------
race_cn = {"Caucasian": "白人", "AfricanAmerican": "非裔", "Hispanic": "西班牙裔",
           "Asian": "亚裔", "Other": "其他", "未知": "未知"}
rc = df["race"].map(race_cn).value_counts()
fig, ax = plt.subplots(figsize=(6.5, 4.5))
wedges, texts = ax.pie(rc, startangle=90, colors=PALETTE[:len(rc)],
                       wedgeprops={"width": 0.55, "edgecolor": "white"})
# 大扇区直接标注百分比，小扇区并入图例避免标签重叠
for w, (name, v) in zip(wedges, rc.items()):
    pct = v / rc.sum()
    if pct >= 0.05:
        ang = np.deg2rad((w.theta1 + w.theta2) / 2)
        ax.text(0.78 * np.cos(ang), 0.78 * np.sin(ang), f"{name}\n{pct*100:.1f}%",
                ha="center", va="center", fontsize=9)
ax.legend(wedges, [f"{n}  {v:,}人（{v/rc.sum()*100:.1f}%）" for n, v in rc.items()],
          loc="center left", bbox_to_anchor=(0.95, 0.5), fontsize=8)
ax.set_title("图2 住院患者种族构成（环形饼图）"); save(fig, "fig02_种族构成_饼图.png")

# ---------- fig03 模板复现：条形图（年龄段分布） ----------
age_order = sorted(df["age_group"].unique(), key=lambda s: int(s.split("-")[0]))
ag = df["age_group"].value_counts().reindex(age_order)
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.bar(ag.index, ag.values, color=PALETTE[2])
ax.set_xlabel("年龄段"); ax.set_ylabel("就诊量"); ax.set_title("图3 住院患者年龄段分布（条形图）")
plt.setp(ax.get_xticklabels(), rotation=35); save(fig, "fig03_年龄段分布_条形图.png")

# ---------- fig04 模板复现：直方图（住院天数分布） ----------
fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(df["time_in_hospital"], bins=range(1, 16), color=PALETTE[0], edgecolor="white")
ax.set_xlabel("住院天数（天）"); ax.set_ylabel("频数"); ax.set_title("图4 住院天数分布（直方图）"); save(fig, "fig04_住院天数分布_直方图.png")

# ---------- fig05 模板复现：堆积柱状图（性别 × 再入院情况） ----------
t = pd.crosstab(df["gender"].map({"Male": "男性", "Female": "女性"}), df["readmitted"].map({"NO": "未再入院", ">30": "30天后", "<30": "30天内"}))
t = t[["未再入院", "30天后", "30天内"]]
fig, ax = plt.subplots(figsize=(6.5, 4.2))
bottom = np.zeros(len(t))
for i, col in enumerate(t.columns):
    ax.bar(t.index, t[col], bottom=bottom, label=col, color=PALETTE[i])
    bottom += t[col].values
ax.set_ylabel("人次"); ax.set_title("图5 性别 × 再入院情况（堆积柱状图）"); ax.legend(); save(fig, "fig05_性别再入院_堆积柱状图.png")

# ---------- fig06 模板复现：折线图（各年龄段30天再入院率） ----------
r = df.groupby("age_group")["readmit_30d"].mean().reindex(age_order) * 100
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.plot(r.index, r.values, marker="o", lw=2, color=PALETTE[1])
for i, v in enumerate(r.values):
    ax.annotate(f"{v:.1f}", (i, v), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8)
ax.set_xlabel("年龄段"); ax.set_ylabel("30天再入院率（%）"); ax.set_title("图6 各年龄段30天再入院率（折线图）")
plt.setp(ax.get_xticklabels(), rotation=35); save(fig, "fig06_年龄再入院率_折线图.png")

# ---------- fig07 模板复现：横向条形图（诊断大类就诊量 TOP8） ----------
top = df["diag_1_group"].value_counts().head(8).sort_values()
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.barh(top.index, top.values, color=PALETTE[0])
for i, v in enumerate(top.values):
    ax.text(v + 150, i, str(v), va="center", fontsize=8)
ax.set_xlabel("就诊量"); ax.set_title("图7 主诊断大类就诊量 TOP8（横向条形图）"); save(fig, "fig07_诊断大类就诊量_横向条形图.png")

# ---------- fig08 模板复现：散点图（年医疗利用次数 × 再入院率） ----------
u = df.groupby("utilization").agg(就诊量=("encounter_id", "count"), 再入院率=("readmit_30d", "mean")).reset_index()
u = u[u["utilization"] <= 10]
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.scatter(u["utilization"], u["再入院率"] * 100, s=u["就诊量"] / 60, alpha=0.6, color=PALETTE[4])
ax.set_xlabel("入院前一年门诊+急诊+住院次数"); ax.set_ylabel("30天再入院率（%）")
ax.set_title("图8 医疗资源利用强度与再入院（气泡散点图）"); save(fig, "fig08_资源利用与再入院_散点图.png")

# ---------- fig09 模板复现：气泡图（用药数量 × 住院天数，颜色=年龄段） ----------
smp = df.sample(3000, random_state=42)
fig, ax = plt.subplots(figsize=(7.5, 4.5))
sc = ax.scatter(smp["num_medications"], smp["time_in_hospital"],
                s=smp["num_lab_procedures"] / 2, c=smp["age_mid"], cmap="viridis", alpha=0.45)
ax.set_xlabel("同期用药数量（种）"); ax.set_ylabel("住院天数（天）")
ax.set_title("图9 用药数量与住院天数（气泡大小=化验项数，颜色=年龄）")
fig.colorbar(sc, label="年龄中位数"); save(fig, "fig09_用药与住院天数_气泡图.png")

# ---------- fig10 模板复现：雷达图（诊断大类多维指标归一化） ----------
radar_groups = ["循环系统", "呼吸系统", "消化系统", "糖尿病", "泌尿生殖系统", "损伤中毒"]
met = df[df["diag_1_group"].isin(radar_groups)].groupby("diag_1_group").agg(
    就诊量=("encounter_id", "count"), 平均住院日=("time_in_hospital", "mean"),
    再入院率=("readmit_30d", "mean"), 平均用药=("num_medications", "mean"),
    平均化验=("num_lab_procedures", "mean"))
norm = (met - met.min()) / (met.max() - met.min())  # 0-1 归一化便于雷达展示
labels = ["就诊量", "平均住院日", "再入院率", "平均用药", "平均化验"]
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist(); angles += angles[:1]
fig, ax = plt.subplots(figsize=(6.5, 6), subplot_kw={"polar": True})
for i, (name, row) in enumerate(norm.iterrows()):
    vals = row.tolist() + row.tolist()[:1]
    ax.plot(angles, vals, label=name, color=PALETTE[i], lw=1.6)
    ax.fill(angles, vals, color=PALETTE[i], alpha=0.08)
ax.set_xticks(angles[:-1]); ax.set_xticklabels(labels)
ax.set_title("图10 主要诊断大类多维指标雷达图（0-1归一化）", pad=20)
ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.1), fontsize=8); save(fig, "fig10_诊断大类多维_雷达图.png")

# ---------- fig11 模板复现：双轴图（世行卫生支出 + 同比增速） ----------
wb = pd.read_csv(CLEAN / "us_health_expenditure.csv")
wb["增速%"] = wb["expenditure_usd"].pct_change() * 100
fig, ax1 = plt.subplots(figsize=(8, 4.5))
ax1.bar(wb["year"], wb["expenditure_usd"], color=PALETTE[0], alpha=0.85, label="人均卫生支出（美元）")
ax2 = ax1.twinx()
ax2.plot(wb["year"], wb["增速%"], color=PALETTE[1], marker=".", lw=1.8, label="同比增速（%）")
ax1.set_ylabel("人均卫生支出（美元）"); ax2.set_ylabel("同比增速（%）")
ax1.set_title("图11 美国人均卫生支出及增速（双轴图，世界银行数据）")
h1, l1 = ax1.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=8); save(fig, "fig11_卫生支出增速_双轴图.png")

# ---------- fig12 模板复现：相关系数热力图 ----------
cols = ["time_in_hospital", "num_lab_procedures", "num_procedures", "num_medications",
        "number_outpatient", "number_emergency", "number_inpatient", "number_diagnoses", "age_mid", "readmit_30d"]
cn = ["住院天数", "化验项数", "操作项数", "用药数量", "年门诊", "年急诊", "年住院", "诊断数", "年龄", "再入院30天"]
corr = df[cols].corr()
fig, ax = plt.subplots(figsize=(7.5, 6.2))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
            xticklabels=cn, yticklabels=cn, square=True, cbar_kws={"shrink": .8}, annot_kws={"size": 7})
ax.set_title("图12 核心数值指标相关系数热力图"); save(fig, "fig12_相关系数_热力图.png")

# ---------- fig13 业务模型：ABC 帕累托图 ----------
abc = pd.read_csv(TAB / "model1_abc_pareto.csv", index_col=0)
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.bar(abc.index, abc["住院天数占比%"], color=[PALETTE[0] if c == "A" else (PALETTE[1] if c == "B" else PALETTE[7]) for c in abc["ABC类别"]])
ax2 = ax.twinx()
ax2.plot(abc.index, abc["累计占比%"], color=PALETTE[4], marker="o", lw=2, label="累计占比")
ax2.axhline(70, ls="--", color="gray", lw=1); ax2.axhline(90, ls="--", color="gray", lw=1)
ax.set_ylabel("住院天数占比（%）"); ax2.set_ylabel("累计占比（%）")
ax.set_title("图13 诊断大类住院天数 ABC 帕累托分析")
plt.setp(ax.get_xticklabels(), rotation=30); save(fig, "fig13_ABC帕累托_模型图.png")

# ---------- fig14 业务模型：波士顿矩阵四象限 ----------
bcg = pd.read_csv(TAB / "model2_bcg_matrix.csv", index_col=0)
x_mid, y_mid = bcg["就诊量份额%"].median(), bcg["再入院率"].median() * 100
fig, ax = plt.subplots(figsize=(8, 5))
ax.axvline(x_mid, color="gray", ls="--", lw=1); ax.axhline(y_mid, color="gray", ls="--", lw=1)
ax.scatter(bcg["就诊量份额%"], bcg["再入院率"] * 100, s=bcg["平均住院天数"] * 120, alpha=0.55, color=PALETTE[0])
for name, r in bcg.iterrows():
    ax.annotate(name, (r["就诊量份额%"], r["再入院率"] * 100), fontsize=8,
                xytext=(5, 5), textcoords="offset points")
# 象限名称固定在绘图区四角，避免与散点标签重叠
ax.text(0.97, 0.97, "问题类", transform=ax.transAxes, fontsize=11, color=PALETTE[3], ha="right", va="top")
ax.text(0.03, 0.97, "瘦狗类", transform=ax.transAxes, fontsize=11, color=PALETTE[7], ha="left", va="top")
ax.text(0.97, 0.03, "明星类", transform=ax.transAxes, fontsize=11, color=PALETTE[2], ha="right", va="bottom")
ax.text(0.03, 0.03, "金牛类", transform=ax.transAxes, fontsize=11, color=PALETTE[1], ha="left", va="bottom")
ax.set_xlabel("就诊量份额（%）"); ax.set_ylabel("30天再入院率（%）")
ax.set_title("图14 诊断大类波士顿矩阵（气泡=平均住院日，虚线=中位数分界）"); save(fig, "fig14_波士顿矩阵_模型图.png")

# ---------- fig15 业务模型：同期群再入院热力图 ----------
cohort = pd.read_csv(TAB / "model3_cohort_readmit_rate.csv", index_col=0)
cnt = pd.read_csv(TAB / "model3_cohort_counts.csv", index_col=0)
fig, ax = plt.subplots(figsize=(6.5, 5.2))
sns.heatmap(cohort * 100, annot=cnt.values, fmt=".0f", cmap="Reds",
            xticklabels=cohort.columns, yticklabels=cohort.index,
            cbar_kws={"label": "30天再入院率（%）"}, annot_kws={"size": 7})
ax.set_xlabel("入院前一年住院次数"); ax.set_ylabel("年龄队列")
ax.set_title("图15 年龄×既往住院同期群再入院热力图（格内数字=样本量）"); save(fig, "fig15_同期群再入院_模型图.png")

# ---------- fig16 业务模型：关联规则 lift 散点 ----------
rules = pd.read_csv(TAB / "model4_apriori_rules.csv")
rules = rules[~rules["consequents"].isin(["A1C异常", "A1C已检测"])]  # 剔除同义规则，保留业务规则
rules = rules.sort_values("lift", ascending=False).reset_index(drop=True)
fig, ax = plt.subplots(figsize=(9.5, 5.2))
fig.subplots_adjust(right=0.58)
ax.scatter(rules["support"], rules["confidence"] * 100, s=rules["lift"] * 200, alpha=0.55, color=PALETTE[4])
# 气泡内放序号，右侧图例表列出规则全文，避免密集区标签互相覆盖
legend_lines = []
for i, r in rules.iterrows():
    ax.text(r["support"], r["confidence"] * 100, str(i + 1), ha="center", va="center",
            fontsize=8, color="white", fontweight="bold")
    legend_lines.append(f"{'%2d' % (i+1)}. {r['antecedents']}→{r['consequents']}"
                        f"  (lift={r['lift']:.2f})")
fig.text(0.61, 0.95, "关联规则一览", fontsize=10, fontweight="bold", va="top")
fig.text(0.61, 0.88, "\n".join(legend_lines), fontsize=8.5, va="top", linespacing=1.9)
ax.set_xlabel("支持度"); ax.set_ylabel("置信度（%）"); ax.margins(x=0.15)
ax.set_title("图16 临床标志关联规则（气泡大小=Lift，数字见右侧列表）"); save(fig, "fig16_关联规则_模型图.png")

# ---------- fig17 业务模型：诊疗路径漏斗 ----------
fun = pd.read_csv(TAB / "model5_funnel.csv")
fig, ax = plt.subplots(figsize=(7.5, 4.5))
maxv = fun["人数"].max()
for i, r in fun.iterrows():
    w = r["人数"] / maxv
    ax.barh(len(fun) - 1 - i, w, left=(1 - w) / 2, height=0.62, color=PALETTE[i % len(PALETTE)])
    ax.text(0.5, len(fun) - 1 - i, f"{r['阶段']}  {r['人数']:,}人（{r['占首阶段%']}%）",
            ha="center", va="center", fontsize=9)
ax.set_xlim(0, 1); ax.axis("off")
ax.set_title("图17 糖尿病住院诊疗路径漏斗（HbA1c检测→调药→未再入院）"); save(fig, "fig17_诊疗路径漏斗_模型图.png")

# ---------- fig18 业务模型：SARIMA 预测（95%置信区间 + 回测） ----------
hist = pd.read_csv(CLEAN / "us_health_expenditure.csv")
bt = pd.read_csv(TAB / "model6_sarima_backtest.csv")
fc = pd.read_csv(TAB / "model6_sarima_forecast.csv")
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.plot(hist["year"], hist["expenditure_usd"], color=PALETTE[0], lw=1.8, label="历史实际值")
ax.plot(bt["year"], bt["回测预测值"], "s--", color=PALETTE[1], ms=5, label="回测预测（末5年）")
ax.plot(fc["year"], fc["预测值(美元/人)"], "^--", color=PALETTE[3], ms=5, label="未来预测（SARIMA）")
ax.fill_between(fc["year"], fc["95%置信下界"], fc["95%置信上界"], color=PALETTE[3], alpha=0.15, label="95%置信区间")
ax.set_xlabel("年份"); ax.set_ylabel("人均卫生支出（美元）")
ax.set_title("图18 SARIMA 美国人均卫生支出预测（回测MAPE见表）")
ax.legend(fontsize=8); save(fig, "fig18_SARIMA支出预测_模型图.png")

print("\n全部图表生成完毕：", len(list(FIG.glob("*.png"))), "张")
