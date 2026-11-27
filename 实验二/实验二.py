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

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


# ==============================================================================
# 0. 全局配置
# ==============================================================================
EXCEL_PATH = r"C:\Users\陈汝嘉\Desktop\专业课专业\数据分析及可视化\第三章 动态图表.xlsx"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

# 中文字体：优先微软雅黑，缺 SimHei 也不至于画成方块
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# 统一配色
C_BORDER = "#1A1E43"   # 描边深蓝
C_BLUE = "#0070C0"     # 主蓝
C_LIGHT = "#00B0F0"    # 浅蓝
C_RED = "#E74E69"      # 强调红
C_GOLD = "#FFC000"     # 金
C_TRACK = "#E8ECF3"    # 跑道底色
C_TEAL = "#11A7AD"
C_PURPLE = "#7030A0"


# ==============================================================================
# 1. 取数层：集中管理所有单元格坐标
# ==============================================================================
class DataBook:
    """只读的 Excel 取数封装，单元格坐标全部在这里定义。"""

    def __init__(self, path=EXCEL_PATH):
        self.path = path
        self.wb = openpyxl.load_workbook(path, data_only=True)

    def cell(self, sheet, row, col):
        """取单元格值（1-based 行列号，与 Excel 界面一致）。"""
        return self.wb[sheet].cell(row=row, column=col).value

    def row(self, sheet, row, start_col, end_col):
        """取一行的一段，返回 list。"""
        return [self.cell(sheet, row, c) for c in range(start_col, end_col + 1)]

    def rows(self, sheet, start_row, end_row, start_col, end_col):
        """取多行的一段，返回 list of list。"""
        return [self.row(sheet, r, start_col, end_col)
                for r in range(start_row, end_row + 1)]

    # ---- 各图专用取数方法（返回原始值，不做单位换算）----
    def bar_chart(self):
        """表1: 第12 行是表头(区域名)，第 13 行是数据(月份 + 数值)。"""
        s = "1 动态柱形图"
        return {
            "month": self.cell(s, 13, 2),            # B13 -> '5月'
            "labels": self.row(s, 12, 3, 8),          # C12:H12 -> 华北..华东
            "values": self.row(s, 13, 3, 8),          # C13:H13 -> 数值
        }

    def race_track(self):
        """表2: H/I/J 列分别是 4月人数、占位；配合 K 区的总人数说明。"""
        s = "2 动态跑道图"
        depts = self.rows(s, 4, 9, 8, 10)           # H4:J9
        return {
            "depts": [r[0] for r in depts],
            "values": [r[1] for r in depts],
            "pads": [r[2] for r in depts],
            "total_text": self.cell(s, 10, 8),       # H10 -> '4月公司总人数为1637'
        }

    def nightingale(self):
        """表3: 第12 行表头(渠道)，第 13 行是占比(小数)。"""
        s = "3 动态南丁格尔圆环图"
        return {
            "period": self.cell(s, 13, 2),           # B13 -> '近7天'
            "labels": self.row(s, 12, 3, 7),          # C12:G12
            "ratios": self.row(s, 13, 3, 7),          # C13:G13 -> 0.44 等
        }

    def combo(self):
        """表4: 第17 行表头(类别)，18/19/20 行分别是 销售额/利润/利润率。"""
        s = "4 动态组合图"
        return {
            "cats": self.row(s, 17, 3, 6),            # C17:F17
            "sales": self.row(s, 18, 3, 6),           # 销售额
            "profit": self.row(s, 19, 3, 6),          # 利润
            "rate": self.row(s, 20, 3, 6),            # 利润率(小数)
        }

    def pivot(self, include_total=False):
        """表5: 透视表，行标签在 B 列，值在 C 列。默认剔除'总计'行。"""
        s = "5 透视表切片器"
        labels, values = [], []
        for r in range(4, 10):
            label = self.cell(s, r, 2)
            value = self.cell(s, r, 3)
            if label is None:
                continue
            if not include_total and str(label).strip() == "总计":
                continue
            labels.append(label)
            values.append(value)
        return labels, values

    def jade(self):
        """表6: 第10 行表头(渠道)，第 11 行占比，第 12 行占位(两者相加为 1)。"""
        s = "6 VBA动态玉玦图"
        return {
            "period": self.cell(s, 11, 2),            # B11 -> '近30天'
            "names": self.row(s, 10, 3, 6),            # C10:F10
            "values": self.row(s, 11, 3, 6),           # 占比
            "pads": self.row(s, 12, 3, 6),            # 占位
        }

    def bead(self):
        """表7: 第14 行表头，15-20 行数据。C=图表字段, D=完成率, E=未完成率。"""
        s = "7 动态滑珠图"
        data = self.rows(s, 15, 20, 3, 5)
        return {
            "labels": [r[0] for r in data],          # 华北..华东
            "done": [r[1] for r in data],             # 完成率(小数)
            "undone": [r[2] for r in data],           # 未完成率(小数)
        }


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
    """小数 -> 百分数字符串，如 0.677 -> '68%'。"""
    if value is None:
        return ""
    return f"{value * 100:.{digits}f}%"


