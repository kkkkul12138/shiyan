# -*- coding: utf-8 -*-

import os
from collections import Counter

import matplotlib
import numpy as np
import openpyxl

# 兼容脚本 / Jupyter 两种运行环境
if os.environ.get("DISPLAY", "") == "" and matplotlib.get_backend() != "Agg":
    try:
        matplotlib.use("Agg")
    except Exception:
        pass

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


# ==============================================================================
# 0. 全局配置
# ==============================================================================
EXCEL_PATH = r"C:\Users\陈汝嘉\Desktop\专业课专业\数据分析及可视化\第四章 人力资源可视化看板.xlsx"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

# 中文字体：优先微软雅黑，缺 SimHei 也不至于画成方块
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# 统一配色（与第三章保持一致）
C_BORDER = "#1A1E43"   # 描边深蓝
C_BLUE = "#0070C0"     # 主蓝
C_LIGHT = "#00B0F0"    # 浅蓝
C_RED = "#E74E69"      # 强调红
C_GOLD = "#FFC000"     # 金
C_TRACK = "#E8ECF3"    # 跑道底色
C_TEAL = "#11A7AD"
C_PURPLE = "#7030A0"


# ==============================================================================
# 1. 取数层：读取员工明细，各维度统计在这里算好
# ==============================================================================
class DataBook:
    """只读的 Excel 取数封装：A2:H 为员工明细，J/K 为年龄段辅助区。"""

    SHEET = "202203人员基础信息"
    EDU_ORDER = ["专科以下", "专科", "本科", "硕士研究生", "博士研究生"]

    def __init__(self, path=EXCEL_PATH):
        self.path = path
        self.ws = openpyxl.load_workbook(path, data_only=True)[self.SHEET]

    def records(self):
        """员工明细，返回 list of dict（跳过空行）。"""
        recs = []
        for r in range(2, self.ws.max_row + 1):
            if self.ws.cell(row=r, column=1).value is None:
                continue
            recs.append({
                "age": self.ws.cell(row=r, column=2).value,
                "gender": self.ws.cell(row=r, column=3).value,
                "edu": self.ws.cell(row=r, column=4).value,
                "marriage": self.ws.cell(row=r, column=5).value,
                "dept": self.ws.cell(row=r, column=6).value,
                "transfer": self.ws.cell(row=r, column=7).value,
                "age_band": self.ws.cell(row=r, column=8).value,
            })
        return recs

    def age_bands(self):
        """年龄段标签，取辅助区 K3:K7，保持 Excel 里的顺序。"""
        return [self.ws.cell(row=r, column=11).value for r in range(3, 8)]


def count_by(recs, key):
    """按维度计数，返回 Counter。"""
    return Counter(r[key] for r in recs if r[key] is not None)


# ==============================================================================
# 2. 通用工具
# ==============================================================================
def save_and_show(fig, filename):
    """保存 PNG 并显示。"""
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    print(f"    已保存 -> {path}")
    plt.show()
    plt.close(fig)


def as_percent(value, digits=0):
    """小数 -> 百分数字符串，如 0.6 -> '60%'。"""
    if value is None:
        return ""
    return f"{value * 100:.{digits}f}%"


def autopct_int(pct):
    """给 matplotlib 的 autopct 用：它传入的已经是百分数数值。"""
    return f"{pct:.0f}%"


# ==============================================================================
# 3. 图1  公司总人数 KPI 卡
# ==============================================================================
def draw_kpi(db, recs):
    total = len(recs)
    transfer = count_by(recs, "transfer")

    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.axis("off")

    # 外框卡片
    card = mpatches.FancyBboxPatch((0.04, 0.08), 0.92, 0.84,
                                   boxstyle="round,pad=0.02,rounding_size=0.03",
                                   facecolor="#F5F8FC", edgecolor=C_BLUE, linewidth=1.5)
    ax.add_patch(card)

    ax.text(0.5, 0.72, "公司总人数", ha="center", va="center",
            fontsize=15, color="#555555")
    ax.text(0.5, 0.42, f"{total:,}", ha="center", va="center",
            fontsize=44, fontweight="bold", color=C_BLUE)

    sub = f"本月入职 {transfer.get('入职', 0)}    转入 {transfer.get('转入', 0)}    转出 {transfer.get('转出', 0)}"
    ax.text(0.5, 0.16, sub, ha="center", va="center", fontsize=11, color="#777777")

    ax.set_title("公司人员总人数（KPI 卡）", fontsize=14, pad=12)
    fig.tight_layout()
    save_and_show(fig, "1_公司总人数.png")


