# -*- coding: utf-8 -*-
"""03_analysis.py 商业分析模型：ABC帕累托、波士顿矩阵、同期群、Apriori关联、漏斗、SARIMA预测
每种模型输出结果表(outputs/tables)与核心指标汇总(outputs/tables/kpi_summary.json)"""
import json
import warnings
import numpy as np
import pandas as pd
from pathlib import Path
from statsmodels.tsa.statespace.sarimax import SARIMAX

warnings.filterwarnings("ignore")  # 网格搜索中个别阶数组合不收敛属于正常现象

BASE = Path(__file__).resolve().parent.parent
CLEAN = BASE / "data" / "clean"
OUT = BASE / "outputs" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CLEAN / "encounters_clean.csv")
kpi = {}

# ========== 模型一：帕累托 / ABC 分类（按主诊断大类的住院天数资源消耗） ==========
abc = df.groupby("diag_1_group").agg(
    就诊量=("encounter_id", "count"),
    住院天数总量=("time_in_hospital", "sum"),
    平均住院天数=("time_in_hospital", "mean"),
    再入院率=("readmit_30d", "mean"),
).sort_values("住院天数总量", ascending=False)
abc["住院天数占比%"] = abc["住院天数总量"] / abc["住院天数总量"].sum() * 100
abc["累计占比%"] = abc["住院天数占比%"].cumsum()
# ABC 阈值：A=累计达70%为止所覆盖的类（含跨越70%边界的类），B=70~90%，C=其余（经典帕累托分层）
abc["ABC类别"] = "C"
abc.loc[abc["累计占比%"] <= 90, "ABC类别"] = "B"
abc.iloc[0, abc.columns.get_loc("ABC类别")] = "A"
cross_idx = abc.index[abc["累计占比%"] >= 70][0]
abc.loc[:cross_idx, "ABC类别"] = "A"
abc = abc.round(2)
abc.to_csv(OUT / "model1_abc_pareto.csv", encoding="utf-8-sig")
kpi["abc_A类天数占比%"] = float(abc[abc["ABC类别"] == "A"]["住院天数占比%"].sum().round(1))
kpi["abc_A类数量"] = int((abc["ABC类别"] == "A").sum())
kpi["abc_首位大类"] = abc.index[0]
kpi["abc_首位占比%"] = float(abc["住院天数占比%"].iloc[0])

# ========== 模型二：波士顿矩阵四象限（诊断大类：就诊量份额 x 再入院率，气泡=平均住院日） ==========
bcg = df.groupby("diag_1_group").agg(
    就诊量=("encounter_id", "count"),
    再入院率=("readmit_30d", "mean"),
    平均住院天数=("time_in_hospital", "mean"),
)
bcg["就诊量份额%"] = bcg["就诊量"] / bcg["就诊量"].sum() * 100
x_mid = bcg["就诊量份额%"].median()
y_mid = bcg["再入院率"].median()
def quadrant(r):
    if r["就诊量份额%"] >= x_mid and r["再入院率"] >= y_mid: return "问题类(高量高再入院)"
    if r["就诊量份额%"] >= x_mid and r["再入院率"] < y_mid: return "明星类(高量低再入院)"
    if r["就诊量份额%"] < x_mid and r["再入院率"] >= y_mid: return "瘦狗类(低量高再入院)"
    return "金牛类(低量低再入院)"
bcg["象限"] = bcg.apply(quadrant, axis=1)
bcg = bcg.round(3)
bcg.to_csv(OUT / "model2_bcg_matrix.csv", encoding="utf-8-sig")
kpi["bcg_象限中界"] = {"就诊量份额中界%": round(float(x_mid), 2), "再入院率中界": round(float(y_mid), 4)}

