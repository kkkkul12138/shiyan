# -*- coding: utf-8 -*-
"""02_clean.py 数据清洗与治理：缺失/异常/重复处理、类型统一、指标派生、多表整合、导出"""
import json
import sqlite3
import numpy as np
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw"
CLEAN = BASE / "data" / "clean"
OUT = BASE / "outputs" / "tables"
CLEAN.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42  # 全项目统一样本种子

# ---------- 1. 主表加载与重复值处理 ----------
df = pd.read_csv(RAW / "diabetic_data.csv")
n0 = len(df)

# encounter_id 完全重复行去除（本数据无，防御性处理）
df = df.drop_duplicates(subset="encounter_id")
# 同一患者多次住院记录仅保留首次就诊（避免同一患者信息泄漏，论文中说明依据）
df = df.sort_values("encounter_id").drop_duplicates(subset="patient_nbr", keep="first")
n1 = len(df)

# ---------- 2. 缺失值处理 ----------
# weight(体重) 缺失率约 97%、payer_code 约 40%、medical_specialty 约 49%，缺失过高且非核心分析字段，整列剔除
df = df.drop(columns=["weight", "payer_code", "medical_specialty"])
# race 中 "?" 视为未知类别，保留为独立类别（占比小但保留分布信息）
df["race"] = df["race"].replace("?", "未知")
# max_glu_serum / A1Cresult 中 NaN 与 "None" 均表示未做该项检测，统一为语义明确的“未检测”
df["max_glu_serum"] = df["max_glu_serum"].fillna("未检测").replace("None", "未检测")
df["A1Cresult"] = df["A1Cresult"].fillna("未检测").replace("None", "未检测")
# 诊断编码 "?" 缺失的行去除（无法归入任何诊断大类）
df = df[(df["diag_1"] != "?") & (df["diag_2"] != "?") & (df["diag_3"] != "?")]
n2 = len(df)

# ---------- 3. 异常值与业务无效记录处理 ----------
# 性别未知/无效的记录去除（占比 <0.01%）
df = df[df["gender"].isin(["Male", "Female"])]
# 出院去向为死亡(11,13,14,19,20,21)与临终关怀(23,24)的记录不纳入再入院分析口径
expired = {11, 13, 14, 19, 20, 21, 23, 24}
n_death = int(df["discharge_disposition_id"].isin(expired).sum())
df = df[~df["discharge_disposition_id"].isin(expired)]
n3 = len(df)

# ---------- 4. 类型统一与指标派生 ----------
df["age_mid"] = df["age"].str.extract(r"\[(\d+)-").astype(int) + 5  # 年龄段中位数
df["age_group"] = df["age"].str.replace("[", "").str.replace(")", "").str.replace(",", "-")

ADMISSION_TYPE = {1: "急诊", 2: "急诊", 3: "择期", 4: "择期", 5: "未注明", 6: "未注明", 7: "急诊", 8: "未注明"}
DISCHARGE = {1: "出院回家", 6: "出院回家", 8: "出院回家", 2: "转其他机构", 3: "转其他机构",
             4: "转其他机构", 5: "转其他机构", 22: "转其他机构", 16: "转其他机构", 17: "转其他机构",
             9: "未注明", 12: "未注明", 15: "未注明", 25: "未注明", 26: "未注明", 18: "未注明",
             10: "其他", 27: "其他", 28: "其他", 29: "其他", 30: "其他"}
ADMISSION_SOURCE = {1: "医师转诊", 2: "医师转诊", 3: "医师转诊", 8: "医师转诊",
                    7: "急诊室", 9: "未注明", 17: "未注明", 20: "未注明", 21: "未注明",
                    4: "转院", 5: "转院", 6: "转院", 10: "转院", 18: "转院", 19: "转院",
                    11: "其他", 12: "其他", 13: "其他", 14: "其他", 22: "其他", 25: "其他", 26: "其他"}
df["admission_type"] = df["admission_type_id"].map(ADMISSION_TYPE).fillna("未注明")
df["discharge_type"] = df["discharge_disposition_id"].map(DISCHARGE).fillna("未注明")
df["admission_source"] = df["admission_source_id"].map(ADMISSION_SOURCE).fillna("其他")

def icd9_group(code):
    """ICD-9 编码归并到大类（依据 ICD-9-CM 章节）"""
    if pd.isna(code):
        return "其他"
    c = str(code).strip()
    if c.startswith("V") or c.startswith("E"):
        return "其他"
    try:
        v = float(c)
    except ValueError:
        return "其他"
    if 390 <= v < 460: return "循环系统"
    if 460 <= v < 520: return "呼吸系统"
    if 520 <= v < 580: return "消化系统"
    if 580 <= v < 630: return "泌尿生殖系统"
    if 250 <= v < 251: return "糖尿病"
    if 710 <= v < 740: return "肌肉骨骼"
    if 290 <= v < 320: return "精神类"
    if 140 <= v < 240: return "肿瘤"
    if 240 <= v < 280: return "内分泌营养代谢"
    if v < 140: return "感染寄生虫"
    if 800 <= v < 1000: return "损伤中毒"
    return "其他"

for c in ["diag_1", "diag_2", "diag_3"]:
    df[c + "_group"] = df[c].map(icd9_group)

# 核心派生指标
df["readmit_30d"] = (df["readmitted"] == "<30").astype(int)          # 30天内再入院
df["utilization"] = df["number_outpatient"] + df["number_emergency"] + df["number_inpatient"]  # 年医疗资源利用次数

# ---------- 5. 辅助表（世界银行）整理 ----------
with open(RAW / "worldbank_US_health_expenditure.json", encoding="utf-8") as f:
    wb = json.load(f)
wb_df = pd.DataFrame(wb[1])[["date", "value"]].dropna()
wb_df.columns = ["year", "expenditure_usd"]
wb_df["year"] = wb_df["year"].astype(int)
wb_df["expenditure_usd"] = wb_df["expenditure_usd"].astype(float)
wb_df = wb_df.sort_values("year").reset_index(drop=True)

# ---------- 6. 导出 CSV / JSON / SQLite ----------
df.to_csv(CLEAN / "encounters_clean.csv", index=False, encoding="utf-8-sig")
df.to_json(CLEAN / "encounters_clean.json", orient="records", force_ascii=False)
wb_df.to_csv(CLEAN / "us_health_expenditure.csv", index=False, encoding="utf-8-sig")

con = sqlite3.connect(CLEAN / "medical_analysis.db")
df.to_sql("encounters", con, index=False, if_exists="replace")
wb_df.to_sql("us_health_expenditure", con, index=False, if_exists="replace")
con.close()

# ---------- 7. 清洗报告 ----------
report = pd.DataFrame([
    ["原始记录数", n0], ["去重后(患者唯一)", n1], ["剔除诊断缺失后", n2],
    ["剔除死亡/临终及性别无效后", n3], ["剔除的死亡/临终记录", n_death],
    ["最终样本数", len(df)], ["抽样随机种子", RANDOM_SEED],
], columns=["项目", "数值"])
report.to_csv(OUT / "cleaning_report.csv", index=False, encoding="utf-8-sig")
print(report.to_string(index=False))
print(f"30天再入院率: {df['readmit_30d'].mean()*100:.2f}% | 平均住院天数: {df['time_in_hospital'].mean():.2f}")
print("已导出: CSV / JSON / SQLite")