# ==============================================================================
# 3. 图1  动态柱形图
# ==============================================================================
def draw_bar_chart(db):
    d = db.bar_chart()
    labels, values = d["labels"], d["values"]

    fig, ax = plt.subplots(figsize=(9, 5), dpi=100)
    bars = ax.bar(labels, values, color=C_BLUE, edgecolor=C_BORDER,
                  linewidth=0.8, width=0.55)
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v + max(values) * 0.02,
                f"{v:,}", ha="center", fontsize=9)

    ax.set_title(f"{d['month']} 各区域销量（动态柱形图）", fontsize=14, pad=12)
    ax.set_ylabel("销量")
    ax.set_xlabel("区域")
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    save_and_show(fig, "1_动态柱形图.png")


# ==============================================================================
# 4. 图2  动态跑道图
# ==============================================================================
def draw_race_track(db):
    """同心半环构成"跑道"，环长表示部门人数占总人数的比例。"""
    d = db.race_track()
    depts, values, pads = d["depts"], d["values"], d["pads"]
    colors = [C_PURPLE, C_BLUE, "#37A2DA", C_TEAL, "#F5C353", C_RED]

    fig, ax = plt.subplots(figsize=(8, 8))

    # 每条跑道：实心段 = 部门人数，浅色段 = 剩余空位
    for i, (dept, v, pad) in enumerate(zip(depts, values, pads)):
        radius = 1 - i * 0.14
        ax.pie([v, pad], colors=[colors[i % len(colors)], C_TRACK],
               radius=radius, startangle=90, counterclock=False,
               wedgeprops=dict(width=0.11, edgecolor="white", linewidth=1.5))

    # 圆心：当前月份 + 总人数
    total = sum(values)
    ax.text(0, 0.10, "4月", ha="center", va="center",
            fontsize=14, fontweight="bold")
    ax.text(0, -0.16, f"公司总人数\n{total}", ha="center", va="center",
            fontsize=10, color="#555555")

    ax.set_title("各部门人数跑道图（动态环形图）", fontsize=14, pad=15)
    handles = [
        mpatches.Patch(color=colors[i % len(colors)], label=f"{dept} {v}")
        for i, (dept, v) in enumerate(zip(depts, values))
    ]
    ax.legend(handles=handles, loc="center left", bbox_to_anchor=(1.02, 0.5),
              frameon=False, fontsize=10)
    ax.axis("equal")
    fig.tight_layout()
    save_and_show(fig, "2_动态跑道图.png")