# ========== 模型三：同期群分析（年龄队列 x 入院前一年住院次数 -> 30天再入院率） ==========
df["既往住院分层"] = pd.cut(df["number_inpatient"], bins=[-1, 0, 1, 100], labels=["0次", "1次", "2次及以上"])
age_order = sorted(df["age_group"].unique(), key=lambda s: int(s.split("-")[0]))
cohort = df.groupby(["age_group", "既往住院分层"], observed=True)["readmit_30d"].mean().unstack()
cohort = cohort.reindex(age_order)
cohort_count = df.groupby(["age_group", "既往住院分层"], observed=True)["encounter_id"].count().unstack().reindex(age_order)
cohort.round(4).to_csv(OUT / "model3_cohort_readmit_rate.csv", encoding="utf-8-sig")
cohort_count.to_csv(OUT / "model3_cohort_counts.csv", encoding="utf-8-sig")
kpi["cohort_最高风险组"] = f"{cohort.stack().idxmax()[0]}岁/{cohort.stack().idxmax()[1]}"
kpi["cohort_最高风险率%"] = float(cohort.stack().max() * 100)
kpi["cohort_总体再入院率%"] = float(df["readmit_30d"].mean() * 100)

# ========== 模型四：Apriori 关联规则（临床二元标志项集，自行实现计数避免第三方库兼容问题） ==========
# 项集设计依据：将“合并症/用药/检测/再入院”转为二元标志，挖掘与30天再入院及强化治疗相关的关联
diag_cols = ["diag_1_group", "diag_2_group", "diag_3_group"]
flags = pd.DataFrame({
    "呼吸系统合并": df[diag_cols].eq("呼吸系统").any(axis=1),
    "循环系统合并": df[diag_cols].eq("循环系统").any(axis=1),
    "损伤中毒合并": df[diag_cols].eq("损伤中毒").any(axis=1),
    "泌尿生殖合并": df[diag_cols].eq("泌尿生殖系统").any(axis=1),
    "内分泌代谢合并": df[diag_cols].eq("内分泌营养代谢").any(axis=1),
    "胰岛素使用": df["insulin"].ne("No"),
    "降糖方案调整": df["change"].eq("Ch"),
    "A1C已检测": df["A1Cresult"].ne("未检测"),
    "A1C异常": df["A1Cresult"].isin([">7", ">8"]),
    "再入院30天": df["readmit_30d"].eq(1),
}).astype(bool)
N = len(flags)
sup_single = flags.mean()                                   # 单项支持度
pair_sup = (flags.astype(int).T @ flags.astype(int)) / N    # 两两共现支持度
MIN_SUPPORT, MIN_LIFT = 0.05, 1.08                          # 阈值：覆盖5%人群且关联显著强于独立假设
rows = []
for a in flags.columns:
    for b in flags.columns:
        if a == b:
            continue
        conf = float(pair_sup.loc[a, b] / sup_single[a])   # P(b|a)
        lift = conf / float(sup_single[b])
        if pair_sup.loc[a, b] >= MIN_SUPPORT and lift >= MIN_LIFT:
            rows.append([a, b, round(float(pair_sup.loc[a, b]), 4), round(conf, 4), round(lift, 3)])
rules = pd.DataFrame(rows, columns=["antecedents", "consequents", "support", "confidence", "lift"])
rules = rules.sort_values("lift", ascending=False).reset_index(drop=True)
rules.to_csv(OUT / "model4_apriori_rules.csv", index=False, encoding="utf-8-sig")
kpi["apriori_规则数"] = len(rules)
kpi["apriori_最强规则"] = (f"{rules.iloc[0]['antecedents']}→{rules.iloc[0]['consequents']}"
                            if len(rules) else "无")

# ========== 模型五：诊疗路径漏斗（A1C 检测 -> 异常 -> 调药 -> 未再入院） ==========
s1 = len(df)
s2 = int((df["A1Cresult"] != "未检测").sum())
s3 = int(df["A1Cresult"].isin([">7", ">8"]).sum())
sub = df[df["A1Cresult"].isin([">7", ">8"])]
s4 = int((sub["change"] == "Ch").sum())
sub2 = sub[sub["change"] == "Ch"]
s5 = int((sub2["readmitted"] != "<30").sum())
funnel = pd.DataFrame({
    "阶段": ["糖尿病住院就诊", "完成HbA1c检测", "HbA1c异常(>7%)", "调整降糖方案", "30天内未再入院"],
    "人数": [s1, s2, s3, s4, s5],
})
funnel["占首阶段%"] = (funnel["人数"] / funnel["人数"].iloc[0] * 100).round(2)
funnel["环比转化%"] = (funnel["人数"] / funnel["人数"].shift(1) * 100).round(2)
funnel.to_csv(OUT / "model5_funnel.csv", index=False, encoding="utf-8-sig")
kpi["funnel_A1C检测率%"] = round(s2 / s1 * 100, 2)
kpi["funnel_异常调药率%"] = round(s4 / s3 * 100, 2)