# ==============================================================================
# 4. 图2  年龄段分布柱形图
# ==============================================================================
def draw_age(db, recs):
    bands = db.age_bands()                       # ['18-24', ..., '40=<']
    cnt = count_by(recs, "age_band")
    values = [cnt.get(b, 0) for b in bands]

    # 人数越多颜色越深
    cmap = LinearSegmentedColormap.from_list("blue_grad", [C_LIGHT, C_BLUE])
    colors = [cmap(v / max(values)) for v in values]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(bands, values, color=colors, edgecolor=C_BORDER,
                  linewidth=0.8, width=0.55)
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v + max(values) * 0.02,
                f"{v}人 ({as_percent(v / len(recs))})", ha="center", fontsize=9)

    ax.set_title("各年龄段人数分布（柱形图）", fontsize=14, pad=12)
    ax.set_ylabel("人数")
    ax.set_xlabel("年龄段")
    ax.set_ylim(0, max(values) * 1.15)
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    save_and_show(fig, "2_年龄段分布柱形图.png")


# ==============================================================================
# 5. 图3  性别占比圆环图
# ==============================================================================
def draw_gender(recs):
    cnt = count_by(recs, "gender")
    labels = ["男", "女"]
    values = [cnt.get(k, 0) for k in labels]
    colors = [C_BLUE, C_RED]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(values, colors=colors, startangle=90, counterclock=False,
           wedgeprops=dict(width=0.32, edgecolor="white", linewidth=2))
    ax.text(0, 0.06, f"{len(recs):,}", ha="center", va="center",
            fontsize=26, fontweight="bold", color=C_BORDER)
    ax.text(0, -0.14, "总人数", ha="center", va="center",
            fontsize=11, color="#777777")

    ax.set_title("男女员工占比（圆环图）", fontsize=14, pad=15)
    handles = [mpatches.Patch(color=c, label=f"{l} {v}人 {as_percent(v / len(recs))}")
               for l, v, c in zip(labels, values, colors)]
    ax.legend(handles=handles, loc="center left", bbox_to_anchor=(1.0, 0.5),
              frameon=False, fontsize=10)
    ax.axis("equal")
    fig.tight_layout()
    save_and_show(fig, "3_性别占比圆环图.png")


# ==============================================================================
# 6. 图4  学历分布条形图
# ==============================================================================
def draw_edu(recs):
    cnt = count_by(recs, "edu")
    labels = DataBook.EDU_ORDER
    values = [cnt.get(k, 0) for k in labels]
    y = np.arange(len(labels))[::-1]             # 学历最低画在最下面

    cmap = LinearSegmentedColormap.from_list("blue_grad", [C_LIGHT, C_BLUE])
    colors = [cmap(v / max(values)) for v in values]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(y, values, color=colors, edgecolor=C_BORDER,
                   linewidth=0.8, height=0.55)
    for b, v in zip(bars, values):
        ax.text(v + max(values) * 0.015, b.get_y() + b.get_height() / 2,
                f"{v}人 ({as_percent(v / len(recs))})", va="center", fontsize=9)

    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlim(0, max(values) * 1.2)
    ax.set_title("各学历人数分布（条形图）", fontsize=14, pad=12)
    ax.set_xlabel("人数")
    ax.set_ylabel("学历")
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    save_and_show(fig, "4_学历分布条形图.png")


# ==============================================================================
# 7. 图5  婚姻状况占比饼图
# ==============================================================================
def draw_marriage(recs):
    cnt = count_by(recs, "marriage")
    labels = ["已婚", "单身", "离异"]
    values = [cnt.get(k, 0) for k in labels]
    colors = [C_BLUE, C_GOLD, C_RED]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(values, labels=labels, colors=colors, startangle=90,
           counterclock=False, autopct=autopct_int,
           wedgeprops=dict(edgecolor="white", linewidth=2),
           textprops=dict(fontsize=11))
    ax.set_title("员工婚姻状况占比（饼图）", fontsize=14, pad=15)
    ax.axis("equal")
    fig.tight_layout()
    save_and_show(fig, "5_婚姻状况占比饼图.png")