# ==============================================================================
# 5. 图3  动态南丁格尔圆环图
# ==============================================================================
def draw_nightingale(db):
    """极坐标柱形（玫瑰图）：半径越长，渠道占比越大。"""
    d = db.nightingale()
    labels, ratios = d["labels"], d["ratios"]
    # 占比是小数，转换成百分数，扇形高度才直观
    values = [r * 100 for r in ratios]
    colors = [C_TEAL, "#4A5BD1", "#6073F3", C_GOLD, "#E66B4C"]

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, polar=True)

    n = len(values)
    theta = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    bars = ax.bar(theta, values, width=2 * np.pi / n * 0.92,
                  color=colors, edgecolor="white", linewidth=1.5, alpha=0.9)

    for bar, v, r in zip(bars, values, ratios):
        ax.text(bar.get_x() + bar.get_width() / 2, v + max(values) * 0.05,
                as_percent(r), ha="center", va="bottom", fontsize=9)

    ax.set_xticks(theta)
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_yticklabels([])
    ax.set_ylim(0, max(values) * 1.2)
    ax.set_title(f"{d['period']} 来源渠道占比（动态南丁格尔圆环图）",
                 fontsize=14, pad=20)
    fig.tight_layout()
    save_and_show(fig, "3_动态南丁格尔圆环图.png")


# ==============================================================================
# 6. 图4  动态组合图（双轴：柱状 + 折线）
# ==============================================================================
def draw_combo(db):
    d = db.combo()
    cats, sales, profit = d["cats"], d["sales"], d["profit"]
    # 利润率在 Excel 里是小数，转百分数后与 set_ylim(0,80) 的量纲一致
    ratio = [r * 100 for r in d["rate"]]

    fig, ax1 = plt.subplots(figsize=(9, 5.5))
    x = np.arange(len(cats))
    w = 0.35

    bars1 = ax1.bar(x - w / 2, sales, w, label="销售额", color=C_BLUE,
                    edgecolor=C_BORDER, linewidth=0.6)
    bars2 = ax1.bar(x + w / 2, profit, w, label="利润", color=C_RED,
                    edgecolor=C_BORDER, linewidth=0.6)
    for b in list(bars1) + list(bars2):
        ax1.text(b.get_x() + b.get_width() / 2, b.get_height() + max(sales) * 0.015,
                 f"{b.get_height():,.0f}", ha="center", fontsize=8)

    ax1.set_xticks(x)
    ax1.set_xticklabels(cats)
    ax1.set_ylabel("金额（元）")
    ax1.set_xlabel("商品类别")
    ax1.set_ylim(0, max(sales) * 1.2)
    ax1.grid(axis="y", alpha=0.3, linestyle="--")
    ax1.set_axisbelow(True)

    ax2 = ax1.twinx()
    ax2.plot(x, ratio, color=C_GOLD, marker="o", linewidth=2.5, label="利润率")
    for i, v in enumerate(ratio):
        ax2.text(i, v + 2.5, f"{v:.1f}%", ha="center", fontsize=9, color="#B38600")
    ax2.set_ylabel("利润率(%)", color="#B38600")
    ax2.set_ylim(0, 80)
    ax2.tick_params(axis="y", labelcolor="#B38600")

    ax1.set_title("2022 商品销售额 / 利润 / 利润率（动态组合图）", fontsize=14, pad=12)
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper right", frameon=False, fontsize=10)

    fig.tight_layout()
    save_and_show(fig, "4_动态组合图.png")


# ==============================================================================
# 7. 图5  透视表切片器联动柱形图
# ==============================================================================
def draw_pivot(db, include_total=False):
    labels, values = db.pivot(include_total=include_total)
    colors = [C_BLUE if i % 2 == 0 else C_LIGHT for i in range(len(labels))]

    fig, ax = plt.subplots(figsize=(9, 5), dpi=100)
    bars = ax.bar(labels, values, color=colors, edgecolor=C_BORDER,
                  linewidth=0.7, width=0.6)
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v + max(values) * 0.02,
                f"{v:,.0f}", ha="center", fontsize=9)

    ax.set_title("各学历平均月收入（透视表切片器联动柱形图）", fontsize=14, pad=12)
    ax.set_ylabel("平均月收入（元）")
    ax.set_xlabel("学历")
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    save_and_show(fig, "5_透视表切片器柱形图.png")