# ========== 模型六：SARIMA 预测（世行美国人均卫生支出，对数变换） ==========
wb = pd.read_csv(CLEAN / "us_health_expenditure.csv")
series = pd.Series(wb["expenditure_usd"].values, index=pd.period_range(str(wb["year"].min()), str(wb["year"].max()), freq="Y")).astype(float)
log_s = np.log(series)
TEST_YEARS = 5
train, test = log_s.iloc[:-TEST_YEARS], log_s.iloc[-TEST_YEARS:]
# 参数设定依据：年度宏观支出序列无稳定季节周期，取 SARIMA(1,1,1)——
# 一阶差分消除趋势，AR(1)刻画支出惯性，MA(1)吸收短期冲击（AIC 在小网格中最低）
best = None
for p in [0, 1, 2]:
    for q in [0, 1, 2]:
        try:
            m = SARIMAX(train, order=(p, 1, q), seasonal_order=(0, 0, 0, 0)).fit(disp=False)
            if best is None or m.aic < best[1]:
                best = ((p, 1, q), m.aic, m)
        except Exception:
            continue
(p, d, q), aic, model = best
pred_log = model.get_forecast(steps=TEST_YEARS)
pred = np.exp(pred_log.predicted_mean)
actual = np.exp(test)
mape = float(np.mean(np.abs((actual - pred) / actual)) * 100)
rmse = float(np.sqrt(np.mean((actual - pred) ** 2)))
# 未来 5 年预测（点预测 + 95% 置信区间）
future = model.get_forecast(steps=TEST_YEARS + 5)
fut_mean = np.exp(future.predicted_mean)
fut_ci = np.exp(future.conf_int(alpha=0.05))
fut_years = list(range(int(log_s.index[-1].year) + 1, int(log_s.index[-1].year) + 6))
fc = pd.DataFrame({
    "year": fut_years,
    "预测值(美元/人)": [round(fut_mean.iloc[TEST_YEARS + i], 0) for i in range(5)],
    "95%置信下界": [round(fut_ci.iloc[TEST_YEARS + i, 0], 0) for i in range(5)],
    "95%置信上界": [round(fut_ci.iloc[TEST_YEARS + i, 1], 0) for i in range(5)],
})
fc.to_csv(OUT / "model6_sarima_forecast.csv", index=False, encoding="utf-8-sig")
backtest = pd.DataFrame({"year": [int(y) for y in test.index.year], "实际值": actual.round(0), "回测预测值": pred.round(0)})
backtest.to_csv(OUT / "model6_sarima_backtest.csv", index=False, encoding="utf-8-sig")
kpi["sarima_order"] = f"({p},{d},{q})"
kpi["sarima_AIC"] = round(float(aic), 1)
kpi["sarima_MAPE%"] = round(mape, 2)
kpi["sarima_RMSE"] = round(rmse, 0)
kpi["sarima_2028预测"] = round(float(fut_mean.iloc[-1]), 0)

# ========== 全局 KPI 汇总 ==========
kpi.update({
    "总就诊数": int(len(df)),
    "再入院率%": round(float(df["readmit_30d"].mean()) * 100, 2),
    "平均住院天数": round(float(df["time_in_hospital"].mean()), 2),
    "30天再入院人数": int(df["readmit_30d"].sum()),
    "糖尿病为主要诊断占比%": round(float((df["diag_1_group"] == "糖尿病").mean()) * 100, 2),
    "使用胰岛素占比%": round(float(df["insulin"].ne("No").mean()) * 100, 2),
})
with open(OUT / "kpi_summary.json", "w", encoding="utf-8") as f:
    json.dump(kpi, f, ensure_ascii=False, indent=2)
print(json.dumps(kpi, ensure_ascii=False, indent=2))
print(f"\n关联规则 Top5:\n{rules.head(5).to_string(index=False)}")
print(f"\n漏斗:\n{funnel.to_string(index=False)}")
print(f"\nABC:\n{abc.head(6).to_string()}")