# ==============================================================================
# 8. 图6  各部门人数跑道图
# ==============================================================================
def draw_dept(recs):
    """同心半环构成"跑道"，人数最多的部门在最内环。"""
    cnt = count_by(recs, "dept")
    # 按人数升序排列：i=0 在最外环，人数最多的落在最内环
    items = sorted(cnt.items(), key=lambda kv: kv[1])
    depts = [k for k, _ in items]
    values = [v for _, v in items]
    colors = [C_PURPLE, C_BLUE, "#37A2DA", C_TEAL, "#F5C353", C_RED]

    fig, ax = plt.subplots(figsize=(8, 8))
    for i, (dept, v) in enumerate(zip(depts, values)):
        radius = 1 - i * 0.14
        ax.pie([v, len(recs) - v], colors=[colors[i % len(colors)], C_TRACK],
               radius=radius, startangle=90, counterclock=False,
               wedgeprops=dict(width=0.11, edgecolor="white", linewidth=1.5))

    ax.text(0, 0.10, "2022年3月", ha="center", va="center",
            fontsize=13, fontweight="bold")
    ax.text(0, -0.16, f"公司总人数\n{len(recs)}", ha="center", va="center",
            fontsize=10, color="#555555")

    ax.set_title("各部门人数跑道图（动态环形图）", fontsize=14, pad=15)
    handles = [mpatches.Patch(color=colors[i % len(colors)], label=f"{d} {v}")
               for i, (d, v) in enumerate(zip(depts, values))]
    ax.legend(handles=handles, loc="center left", bbox_to_anchor=(1.02, 0.5),
              frameon=False, fontsize=10)
    ax.axis("equal")
    fig.tight_layout()
    save_and_show(fig, "6_各部门人数跑道图.png")