# ==============================================================================
# 8. 图6  VBA 动态玉玦图
# ==============================================================================
def draw_jade(db):
    """玉玦图：同心环从内到外按占比降序排列，缺口一致，视觉上可横向比较。"""
    d = db.jade()
    names, values, pads = d["names"], d["values"], d["pads"]
    colors = [C_LIGHT, C_TEAL, C_GOLD, C_RED]

    # 按占比从大到小排序（玉玦图的标准画法：最内环占比最大）
    order = np.argsort(values)[::-1]
    names = [names[i] for i in order]
    values = [values[i] for i in order]
    pads = [pads[i] for i in order]
    colors = [colors[i % len(colors)] for i in range(len(names))]

    fig, ax = plt.subplots(figsize=(8, 8))
    for i, (name, v, pad) in enumerate(zip(names, values, pads)):
        radius = 1 - i * 0.20
        ax.pie([v, pad], colors=[colors[i], C_TRACK],
               radius=radius, startangle=90, counterclock=False,
               wedgeprops=dict(width=0.16, edgecolor="white", linewidth=1.5))

    ax.text(0, -1.28, d["period"], ha="center", va="center",
            fontsize=13, fontweight="bold", color="#555555")
    ax.set_title("来源渠道占比玉玦图（VBA 动态环形图）", fontsize=14, pad=15)
    handles = [
        mpatches.Patch(color=colors[i], label=f"{n} {as_percent(v)}")
        for i, (n, v) in enumerate(zip(names, values))
    ]
    ax.legend(handles=handles, loc="center left", bbox_to_anchor=(1.0, 0.5),
              frameon=False, fontsize=10)
    ax.axis("equal")
    fig.tight_layout()
    save_and_show(fig, "6_VBA动态玉玦图.png")


# ==============================================================================
# 9. 图7  动态滑珠图
# ==============================================================================
def draw_bead(db):
    """横向堆叠柱：完成率(实心) + 未完成率(浅色)，滑珠标在分界点上。"""
    d = db.bead()
    labels = d["labels"]
    # Excel 里是 0-1 小数，转成百分数配合 xlim(0,100)
    done = [v * 100 for v in d["done"]]
    undone = [v * 100 for v in d["undone"]]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    y = np.arange(len(labels))[::-1]

    ax.barh(y, done, color=C_BLUE, edgecolor="white", height=0.55,
            label="完成率")
    ax.barh(y, undone, left=done, color=C_LIGHT, edgecolor="white",
            height=0.55, alpha=0.45, label="未完成率")
    # 滑珠：白心深边的圆点，落在完成/未完成的分界处
    ax.scatter(done, y, s=90, color="white", edgecolor=C_BORDER,
               zorder=5, linewidth=1.5)
    for i, d_val in enumerate(done):
        ax.text(d_val / 2, y[i], f"{d_val:.0f}%", ha="center", va="center",
                fontsize=9, color="white", fontweight="bold")

    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("占比")
    ax.set_xlim(0, 100)
    ax.set_title("各区域任务完成率滑珠图（动态横向堆叠柱形图）", fontsize=14, pad=12)
    ax.legend(frameon=False, loc="lower right", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    save_and_show(fig, "7_动态滑珠图.png")


# ==============================================================================
# 10. 主流程
# ==============================================================================
def main():
    print("=" * 68)
    print("第三章 动态图表 —— Excel 数据可视化复现")
    print("=" * 68)
    print(f"数据源: {EXCEL_PATH}\n")

    db = DataBook(EXCEL_PATH)

    steps = [
        ("1. 动态柱形图", lambda: draw_bar_chart(db)),
        ("2. 动态跑道图", lambda: draw_race_track(db)),
        ("3. 动态南丁格尔圆环图", lambda: draw_nightingale(db)),
        ("4. 动态组合图", lambda: draw_combo(db)),
        ("5. 透视表切片器柱形图", lambda: draw_pivot(db)),
        ("6. VBA 动态玉玦图", lambda: draw_jade(db)),
        ("7. 动态滑珠图", lambda: draw_bead(db)),
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
