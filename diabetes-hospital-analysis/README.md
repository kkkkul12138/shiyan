# 糖尿病住院患者再入院风险与资源配置分析

《商业数据分析》期末大作业——基于 UCI 糖尿病住院数据（主源）与世界银行卫生支出数据（辅源）的商业数据分析全链路项目：合规获取 → 清洗治理 → 六模型分析 → 18 张 Python 图表 → Pyecharts 交互大屏 → 商业建议。

## 数据来源与合规声明

| 角色 | 数据源 | 获取方式（白名单） | 获取日期 | License |
| --- | --- | --- | --- | --- |
| 主数据源 | UCI ML Repository: Diabetes 130-US Hospitals for Years 1999-2008 (DOI:10.24432/C5230J) | 数据集页面官方静态下载链接（ZIP） | 2026-10-29 | CC BY 4.0 |
| 辅助数据源 | 世界银行开放数据：Current health expenditure per capita (SH.XPD.CHEX.PC.CD) | 官方数据 API（api.worldbank.org）JSON 下载 | 2026-10-29 | CC-BY 4.0 |

- 本项目**全程未使用爬虫**（无 Scrapy/Selenium/requests 网页解析/模拟登录），仅使用上表白名单渠道；
- 原始文件完整保存于 `data/raw/`，可复验；
- 数据为去标识化历史运营数据，不含直接身份信息；
- 引用格式见论文参考文献 [1][3]。

## 一键复现

```bash
pip install -r requirements.txt
python run_all.py        # 依次执行 01_load → 02_clean → 03_analysis → 04_visuals → 05_dashboard
```

说明：`scripts/01_load.py` 需要 `data/raw/` 下已存在原始文件（原始文件随仓库提交）；若需重新下载，见 `data/raw/README.md`。

## 目录结构

```
├── data/
│   ├── raw/            # 原始数据 + 下载说明
│   └── clean/          # 清洗后数据（CSV / JSON / SQLite）
├── scripts/
│   ├── 01_load.py      # 数据加载与概览
│   ├── 02_clean.py     # 清洗治理与三格式导出
│   ├── 03_analysis.py  # 六模型：ABC/波士顿/同期群/Apriori/漏斗/SARIMA
│   ├── 04_visuals.py   # fig01–fig18（模板复现12 + 业务模型6）
│   └── 05_dashboard.py # 交互大屏（echarts 已内联，离线可开）
├── outputs/
│   ├── figures/        # 18 张 PNG + dashboard.html + 大屏截图
│   └── tables/         # 模型结果表 / KPI 汇总 / 清洗报告
├── docs/               # 期末论文（Word）、合规声明、章节底稿
├── assets/echarts.min.js
├── requirements.txt
└── run_all.py
```

## 核心结果速览

- 样本：清洗去重后 68,404 名糖尿病患者；30 天再入院率 9.07%，平均住院 4.29 天
- ABC：前 5 个诊断大类消耗 70.51% 住院天数（循环系统单类 30.04%）
- 漏斗：HbA1c 检测率仅 18.15%，为诊疗路径最大瓶颈
- 同期群：既往年住院 ≥2 次人群再入院率 20%–38%（基线约 8%）
- SARIMA(1,1,0)：回测 MAPE=6.16%，预测 2028 年人均卫生支出约 $14,043
- 大屏：`outputs/figures/dashboard.html`，13 组件，支持点击柱图下钻诊断构成

## 图表索引

fig01–fig12 为模板复现类（分组柱/饼/条形/直方/堆积柱/折线/横条/散点/气泡/雷达/双轴/热力），fig13–fig18 为业务模型类（ABC 帕累托/波士顿矩阵/同期群热力/关联规则/漏斗/SARIMA 预测），完整对照表见论文附录 C。

## AI 使用披露

本项目使用 AI 编程助手（Kimi/WorkBuddy）辅助代码框架搭建、绘图代码编写与论文初稿润色；数据获取、模型选型、阈值设定与结论解读由作者独立完成，全部代码经真实运行验证，详见论文 7.3 节。
