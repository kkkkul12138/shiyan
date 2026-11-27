# -*- coding: utf-8 -*-

import os

import matplotlib
import numpy as np
import openpyxl

# 兼容脚本 / Jupyter 两种运行环境
if os.environ.get("DISPLAY", "") == "" and matplotlib.get_backend() != "Agg":
    try:
        matplotlib.use("Agg")
    except Exception:
        pass

import matplotlib.pyplot as plt

# Windows 黑体，解决中文方框
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# ==============================================================================
# 0. 全局配置
# ==============================================================================
EXCEL_PATH = r"C:\Users\陈汝嘉\Desktop\专业课专业\数据分析及可视化\第四章 销售看板参考.xlsx"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

# 看板配色（从原图XML提取）
C_KPI, C_AREA, C_EXP, C_TREND = "#7BBDD5", "#7BBDD5", "#FC6C9D", "#4A5BD1"
C_CATE = ["#FC6C9D", "#4A5BD1", "#F6A576"]
C_GRAY, C_EDGE = "#EDF1F7", "#2C3560"


# ==============================================================================
# 1. 通用工具
# ==============================================================================
def save_and_show(filename):
    """保存 PNG 并显示。"""
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, filename)
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    print(f"    已保存 -> {path}")
    plt.show()
    plt.close()


# ==============================================================================
# 2. 读取看板图表统计数据源（与原图完全同源）
# ==============================================================================
wb = openpyxl.load_workbook(EXCEL_PATH, data_only=True)
ws = wb["统计数据"]


def read_two(col_c, col_v, r1, r2):
    return ([ws.cell(row=r, column=col_c).value for r in range(r1, r2 + 1)],
            [ws.cell(row=r, column=col_v).value for r in range(r1, r2 + 1)])


region_cats, region_vals = read_two(4, 5, 9, 14)       # 区域销量
express_cats, express_vals = read_two(4, 5, 18, 23)    # 快递公司销量
mom_cats, mom_vals = read_two(10, 11, 9, 10)           # 销量环比
cate_cats, cate_vals = read_two(10, 11, 13, 15)        # 产品类别销量
mon_cats, mon_vals = read_two(10, 11, 18, 29)          # 各月销售额(万)
# 商品销售额 TOP3 实体数据在 W3:Z5（X=产品名称, Y=销售额(万)）；
# W11:Z13 是看板里的装饰辅助列（300/100/100），不含真实信息
top3_names = [ws.cell(row=r, column=24).value for r in range(3, 6)]
top3_sales = [ws.cell(row=r, column=25).value for r in range(3, 6)]
kpi_names = [ws.cell(row=r, column=4).value for r in range(27, 31)]   # 推广/其他/人工/产品
kpi_pcts = [ws.cell(row=r, column=6).value for r in range(27, 31)]    # 占比
profit_pct = ws.cell(row=3, column=14).value                          # 利润率


# ==============================================================================
# 3. 图1-4：成本占比 KPI 环形图（推广/其他/人工/产品）
# ==============================================================================
for i, (name, pct) in enumerate(zip(kpi_names, kpi_pcts), start=1):
    plt.figure(figsize=(3.2, 3.2), dpi=100)
    plt.pie([pct, 1 - pct], colors=[C_KPI, C_GRAY], startangle=90, counterclock=False,
            wedgeprops={"width": 0.15, "edgecolor": "white", "linewidth": 2})
    plt.text(0, 0.06, f"{pct*100:.1f}%", ha="center", va="center",
             fontsize=15, fontweight="bold")
    plt.text(0, -0.30, name, ha="center", va="center", fontsize=10, color="#555555")
    plt.axis("off")
    plt.tight_layout()
    save_and_show(f"{i}_{name}成本占比.png")


# ==============================================================================
# 4. 图5：快递公司销量（纵向柱形图）
# ==============================================================================
plt.figure(figsize=(6.5, 4.5), dpi=100)
bars = plt.bar(express_cats, express_vals, color=C_EXP, edgecolor=C_EDGE,
               linewidth=0.8, width=0.55)
for b, v in zip(bars, express_vals):
    plt.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:,}", ha="center", fontsize=9)
plt.title("快递公司销量", fontsize=14)
plt.ylabel("销量")
plt.ylim(0, max(express_vals) * 1.12)
plt.grid(axis="y", alpha=0.3, linestyle="--")
plt.tight_layout()
save_and_show("5_快递公司销量.png")


# ==============================================================================
# 5. 图6：区域销量（纵向柱形图）
# ==============================================================================
plt.figure(figsize=(6.5, 4.5), dpi=100)
bars = plt.bar(region_cats, region_vals, color=C_AREA, edgecolor=C_EDGE,
               linewidth=0.8, width=0.55)
