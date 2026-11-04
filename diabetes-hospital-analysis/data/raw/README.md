# 原始数据获取说明（白名单渠道，非爬虫）

获取日期：2026-10-29

## 1. UCI 糖尿病住院数据集（主数据源）

- 数据集页面：https://archive.ics.uci.edu/dataset/296/diabetes+130+us+hospitals+for+years+1999+2008
- 下载方式：页面 "Download" 按钮指向的官方静态链接（一次性 ZIP 文件下载）：
  `https://archive.ics.uci.edu/static/public/296/diabetes+130-us+hospitals+for+years+1999-2008.zip`
- 解压得到 `diabetic_data.csv`（101,766 条 × 50 列）与 `IDS_mapping.csv`（编码映射表）
- License：CC BY 4.0；引用：Clore J, Cios K, DeShazo J, Strack B. (2014). Diabetes 130-US Hospitals for Years 1999-2008. UCI ML Repository. DOI:10.24432/C5230J.

## 2. 世界银行卫生支出数据（辅助数据源）

- 指标：Current health expenditure per capita (current US$)，代码 SH.XPD.CHEX.PC.CD
- 下载方式：世界银行官方数据 API：
  `https://api.worldbank.org/v2/country/USA/indicator/SH.XPD.CHEX.PC.CD?format=json&per_page=2000`
- 美国 2000—2023 年共 24 个年度观测值
- License：CC-BY 4.0，引用要求注明 "Source: World Bank (2026)"

本目录下 `uci_diabetes_hospitals.zip`、`diabetic_data.csv`、`IDS_mapping.csv`、`worldbank_US_health_expenditure.json` 为 2026-10-29 获取的原始文件未修改副本。