# ==============================================================================
# 9. 图7  人力资源可视化看板（总览）
# ==============================================================================
def draw_dashboard(db, recs):
    total = len(recs)
    transfer = count_by(recs, "transfer")

    fig = plt.figure(figsize=(16, 9))
    gs = fig.add_gridspec(2, 3, hspace=0.32, wspace=0.25,
                          left=0.06, right=0.94, top=0.88, bottom=0.08)
    fig.suptitle("人力资源可视化看板（2022年3月）", fontsize=20, fontweight="bold")

    # ---- KPI 卡 ----
    ax = fig.add_subplot(gs[0, 0])
    ax.axis("off")
    card = mpatches.FancyBboxPatch((0.05, 0.1), 0.9, 0.8,
                                   boxstyle="round,pad=0.02,rounding_size=0.03",
                                   facecolor="#F5F8FC", edgecolor=C_BLUE, linewidth=1.5)
    ax.add_patch(card)
    ax.text(0.5, 0.74, "公司总人数", ha="center", fontsize=13, color="#555555",
            transform=ax.transAxes)
    ax.text(0.5, 0.45, f"{total:,}", ha="center", fontsize=36,
            fontweight="bold", color=C_BLUE, transform=ax.transAxes)
    sub = f"入职 {transfer.get('入职', 0)} · 转入 {transfer.get('转入', 0)} · 转出 {transfer.get('转出', 0)}"
    ax.text(0.5, 0.18, sub, ha="center", fontsize=10, color="#777777",
            transform=ax.transAxes)
    ax.set_title("人员总量", fontsize=13)

    # ---- 年龄段 ----
    ax = fig.add_subplot(gs[0, 1])
    bands = db.age_bands()
    cnt_age = count_by(recs, "age_band")
    vals = [cnt_age.get(b, 0) for b in bands]
    cmap = LinearSegmentedColormap.from_list("blue_grad", [C_LIGHT, C_BLUE])
    ax.bar(bands, vals, color=[cmap(v / max(vals)) for v in vals],
           edgecolor=C_BORDER, linewidth=0.8, width=0.6)
    for i, v in enumerate(vals):
        ax.text(i, v + max(vals) * 0.02, str(v), ha="center", fontsize=9)
    ax.set_ylim(0, max(vals) * 1.15)
    ax.set_title("年龄段分布", fontsize=13)
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # ---- 性别圆环 ----
    ax = fig.add_subplot(gs[0, 2])
    cnt_g = count_by(recs, "gender")
    g_vals = [cnt_g.get("男", 0), cnt_g.get("女", 0)]
    ax.pie(g_vals, colors=[C_BLUE, C_RED], startangle=90, counterclock=False,
           wedgeprops=dict(width=0.32, edgecolor="white", linewidth=2),
           autopct=autopct_int, pctdistance=0.82,
           textprops=dict(fontsize=10, color="white", fontweight="bold"))
    ax.set_title("性别占比", fontsize=13)
    ax.legend(["男", "女"], loc="lower center", ncol=2, frameon=False, fontsize=10)

    # ---- 学历条形 ----
    ax = fig.add_subplot(gs[1, 0])
    cnt_e = count_by(recs, "edu")
    labels = DataBook.EDU_ORDER
    vals = [cnt_e.get(k, 0) for k in labels]
    y = np.arange(len(labels))[::-1]
    ax.barh(y, vals, color=[cmap(v / max(vals)) for v in vals],
            edgecolor=C_BORDER, linewidth=0.8, height=0.55)
    for i, v in enumerate(vals):
        ax.text(v + max(vals) * 0.015, y[i], str(v), va="center", fontsize=9)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlim(0, max(vals) * 1.18)
    ax.set_title("学历分布", fontsize=13)
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # ---- 婚姻饼图 ----
    ax = fig.add_subplot(gs[1, 1])
    cnt_m = count_by(recs, "marriage")
    m_labels = ["已婚", "单身", "离异"]
    m_vals = [cnt_m.get(k, 0) for k in m_labels]
    ax.pie(m_vals, labels=m_labels, colors=[C_BLUE, C_GOLD, C_RED],
           startangle=90, counterclock=False, autopct=autopct_int,
           wedgeprops=dict(edgecolor="white", linewidth=2),
           textprops=dict(fontsize=10))
    ax.set_title("婚姻状况", fontsize=13)

    # ---- 部门条形 ----
    ax = fig.add_subplot(gs[1, 2])
    cnt_d = count_by(recs, "dept")
    items = sorted(cnt_d.items(), key=lambda kv: kv[1])
    d_labels = [k for k, _ in items]
    d_vals = [v for _, v in items]
    y = np.arange(len(d_labels))
    ax.barh(y, d_vals, color=C_BLUE, edgecolor=C_BORDER, linewidth=0.8, height=0.55)
    for b, v in zip(y, d_vals):
        ax.text(v + max(d_vals) * 0.015, b, str(v), va="center", fontsize=9)
    ax.set_yticks(y)
    ax.set_yticklabels(d_labels, fontsize=9)
    ax.set_xlim(0, max(d_vals) * 1.18)
    ax.set_title("部门人数", fontsize=13)
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    save_and_show(fig, "7_人力资源可视化看板.png")


# ==============================================================================
# 10. 主流程
# ==============================================================================
def main():
    print("=" * 68)
    print("第四章 人力资源可视化看板 —— Excel 数据可视化复现")
    print("=" * 68)
    print(f"数据源: {EXCEL_PATH}\n")

    db = DataBook(EXCEL_PATH)
    recs = db.records()
    print(f"  读取员工明细 {len(recs)} 条\n")

    steps = [
        ("1. 公司总人数 KPI 卡", lambda: draw_kpi(db, recs)),
        ("2. 年龄段分布柱形图", lambda: draw_age(db, recs)),
        ("3. 性别占比圆环图", lambda: draw_gender(recs)),
        ("4. 学历分布条形图", lambda: draw_edu(recs)),
        ("5. 婚姻状况占比饼图", lambda: draw_marriage(recs)),
        ("6. 各部门人数跑道图", lambda: draw_dept(recs)),
        ("7. 人力资源可视化看板", lambda: draw_dashboard(db, recs)),
    ]

    for title, fn in steps:
        print(f"  {title}")
        fn()
        print()

    print("=" * 68)
    print(f"全部完成，图片已输出至: {OUT_DIR}")
    print("=" * 68)


if __name__ == "__main__":
    main()
