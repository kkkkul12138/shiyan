仓库链接（公开仓库，提交时请替换为实际地址）：

https://gitee.com/<你的用户名>/diabetes-hospital-analysis

或 GitHub：https://github.com/<你的用户名>/diabetes-hospital-analysis

仓库目录结构：

```
diabetes-hospital-analysis/
├── data/
│   ├── raw/          # 原始数据（UCI官方ZIP解压CSV、世行API JSON）+ 下载说明
│   └── clean/        # 清洗后数据（CSV/JSON/SQLite三格式）
├── scripts/
│   ├── 01_load.py    # 数据加载与概览
│   ├── 02_clean.py   # 清洗治理与导出
│   ├── 03_analysis.py# 六模型分析
│   ├── 04_visuals.py # 18张图（模板复现12+业务模型6）
│   └── 05_dashboard.py# 交互大屏生成
├── outputs/
│   ├── figures/      # fig01–fig18 PNG + dashboard.html + 大屏截图
│   └── tables/       # 模型结果表与KPI汇总
├── docs/             # 期末论文与合规声明
├── assets/           # echarts.min.js（大屏离线内联用）
├── requirements.txt
└── run_all.py        # 一键复现入口
```