for b, v in zip(bars, region_vals):
    plt.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:,}", ha="center", fontsize=9)
plt.title("区域销量", fontsize=14)
plt.ylabel("销量")
plt.ylim(0, max(region_vals) * 1.12)
plt.grid(axis="y", alpha=0.3, linestyle="--")
plt.tight_layout()
save_and_show("6_区域销量.png")


# ==============================================================================
# 6. 图7：销量环比（横向柱形图）
# ==============================================================================
plt.figure(figsize=(5.5, 3.2), dpi=100)
bars = plt.barh(mom_cats, mom_vals, color=C_TREND, edgecolor=C_EDGE,
                linewidth=0.8, height=0.45)
for b, v in zip(bars, mom_vals):
    plt.text(v + 3, b.get_y() + b.get_height() / 2, f"{v:,}", va="center", fontsize=9)
plt.title("销量环比（8月 / 9月）", fontsize=13)
plt.xlabel("销量")
plt.xlim(0, max(mom_vals) * 1.15)
plt.grid(axis="x", alpha=0.3, linestyle="--")
plt.tight_layout()
save_and_show("7_销量环比.png")


# ==============================================================================
# 7. 图8：各月销售额（面积图）
# ==============================================================================
plt.figure(figsize=(9, 4.5), dpi=100)
x = np.arange(len(mon_cats))
plt.plot(x, mon_vals, color=C_TREND, linewidth=2, marker="o", markersize=4)
plt.fill_between(x, mon_vals, color=C_TREND, alpha=0.30)
plt.xticks(x, mon_cats)
for i, v in enumerate(mon_vals):
    plt.text(i, v + 1.5, f"{v:.0f}", ha="center", fontsize=8, color="#555555")
plt.title("各月销售额", fontsize=14)
plt.ylabel("销售额（万元）")
plt.ylim(0, max(mon_vals) * 1.15)
plt.grid(axis="y", alpha=0.3, linestyle="--")
plt.tight_layout()
save_and_show("8_各月销售额.png")


# ==============================================================================
# 8. 图9：产品类别销量（环形图，显示百分比）
# ==============================================================================
plt.figure(figsize=(6.5, 4.8), dpi=100)
wedges, _, autotexts = plt.pie(cate_vals, labels=None, colors=C_CATE, startangle=90,
                               counterclock=False, autopct="%.1f%%", pctdistance=0.75,
                               wedgeprops={"width": 0.15, "edgecolor": "white",
                                           "linewidth": 1.5})
for t in autotexts:
    t.set_fontsize(9)
plt.title("产品类别销量", fontsize=14)
plt.legend(wedges, [f"{c}  {v:,}" for c, v in zip(cate_cats, cate_vals)],
           loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False, fontsize=10)
plt.axis("equal")
plt.tight_layout()
save_and_show("9_产品类别销量.png")


# ==============================================================================
# 9. 图10：商品销售额（TOP3 排名条形图）
# ==============================================================================
plt.figure(figsize=(7, 3.6), dpi=100)
y = np.arange(len(top3_names))[::-1]     # 排名1在最上面
bars = plt.barh(y, top3_sales, color=C_TREND, edgecolor=C_EDGE, height=0.5)
for b, v in zip(bars, top3_sales):
    plt.text(v + max(top3_sales) * 0.02, b.get_y() + b.get_height() / 2,
             f"{v:.2f}万", va="center", fontsize=9)
plt.yticks(y, top3_names)
plt.xlabel("销售额（万元）")
plt.xlim(0, max(top3_sales) * 1.15)
plt.title("商品销售额（TOP3 排名条形图）", fontsize=14)
plt.grid(axis="x", alpha=0.3, linestyle="--")
plt.tight_layout()
save_and_show("10_商品销售额TOP3.png")


# ==============================================================================
# 10. 图11：利润额占比销售额（环形图）
# ==============================================================================
plt.figure(figsize=(4.5, 4.5), dpi=100)
plt.pie([profit_pct, 1 - profit_pct], colors=[C_EXP, C_GRAY], startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.15, "edgecolor": "white", "linewidth": 2})
plt.text(0, 0.05, f"{profit_pct*100:.1f}%", ha="center", va="center",
         fontsize=16, fontweight="bold")
plt.text(0, -0.32, "利润额占比销售额", ha="center", va="center",
         fontsize=10, color="#555555")
plt.axis("off")
plt.tight_layout()
save_and_show("11_利润率.png")


# ==============================================================================
# 11. 完成
# ==============================================================================
print("=" * 68)
print(f"全部完成，图片已输出至: {OUT_DIR}")
print("=" * 68)
