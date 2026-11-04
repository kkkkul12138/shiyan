# -*- coding: utf-8 -*-
"""run_all.py 一键复现入口：依次执行加载、清洗、分析、可视化、大屏五个脚本"""
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
SCRIPTS = BASE / "scripts"

STEPS = ["01_load.py", "02_clean.py", "03_analysis.py", "04_visuals.py", "05_dashboard.py"]

for s in STEPS:
    print(f"\n===== 执行 {s} =====")
    r = subprocess.run([sys.executable, str(SCRIPTS / s)], cwd=BASE)
    if r.returncode != 0:
        print(f"{s} 执行失败，流程中止")
        sys.exit(r.returncode)
print("\n全部完成：图表见 outputs/figures/，大屏打开 outputs/figures/dashboard.html")
