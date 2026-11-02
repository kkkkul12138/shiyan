# -*- coding: utf-8 -*-
"""01_load.py 数据加载与概览：读取原始文件，输出数据字典与概览表"""
import json
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RAW = BASE / "data" / "raw"
OUT = BASE / "outputs" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

# UCI 糖尿病住院主表（官方 ZIP 内 CSV）
df = pd.read_csv(RAW / "diabetic_data.csv")
print(f"主表 diabetic_data: {df.shape[0]} 行 x {df.shape[1]} 列")

# 字段缺失率概览（写入表格，供论文数据治理章节引用）
na = pd.DataFrame({
    "字段": df.columns,
    "类型": [str(df[c].dtype) for c in df.columns],
    "缺失数": [int(df[c].isna().sum()) for c in df.columns],
    "缺失率%": [round(float(df[c].isna().mean()) * 100, 2) for c in df.columns],
    "唯一值数": [int(df[c].nunique()) for c in df.columns],
})
na.to_csv(OUT / "schema_overview.csv", index=False, encoding="utf-8-sig")
print(na[na["缺失率%"] > 0].sort_values("缺失率%", ascending=False).head(10).to_string(index=False))

# IDS 映射表（admission_type / discharge_disposition / admission_source 三段）
mapping = pd.read_csv(RAW / "IDS_mapping.csv")
print(f"\nIDS_mapping: {mapping.shape}")

# 世界银行辅助表（官方 API JSON）
with open(RAW / "worldbank_US_health_expenditure.json", encoding="utf-8") as f:
    wb = json.load(f)
wb_df = pd.DataFrame(wb[1])
wb_df = wb_df[["date", "value"]].dropna()
wb_df.columns = ["year", "expenditure_usd"]
wb_df["year"] = wb_df["year"].astype(int)
wb_df["expenditure_usd"] = wb_df["expenditure_usd"].astype(float)
wb_df = wb_df.sort_values("year").reset_index(drop=True)
wb_df.to_csv(OUT / "wb_expenditure_overview.csv", index=False, encoding="utf-8-sig")
print(f"\n世行卫生支出序列: {wb_df['year'].min()}-{wb_df['year'].max()}, 共 {len(wb_df)} 年, "
      f"最新值 {wb_df['expenditure_usd'].iloc[-1]:.0f} 美元/人")
