import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Wedge, Circle, Polygon, Rectangle, FancyArrow
from matplotlib.collections import PatchCollection
import matplotlib.font_manager as fm

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

OUTER = "#0b1226"
CARD = "#141c3a"
CARD2 = "#182144"
GRID = "#22315f"
TRACK = "#2a3765"
TICK = "#93a7d4"
TEXT = "#eaf1ff"
SUB = "#8ca3d8"
FOOT = "#4e6095"

BLUE = "#2e7cf6"
BLUEL = "#5aa9ff"
CYAN = "#37c6d4"
GREEN = "#2fd3a0"
YELLOW = "#f5d14e"
ORANGE = "#f79a3e"
RED = "#f2556b"
PINK = "#ff7a9c"
PURPLE = "#8b6bf0"
GRAY = "#5a6d9e"
GRAYD = "#3c4a7a"

PALETTE = [BLUE, ORANGE, CYAN, YELLOW, PURPLE, RED, GREEN, PINK, BLUEL, ORANGE]

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUT, exist_ok=True)

_counter = [0]


def new_card(title, sub="", note="", w=6.2, h=3.7, top=0.80):
    fig = plt.figure(figsize=(w, h), facecolor=OUTER)
    fig.add_artist(FancyBboxPatch(
        (0.012, 0.012), 0.976, 0.976,
        boxstyle="round,pad=0,rounding_size=0.045",
        transform=fig.transFigure, fc=CARD, ec="none", zorder=-10))
    if title:
        fig.text(0.055, 0.945, title, color=TEXT, fontsize=12.5,
                 fontweight="bold", va="top")
    if sub:
        fig.text(0.055, 0.845, sub, color=SUB, fontsize=7.2, va="top")
    if note:
        fig.text(0.055, 0.038, note, color=FOOT, fontsize=5.8, va="bottom")
    return fig


def area(fig, l=0.085, b=0.115, w=0.845, h=0.66):
    ax = fig.add_axes([l, b, w, h])
    ax.set_facecolor("none")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors=TICK, labelsize=6.0, length=0, pad=2)
    ax.xaxis.label.set_color(TICK)
    ax.yaxis.label.set_color(TICK)
    return ax


def gridlines(ax, axis="y"):
    ax.grid(axis=axis, color=GRID, lw=0.6, alpha=0.8)
    ax.set_axisbelow(True)


def save(fig, name):
    _counter[0] += 1
    path = os.path.join(OUT, f"{_counter[0]:02d}_{name}.png")
    fig.savefig(path, dpi=150, facecolor=OUTER)
    plt.close(fig)
    return path


def polar_area(fig, h=0.66, cx=0.5, cy=0.13, polar=True):
    fh, fw = fig.get_size_inches()[1], fig.get_size_inches()[0]
    w = h * fh / fw
    proj = "polar" if polar else None
    ax = fig.add_axes([cx - w / 2, cy, w, h], projection=proj)
    ax.set_facecolor("none")
    ax.set_aspect("equal")
    return ax


def nolabels(ax):
    ax.set_xticks([])
    ax.set_yticks([])


def bar_labels(ax, bars, fmt="{:,.0f}", dy=0.012, color=TEXT, size=5.6, weight="bold"):
    for b in bars:
        v = b.get_width() if b.get_height() == 0 else b.get_height()
        x, y = b.get_x() + b.get_width() / 2, b.get_height()
        if abs(b.get_height()) > 1e-9:
            ax.text(x, y + dy * abs(1), fmt.format(v), ha="center", va="bottom",
                    color=color, fontsize=size, fontweight=weight)
        else:
            ax.text(b.get_x() + b.get_width(), b.get_y() + b.get_height() / 2,
                    fmt.format(v), ha="left", va="center", color=color,
                    fontsize=size, fontweight=weight)


# ---------------------------------------------------------------- 1 横向条形
def c01():
    fig = new_card("3月各区域销量分布",
                   "东北区销量占比总销量的22%，华南销量最低",
                   "数据来源:营销中心大区数据看板 · 统计口径2023.03.31")
    ax = area(fig, 0.20, 0.13, 0.70, 0.63)
    cats = ["东区", "西区", "南区", "北区", "西北区", "东北区"]
    vals = [20445, 20663, 21178, 19980, 28535, 30642]
    y = np.arange(len(cats))
    bars = ax.barh(y, vals, height=0.55, color=BLUE)
    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=6.5)
    ax.set_xlim(0, 35500)
    gridlines(ax, "x")
    ax.set_xticks([0, 5000, 10000, 15000, 20000, 25000, 30000, 35000])
    ax.set_xticklabels([f"{v//1000}k" for v in [0, 5000, 10000, 15000, 20000, 25000, 30000, 35000]])
    for b, v in zip(bars, vals):
        ax.text(v + 500, b.get_y() + b.get_height() / 2, f"{v:,}",
                va="center", color=TEXT, fontsize=5.8)
    return save(fig, "3月各区域销量分布")


# ---------------------------------------------------------------- 2 横向分组条
def c02():
    fig = new_card("3月商品销量对比",
                   "华东地区:3月销量最高，苏南地区-3月销量8.23万",
                   "数据来源:营销中心大区数据看板 · 统计口径2023.03.31")
    ax = area(fig, 0.20, 0.14, 0.68, 0.62)
    cats = ["华东", "华西", "华北", "华南", "华中", "东北"]
    v2020 = [68200, 72100, 65400, 61400, 52900, 46400]
    v2021 = [85200, 74100, 78400, 71100, 66200, 51600]
    y = np.arange(len(cats))
    h = 0.32
    ax.barh(y - h / 2 - 0.02, v2020, height=h, color=CYAN, label="2020年")
    ax.barh(y + h / 2 + 0.02, v2021, height=h, color=RED, label="2021年")
    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=6.5)
    ax.invert_yaxis()
    ax.set_xlim(0, 96000)
    gridlines(ax, "x")
    for i, (a, b) in enumerate(zip(v2020, v2021)):
        ax.text(a + 1200, i - h / 2 - 0.02, f"{a:,}", va="center", color=TEXT, fontsize=5.2)
        ax.text(b + 1200, i + h / 2 + 0.02, f"{b:,}", va="center", color=TEXT, fontsize=5.2)
    ax.legend(loc="upper right", frameon=False, fontsize=5.6, labelcolor=TICK, ncol=2)
    return save(fig, "3月商品销量对比")


# ---------------------------------------------------------------- 3 多色竖柱
def c03():
    fig = new_card("2021年商品销售情况",
                   "口红总销量最高同比增长24.13%",
                   "数据来源:营销中心大区数据看板 · 统计口径2021.12.31")
    ax = area(fig)
    cats = ["口红", "面膜", "眼影", "粉底液", "精华", "防晒霜"]
    vals = [9820, 7640, 6950, 11250, 8540, 7230]
    bars = ax.bar(cats, vals, width=0.5, color=[CYAN, GREEN, ORANGE, YELLOW, PURPLE, BLUEL])
    ax.set_ylim(0, 14000)
    gridlines(ax, "y")
    for b, v, r in zip(bars, vals, ["24.13%", "18.02%", "11.45%", "31.20%", "9.87%", "6.43%"]):
        ax.text(b.get_x() + b.get_width() / 2, v + 200, f"{v:,}",
                ha="center", color=TEXT, fontsize=5.8, fontweight="bold")
        ax.text(b.get_x() + b.get_width() / 2, v / 2, r,
                ha="center", color="#0b1226", fontsize=5.0, fontweight="bold")
    return save(fig, "2021年商品销售情况")


# ---------------------------------------------------------------- 4 柱+线双轴
def c04():
    fig = new_card("2021年各季度销售额(万)与利润额(万)",
                   "总利润达:年度总利润达1578.7万,同期增长79.5%",
                   "数据来源:营销中心大区数据看板 · 统计口径2021.12.31")
    ax = area(fig)
    q = ["第一季度", "第二季度", "第三季度", "第四季度"]
    sales = [6230, 5480, 6120, 6540]
    profit = [186, 164, 192, 205]
    x = np.arange(4)
    bars = ax.bar(x - 0.19, sales, width=0.34, color=BLUE, label="销售额")
    bars2 = ax.bar(x + 0.19, profit, width=0.34, color=PINK, label="利润额")
    ax.set_ylim(0, 8200)
    gridlines(ax, "y")
    ax.set_xticks(x)
    ax.set_xticklabels(q, fontsize=6.5)
    for bs in (bars, bars2):
        for b in bs:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 110,
                    f"{b.get_height():,.0f}", ha="center", color=TEXT, fontsize=5.2)
    ax2 = ax.twinx()
    ax2.set_facecolor("none")
    for s in ax2.spines.values():
        s.set_visible(False)
    ax2.set_ylim(0, 300)
    ax2.tick_params(colors=TICK, labelsize=6.0, length=0)
    ln, = ax2.plot(x, [p * 10.4 for p in profit], color=YELLOW, lw=1.6, marker="o", ms=4)
    ax2.legend([bars, ln], ["销售额", "利润额"], loc="upper left", frameon=False,
               fontsize=5.6, labelcolor=TICK)
    return save(fig, "2021年各季度销售额与利润额")


# ---------------------------------------------------------------- 5 分组柱+折线
def c05():
    fig = new_card("2022年商品对比去年销售情况",
                   "同比数据:受疫情影响销售量下降，同期下降28%，同期销售下降",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.12.31")
    ax = area(fig)
    cats = ["口红", "面膜", "精华", "粉底液", "眼影"]
    cur = [11240, 8640, 9120, 10350, 7880]
    last = [12840, 9620, 8960, 9640, 8640]
    growth = [-12.5, -10.1, 1.8, 7.3, -8.8]
    x = np.arange(len(cats))
    b1 = ax.bar(x - 0.19, cur, width=0.34, color=BLUE, label="2022年")
    b2 = ax.bar(x + 0.19, last, width=0.34, color=GRAY, label="2021年")
    ax.set_ylim(0, 16500)
    gridlines(ax, "y")
    ax.set_xticks(x)
    ax.set_xticklabels(cats, fontsize=6.5)
    for bs, col in ((b1, TEXT), (b2, TICK)):
        for b in bs:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 220,
                    f"{b.get_height():,.0f}", ha="center", color=col, fontsize=5.0)
    ax.tick_params(axis="y", labelsize=6)
    ax2 = ax.twinx()
    ax2.set_facecolor("none")
    for s in ax2.spines.values():
        s.set_visible(False)
    ax2.set_ylim(-22, 14)
    ax2.tick_params(colors=TICK, labelsize=6.0, length=0)
    ax2.plot(x, growth, color=ORANGE, lw=1.5, marker="o", ms=4)
    ax2.axhline(0, color=GRID, lw=0.8)
    for xi, g in zip(x, growth):
        ax2.annotate(f"{g}%", (xi, g), textcoords="offset points", xytext=(0, 6),
                     ha="center", color=ORANGE, fontsize=5.0, fontweight="bold")
    ax.legend(loc="upper left", frameon=False, fontsize=5.6, labelcolor=TICK, ncol=2)
    return save(fig, "2022年商品对比去年销售情况")


# ---------------------------------------------------------------- 6 竖柱+目标线
def c06():
    fig = new_card("2022年上半年各商品销售情况",
                   "口罩品类销量最高同比增长78.7%，增速领先所有品类",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.06.30")
    ax = area(fig)
    cats = ["口红", "面膜", "精华", "防晒", "清洁", "彩妆"]
    vals = [9840, 7620, 8210, 11240, 9340, 8720]
    bars = ax.bar(cats, vals, width=0.48, color=BLUE)
    ax.set_ylim(0, 13800)
    gridlines(ax, "y")
    ax.axhline(9000, color=ORANGE, lw=1.1, ls=(0, (4, 3)))
    ax.text(4.55, 9300, "目标线 9,000", color=ORANGE, fontsize=5.2, ha="right")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 200, f"{v:,}",
                ha="center", color=TEXT, fontsize=5.8, fontweight="bold")
    return save(fig, "2022年上半年各商品销售情况")


# ---------------------------------------------------------------- 7 城市销售进度
def c07():
    fig = new_card("2022年上半年各城市销售进度",
                   "深莞市销售进度82.9%排在第一，增速55.8%",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.06.30")
    ax = area(fig, 0.16, 0.14, 0.76, 0.62)
    cities = ["苏州市", "青岛市", "长沙市", "西安市", "合肥市"]
    done = [62, 48, 71, 35, 20]
    total = [100, 100, 100, 100, 100]
    y = np.arange(len(cities))
    ax.barh(y, total, height=0.46, color=TRACK)
    cols = [BLUE, "#2f6dd8", BLUE, "#2a58b0", "#25488c"]
    for i, d in enumerate(done):
        ax.barh(y[i], d, height=0.46, color=cols[i])
        ax.text(d + 2, y[i], f"{d}%", va="center", color=TEXT, fontsize=6.0, fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(cities, fontsize=6.5)
    ax.set_xlim(0, 118)
    ax.set_xticks([])
    ax.invert_yaxis()
    return save(fig, "2022年上半年各城市销售进度")


# ---------------------------------------------------------------- 8 瀑布图
def c08():
    fig = new_card("2022年饮品类别季度销量进度",
                   "各茶饮销售额达标，全年总销售额26万杯",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.12.31")
    ax = area(fig, 0.17, 0.14, 0.74, 0.62)
    labels = ["第一季度", "第二季度", "第三季度", "第四季度", "全年合计"]
    start = 38
    delta = [9, -6, 4, -2]
    running = start
    xs = np.arange(5)
    ax.bar(0, start, width=0.55, color=BLUE)
    ax.text(0, start + 1.4, f"{start}", ha="center", color=TEXT, fontsize=6, fontweight="bold")
    for i, d in enumerate(delta):
        col = GREEN if d > 0 else RED
        base = running if d > 0 else running + d
        ax.bar(i + 1, abs(d), bottom=base, width=0.55, color=col)
        ax.text(i + 1, base + abs(d) + 1.4, f"{d:+d}", ha="center",
                color=col, fontsize=6, fontweight="bold")
        ax.plot([i + 0.72, i + 1.28], [running, running], color=GRAYD, lw=0.9, ls=":")
        running += d
    ax.bar(4, running, width=0.55, color=BLUEL)
    ax.text(4, running + 1.4, f"{running}", ha="center", color=TEXT, fontsize=6, fontweight="bold")
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=6.0)
    ax.set_ylim(0, 56)
    gridlines(ax, "y")
    return save(fig, "2022年饮品类别季度销量进度")


# ---------------------------------------------------------------- 9 分组柱多系列
def c09():
    fig = new_card("2021年各化奖品销售走势",
                   "全年总销售额达9,237万元，年度销售额同比增长16.67%",
                   "数据来源:营销中心大区数据看板 · 统计口径2021.12.31")
    ax = area(fig)
    groups = ["护肤类", "彩妆类", "洗护类", "香氛类"]
    data = np.array([
        [1240, 980, 620, 1450],
        [1620, 1340, 780, 1180],
        [980, 1540, 1120, 860],
        [1840, 1460, 1240, 980],
    ])
    cols = [BLUE, ORANGE, YELLOW, PURPLE]
    x = np.arange(4)
    w = 0.19
    for i in range(4):
        b = ax.bar(x + (i - 1.5) * w, data[:, i], width=w, color=cols[i],
                   label=["Q1", "Q2", "Q3", "Q4"][i])
        for r in b:
            ax.text(r.get_x() + r.get_width() / 2, r.get_height() + 25,
                    f"{r.get_height():,.0f}", ha="center", color=TEXT, fontsize=4.3)
    for xi, xi2 in zip(ax.patches[-4:], ax.patches[-4:]):
        pass
    ax.set_xticks(x)
    ax.set_xticklabels(groups, fontsize=6.5)
    ax.set_ylim(0, 2250)
    gridlines(ax, "y")
    ax.legend(loc="upper left", frameon=False, fontsize=5.4, labelcolor=TICK, ncol=4)
    return save(fig, "2021年各化奖品销售走势")


# ---------------------------------------------------------------- 10 百分比堆叠条
def c10():
    fig = new_card("2021年各区域销量及同比情况",
                   "东北地区销量最高同比增长9.7%，其中华中下降最多，同比下降20.6%",
                   "数据来源:营销中心大区数据看板 · 统计口径2021.12.31")
    ax = area(fig, 0.22, 0.15, 0.70, 0.60)
    cats = ["华东", "东北", "华北", "华中", "华南", "西南"]
    share = [28, 22, 18, 14, 11, 7]
    yoy = [2.8, 9.7, -17.0, -20.6, -3.7, -19.6]
    y = np.arange(len(cats))
    ax.barh(y, share, height=0.5, color=BLUE)
    ax.barh(y, [100 - s for s in share], left=share, height=0.5, color=TRACK)
    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=6.5)
    ax.set_xlim(0, 100)
    ax.set_xticks([])
    ax.invert_yaxis()
    for i, (s, g) in enumerate(zip(share, yoy)):
        ax.text(s / 2, i, f"{s}%", ha="center", va="center", color="#ffffff",
                fontsize=5.8, fontweight="bold")
        c = GREEN if g > 0 else RED
        ax.text(101, i, f"{g:+.1f}%", va="center", color=c, fontsize=5.6, fontweight="bold")
    return save(fig, "2021年各区域销量及同比情况")


# ---------------------------------------------------------------- 11 子弹图
def c11():
    fig = new_card("区域年度销售情况分析",
                   "华东区域销量最高，目标达成率最高；华西区域",
                   "数据来源:营销中心大区数据看板 · 统计口径2021.12.31")
    ax = area(fig, 0.20, 0.15, 0.72, 0.60)
    cats = ["华东", "华西", "华北", "华中", "华南"]
    pct = [78, 62, 55, 41, 88]
    y = np.arange(len(cats))
    ax.barh(y, 100, height=0.42, color=TRACK)
    cols = [BLUE, "#3a6ad0", "#2f5cc0", "#2a55b0", CYAN]
    for i, p in enumerate(pct):
        ax.barh(y[i], p, height=0.42, color=cols[i])
        ax.plot([p], [y[i]], marker="o", ms=4.2, color="#ffffff", zorder=5)
        ax.text(p + 2.5, y[i], f"{p}%", va="center", color=TEXT, fontsize=6.0, fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=6.5)
    ax.set_xlim(0, 118)
    ax.set_xticks([])
    ax.invert_yaxis()
    ax.text(101, len(cats) - 0.35, "目标达成率", color=TICK, fontsize=5.4)
    return save(fig, "区域年度销售情况分析")


# ---------------------------------------------------------------- 12 左右对比条
def c12():
    fig = new_card("2022年上半年各区域同比去年销量",
                   "2022年整体销量高于2021年，只有东北地区出现销量下降",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.06.30")
    ax = area(fig, 0.185, 0.14, 0.72, 0.62)
    cats = ["华东地区", "华西地区", "华北地区", "华中地区", "东北地区"]
    cur = [65200, 51300, 44800, 38700, 21000]
    last = [58200, 49600, 42100, 36400, 27500]
    y = np.arange(len(cats))
    ax.barh(y, cur, height=0.38, color=BLUE, label="2022年")
    ax.barh(y, [-v for v in last], height=0.38, color=RED, label="2021年")
    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=6.5)
    ax.set_xlim(-72000, 78000)
    ax.invert_yaxis()
    ax.axvline(0, color=GRID, lw=0.8)
    gridlines(ax, "x")
    for i, (a, b) in enumerate(zip(cur, last)):
        ax.text(a + 1200, i, f"{a:,}", va="center", color=TEXT, fontsize=5.0)
        ax.text(-b - 1200, i, f"{b:,}", va="center", color=TEXT, fontsize=5.0)
    ax.text(0, 4.80, "2022年", color=SUB, fontsize=5.4, ha="center")
    ax.set_xticks([])
    ax.legend(loc="upper right", frameon=False, fontsize=5.4, labelcolor=TICK, ncol=2)
    return save(fig, "2022年上半年各区域同比去年销量")


# ---------------------------------------------------------------- 13 目标达成子弹
def c13():
    fig = new_card("2022年上半年产品销售目标达成率情况",
                   "华南地区销售达成率超86%，年度总销售额75%",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.06.30")
    ax = area(fig, 0.21, 0.15, 0.70, 0.60)
    cats = ["华东", "华西", "华北", "华中", "华南"]
    pct = [68, 74, 62, 51, 86]
    target = [70, 70, 70, 70, 70]
    y = np.arange(len(cats))
    ax.barh(y, 100, height=0.40, color=TRACK)
    for i, (p, t) in enumerate(zip(pct, target)):
        ax.barh(y[i], p, height=0.40, color=BLUE)
        ax.plot([t], [y[i]], marker="o", ms=6, color=ORANGE, zorder=6)
        ax.text(p + 3.0, y[i] + 0.26, f"{p}%", va="center", color=TEXT,
                fontsize=6.0, fontweight="bold")
        ax.text(t, y[i] - 0.40, f"目标{t}%", va="center", ha="center",
                color=ORANGE, fontsize=4.6)
    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=6.5)
    ax.set_xlim(0, 112)
    ax.set_xticks([])
    ax.invert_yaxis()
    return save(fig, "2022年上半年产品销售目标达成率")


# ---------------------------------------------------------------- 14 漏斗
def c14():
    fig = new_card("2023年录制人员转化情况",
                   "高的转换比率达到61.1%，是我的不断下午做一个数据源",
                   "数据来源:营销中心大区数据看板 · 统计口径2023.11.17")
    ax = area(fig, 0.20, 0.13, 0.72, 0.64)
    stages = ["到达人数", "沟通人数", "面试人数", "入职人数"]
    vals = [124, 82, 49, 21]
    cols = [RED, YELLOW, BLUE, GREEN]
    maxw, minw = 100, 26
    y = np.arange(len(stages))
    top_w = 100
    for i, (v, c) in enumerate(zip(vals, cols)):
        w0 = top_w - i * (top_w - 24) / 3
        w1 = top_w - (i + 1) * (top_w - 24) / 3
        ax.add_patch(Polygon([[-w0 / 2, i - 0.44], [w0 / 2, i - 0.44],
                              [w1 / 2, i + 0.44], [-w1 / 2, i + 0.44]],
                             closed=True, facecolor=c, edgecolor="none"))
        ax.text(0, i, str(v), ha="center", va="center", color="#0b1226",
                fontsize=8, fontweight="bold")
        if i > 0:
            rate = vals[i] / vals[i - 1] * 100
            ax.text(maxw / 2 + 4, i, f"{rate:.1f}%", va="center", color=TICK, fontsize=5.4)
    ax.set_yticks(y)
    ax.set_yticklabels(stages, fontsize=6.5)
    ax.set_xlim(-62, 78)
    ax.set_ylim(3.7, -0.75)
    ax.set_xticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    return save(fig, "2023年录制人员转化情况")


# ---------------------------------------------------------------- 15 漏斗百分比
def c15():
    fig = new_card("2023年录制人员转化率",
                   "我的课题领域交付18.4%，较到下月份做一个数据源",
                   "数据来源:营销中心大区数据看板 · 统计口径2023.11.17")
    ax = area(fig, 0.19, 0.13, 0.73, 0.64)
    stages = ["到达人数", "留存人数", "面试人数", "入职人数", "转正人数"]
    vals = [124, 82, 49, 21, 8]
    rates = [100, 66.1, 59.8, 42.9, 38.1]
    cols = [RED, ORANGE, YELLOW, BLUE, CYAN]
    y = np.arange(len(stages))
    top_w = 118
    for i, (r, c) in enumerate(zip(rates, cols)):
        w0 = r * 1.05
        w1 = (rates[i + 1] * 1.05 if i + 1 < len(rates) else r * 0.62)
        ax.add_patch(Polygon([[-w0 / 2, i - 0.45], [w0 / 2, i - 0.45],
                              [w1 / 2, i + 0.45], [-w1 / 2, i + 0.45]],
                             closed=True, facecolor=c, edgecolor="none"))
        ax.text(0, i, f"{r}%", ha="center", va="center", color="#0b1226",
                fontsize=7, fontweight="bold")
        ax.text(64, i, f"{vals[i]}人", ha="right", va="center", color=TICK, fontsize=5.6)
    ax.set_yticks(y)
    ax.set_yticklabels(stages, fontsize=6.5)
    ax.set_xlim(-66, 66)
    ax.set_ylim(4.7, -0.7)
    ax.set_xticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    return save(fig, "2023年录制人员转化率")


# ---------------------------------------------------------------- 16 红色横向条
def c16():
    fig = new_card("2023年上半年产品销售情况",
                   "华东区域销售业绩172.1万，稳坐区域第1",
                   "数据来源:营销中心大区数据看板 · 统计口径2023.06.30")
    ax = area(fig, 0.22, 0.14, 0.66, 0.62)
    cats = ["口红", "面膜", "粉底液", "眼影", "精华", "防晒", "卸妆水"]
    vals = [5630, 5391, 3787, 3465, 2518, 2130, 1946]
    y = np.arange(len(cats))
    cmap = plt.cm.Reds
    cols = [cmap(0.35 + 0.09 * i) for i in range(len(cats))]
    ax.barh(y, vals, height=0.52, color=cols)
    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=6.5)
    ax.invert_yaxis()
    ax.set_xlim(0, 6600)
    ax.set_xticks([])
    gridlines(ax, "x")
    for b, v in zip(ax.patches, vals):
        ax.text(v + 90, b.get_y() + b.get_height() / 2, f"{v:,}", va="center",
                color=TEXT, fontsize=5.4)
    return save(fig, "2023年上半年产品销售情况")


# ---------------------------------------------------------------- 17 三列分组柱
def c17():
    fig = new_card("2022年1-3月各品牌销售情况",
                   "54及1月销量同比下降，TF 1月份销量高于同期",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.03.31")
    ax = area(fig)
    brands = ["VOGUE", "WS", "TF", "新锐品牌", "国货品牌", "其他"]
    jan = [620, 480, 340, 760, 910, 520]
    feb = [480, 620, 450, 610, 1080, 430]
    mar = [740, 590, 520, 830, 1260, 610]
    y = np.arange(len(brands))
    h = 0.24
    cols = [PINK, PURPLE, ORANGE]
    for k, (vals, name) in enumerate(zip([jan, feb, mar], ["1月", "2月", "3月"])):
        ax.barh(y + (1 - k) * h, vals, height=h, color=cols[k], label=name)
    ax.set_yticks(y)
    ax.set_yticklabels(brands, fontsize=6.0)
    ax.invert_yaxis()
    ax.set_xlim(0, 1600)
    ax.set_xticks([])
    for k, vals in enumerate([jan, feb, mar]):
        for i, v in enumerate(vals):
            ax.text(v + 20, i + (1 - k) * h, f"{v}", va="center", color=TEXT, fontsize=4.6)
    ax.legend(loc="upper right", frameon=False, fontsize=5.2, labelcolor=TICK, ncol=3)
    return save(fig, "2022年1-3月各品牌销售情况")


# ---------------------------------------------------------------- 18 分组柱+折线
def c18():
    fig = new_card("2022年商品对比去年销售情况",
                   "商品整体销售业绩不佳，其中线下销量多，同比下降33%",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.12.31")
    ax = area(fig)
    cats = ["口红", "面膜", "精华", "粉底液", "眼影", "防晒"]
    cur = [6420, 4780, 3860, 5210, 4620, 5340]
    last = [5540, 4210, 3480, 4160, 4260, 3980]
    growth = [15.9, 13.5, 10.9, 25.2, 8.5, 34.2]
    x = np.arange(len(cats))
    ax.bar(x - 0.19, cur, width=0.34, color=BLUE, label="2022年")
    ax.bar(x + 0.19, last, width=0.34, color=GRAY, label="2021年")
    ax.set_ylim(0, 8200)
    gridlines(ax, "y")
    ax.set_xticks(x)
    ax.set_xticklabels(cats, fontsize=6.2)
    ax.tick_params(axis="y", labelsize=5.6)
    for bs, col in ((ax.patches[:6], TEXT), (ax.patches[6:], TICK)):
        for b in bs:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 130,
                    f"{b.get_height():,.0f}", ha="center", color=col, fontsize=4.6)
    ax2 = ax.twinx()
    ax2.set_facecolor("none")
    for s in ax2.spines.values():
        s.set_visible(False)
    ax2.set_ylim(0, 46)
    ax2.tick_params(colors=TICK, labelsize=6.0, length=0)
    ax2.plot(x, growth, color=ORANGE, lw=1.5, marker="o", ms=4)
    for xi, g in zip(x, growth):
        ax2.annotate(f"{g}%", (xi, g), textcoords="offset points", xytext=(0, 6),
                     ha="center", color=ORANGE, fontsize=4.8, fontweight="bold")
    ax.legend(loc="upper left", frameon=False, fontsize=5.4, labelcolor=TICK, ncol=2)
    return save(fig, "2022年商品对比去年销售情况_条形")


# ---------------------------------------------------------------- 19 折线+面积
def c19():
    fig = new_card("化妆品类月度销售趋势",
                   "2022年数据显示7月、11月最高，销量达3.752",
                   "数据来源:营销中心大区数据看板 · 统计口径2023.08.31")
    ax = area(fig, 0.09, 0.34, 0.85, 0.42)
    m = list(range(1, 13))
    v = [380, 420, 560, 720, 980, 1420, 2750, 3120, 2050, 1780, 3400, 2100]
    ax.fill_between(m, v, color=BLUE, alpha=0.18)
    ax.plot(m, v, color=BLUE, lw=1.7)
    ax.scatter([7, 11], [2750, 3400], s=22, color=ORANGE, zorder=6)
    ax.annotate("3,752", (7, 2750), textcoords="offset points", xytext=(0, 9),
                ha="center", color=ORANGE, fontsize=5.4, fontweight="bold")
    ax.set_ylim(0, 4100)
    ax.set_xticks(m)
    ax.set_xticklabels(["1月", "2月", "3月", "4月", "5月", "6月",
                        "7月", "8月", "9月", "10月", "11月", "12月"], fontsize=5.6)
    gridlines(ax, "y")
    bands = [(0.08, 0.30, CYAN, "2022上半年"), (0.36, 0.58, YELLOW, "2022下半年"),
             (0.64, 0.86, ORANGE, "2023上半年"), (0.92, 0.99, PURPLE, "")]
    for x0, x1, c, t in bands:
        fig.patches.append(Rectangle((x0, 0), x1 - x0, 0.105,
                                     transform=fig.transFigure, facecolor=c,
                                     edgecolor="none", zorder=5))
        if t:
            fig.text((x0 + x1) / 2, 0.052, t, ha="center", va="center",
                     color="#0b1226", fontsize=4.6, fontweight="bold", zorder=6)
    return save(fig, "化妆品类月度销售趋势")


# ---------------------------------------------------------------- 20 多系列折线
def c20():
    fig = new_card("近三年各月销售额月度走势(完)",
                   "上半年同比去年有增长，5月份同比去年最多，增长达40%",
                   "数据来源:营销中心大区数据看板 · 统计口径2023.08.31")
    ax = area(fig, 0.07, 0.13, 0.88, 0.64)
    m = list(range(1, 13))
    d2021 = [320, 380, 460, 520, 610, 680, 720, 760, 690, 640, 560, 480]
    d2022 = [280, 340, 520, 610, 740, 820, 690, 720, 810, 780, 690, 610]
    d2023 = [420, 480, 560, 640, 760, 880, 950, 920, 1010, 860, 740, 620]
    ax.plot(m, d2021, color=CYAN, lw=1.3, label="2021年")
    ax.plot(m, d2022, color=YELLOW, lw=1.3, label="2022年")
    ax.plot(m, d2023, color=PINK, lw=1.6, label="2023年")
    for d, c in ((d2021, CYAN), (d2022, YELLOW), (d2023, PINK)):
        ax.scatter([5], [d[4]], s=16, color=c, zorder=5)
        ax.annotate(f"{d[4]}", (5, d[4]), textcoords="offset points",
                    xytext=(0, -10), ha="center", color=c, fontsize=4.8)
    ax.set_xlim(0.4, 12.6)
    ax.set_ylim(180, 1200)
    ax.set_xticks(m)
    ax.set_xticklabels([f"{i}月" for i in m], fontsize=5.4)
    ax.tick_params(axis="y", labelsize=5.6)
    gridlines(ax, "y")
    ax.legend(loc="upper left", frameon=False, fontsize=5.4, labelcolor=TICK, ncol=3)
    return save(fig, "近三年各月销售额月度走势")


# ---------------------------------------------------------------- 21 环形进度
def c21():
    fig = new_card("2022年上半年目标完成率",
                   "截至6月30日销售目标完成率为85%",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.06.30")
    ax = polar_area(fig, h=0.60, cy=0.15)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["polar"].set_visible(False)
    val = 85
    ax.bar(np.linspace(0, 2 * np.pi, 200), np.ones(200) * 0.30,
           width=2 * np.pi / 200 * 0.98, color=TRACK, bottom=0.55)
    th = np.linspace(0, 2 * np.pi * val / 100, 200)
    ax.bar(th, np.ones(200) * 0.30, width=2 * np.pi / 200 * 0.98, color=RED, bottom=0.55)
    ax.bar(np.linspace(2 * np.pi * val / 100, 2 * np.pi, 200), np.ones(200) * 0.30,
           width=2 * np.pi / 200 * 0.98, color=PURPLE, bottom=0.55)
    ax.text(0.5, 0.5, f"{val}%", transform=ax.transAxes, ha="center", va="center",
            color=TEXT, fontsize=20, fontweight="bold")
    ax.text(0.5, 0.36, "目标完成", transform=ax.transAxes, ha="center", va="center",
            color=SUB, fontsize=6.5)
    return save(fig, "2022年上半年目标完成率_环形")


# ---------------------------------------------------------------- 22 半圆仪表
def c22():
    fig = new_card("2022年上半年目标完成率",
                   "截至6月30日销售目标完成率为85%",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.06.30")
    ax = polar_area(fig, h=0.56, cy=0.17, polar=False)
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-0.30, 1.25)
    ax.axis("off")
    ax.add_patch(Wedge((0, 0), 1.0, 0, 180, width=0.16, facecolor=TRACK, edgecolor="none"))
    for i, frac in enumerate(np.linspace(0, 1, 49)):
        col = BLUE if i < 24 else "#dfe8f8"
        ax.add_patch(Wedge((0, 0), 1.0, i * 180 / 48, (i + 1) * 180 / 48, width=0.16,
                           facecolor=col, edgecolor="none"))
    ax.text(0, 0.42, "75%", ha="center", va="center", color=TEXT,
            fontsize=20, fontweight="bold")
    ax.text(0, 0.20, "目标完成率", ha="center", va="center", color=SUB, fontsize=6.5)
    return save(fig, "2022年上半年目标完成率_半圆")


# ---------------------------------------------------------------- 23 半环粗条
def c23():
    fig = new_card("2022年上半年目标完成率",
                   "截至6月30日销售目标完成率为85%",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.06.30")
    ax = polar_area(fig, h=0.54, cy=0.16, polar=False)
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.22, 1.22)
    ax.axis("off")
    ax.add_patch(Wedge((0, 0), 1.0, 0, 180, width=0.30, facecolor=TRACK, edgecolor="none"))
    ax.add_patch(Wedge((0, 0), 1.0, 0, 135, width=0.30, facecolor=BLUE, edgecolor="none"))
    ax.text(0, 0.30, "75%", ha="center", va="center", color=TEXT,
            fontsize=19, fontweight="bold")
    ax.text(0, 0.12, "目标完成率", ha="center", va="center", color=SUB, fontsize=6.5)
    return save(fig, "2022年上半年目标完成率_半环")


# ---------------------------------------------------------------- 24 车速表
def c24():
    fig = new_card("2022年6月29日公司整体运营指数良好",
                   "公司整体运营指数76分",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.06.30")
    ax = polar_area(fig, h=0.58, cy=0.15, polar=False)
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-0.55, 1.45)
    ax.axis("off")
    ax.set_aspect("equal")
    segs = [(0, 34, ORANGE), (34, 52, YELLOW), (52, 86, BLUE), (86, 100, RED)]
    for a, b, c in segs:
        ax.add_patch(Wedge((0, 0), 1.02, 180 - a * 1.8, 180 - b * 1.8, width=0.15,
                           facecolor=c, edgecolor="none"))
    for t in range(0, 101, 20):
        ang = np.radians(180 - t * 1.8)
        ax.plot([1.10 * np.cos(ang), 1.20 * np.cos(ang)],
                [1.10 * np.sin(ang), 1.20 * np.sin(ang)], color=SUB, lw=0.9)
        ax.text(1.31 * np.cos(ang), 1.31 * np.sin(ang), str(t), ha="center",
                va="center", color=SUB, fontsize=5.2)
    ang = np.radians(180 - 76 * 1.8)
    ax.plot([0, 0.82 * np.cos(ang)], [0, 0.82 * np.sin(ang)],
            color=TICK, lw=1.4, solid_capstyle="round")
    ax.add_patch(Circle((0, 0), 0.06, facecolor=TICK, edgecolor="none"))
    ax.text(0, 0.32, "76", ha="center", va="center", color=TEXT,
            fontsize=17, fontweight="bold")
    ax.text(0, 0.17, "运营指数", ha="center", va="center", color=SUB, fontsize=5.6)
    return save(fig, "公司整体运营指数")


# ---------------------------------------------------------------- 25 多层环形
def c25():
    fig = new_card("2022年上半年各品类商品销售情况",
                   "口红总销量最高，销量达8.75万，销售额同比增长71%",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.06.30")
    ax = polar_area(fig, h=0.62, cy=0.10, polar=False)
    ax.set_xlim(-1.10, 1.10)
    ax.set_ylim(-1.10, 1.10)
    ax.axis("off")
    layers = [
        ([22, 18, 15, 13, 12, 10, 10], [BLUE, BLUEL, CYAN, GREEN, YELLOW, ORANGE, PURPLE], 1.00, 0.16),
        ([26, 20, 18, 14, 12, 10], [RED, PINK, ORANGE, YELLOW, GREEN, CYAN], 0.82, 0.14),
        ([28, 24, 20, 16, 12], [PURPLE, "#6a5ae0", BLUE, CYAN, YELLOW], 0.66, 0.12),
        ([30, 26, 22, 22], [ORANGE, RED, BLUE, GREEN], 0.52, 0.10),
    ]
    for vals, cols, r, w in layers:
        norm = [v / sum(vals) * 360 for v in vals]
        start = 90
        for v, c in zip(norm, cols):
            ax.add_patch(Wedge((0, 0), r, start - v, start, width=w,
                               facecolor=c, edgecolor=CARD, linewidth=0.8))
            start -= v
    ax.text(0, 0.02, "2023", ha="center", va="center", color=TEXT,
            fontsize=7, fontweight="bold")
    ax.text(0, -0.12, "财年", ha="center", va="center", color=SUB, fontsize=5.4)
    return save(fig, "2022年上半年各品类商品销售情况")


# ---------------------------------------------------------------- 26 玫瑰图
def c26():
    fig = new_card("2021年各部门人数分布",
                   "公司总人数1664，销服部人数最多451，占比29.2%",
                   "数据来源:营销中心大区数据看板 · 统计口径2021.12.31")
    ax = polar_area(fig, h=0.62, cy=0.11)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    labels = ["营销部", "销售部", "技术部", "财务部", "人事部", "客服部", "供应链"]
    vals = [451, 384, 262, 198, 156, 142, 71]
    n = len(vals)
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    r = np.sqrt(np.array(vals) / max(vals)) * 1.0
    cols = [RED, YELLOW, CYAN, GREEN, BLUEL, ORANGE, PURPLE]
    ax.bar(th, r, width=2 * np.pi / n * 0.72, color=cols, alpha=0.95)
    ax.set_ylim(0, 1.32)
    ax.set_xticks(th)
    ax.set_xticklabels(labels, fontsize=5.8)
    ax.set_yticks([])
    ax.spines["polar"].set_visible(False)
    for t, v in zip(th, vals):
        ax.text(t, 1.20, f"{v}\n{v/sum(vals)*100:.1f}%", ha="center", va="center",
                color=TEXT, fontsize=4.6)
    return save(fig, "2021年各部门人数分布")


# ---------------------------------------------------------------- 27 年龄径向条
def c27():
    fig = new_card("2022年上半年年龄分布",
                   "公司平均年龄34.5，25-30岁员工规模居",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.06.30")
    ax = polar_area(fig, h=0.62, cy=0.11)
    ax.set_theta_zero_location("E")
    ax.set_theta_direction(-1)
    labels = ["25岁以下", "25-30岁", "30-35岁", "35-40岁", "40岁以上"]
    vals = [142, 386, 428, 264, 96]
    n = len(vals)
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    cols = [RED, ORANGE, YELLOW, CYAN, BLUE]
    ax.bar(th, np.array(vals) / max(vals) * 1.0, width=2 * np.pi / n * 0.55,
           color=cols, alpha=0.9)
    ax.bar(np.linspace(0, 2 * np.pi, 5), [1.0] * 5, width=2 * np.pi / 5 * 0.55,
           color="none", edgecolor=CARD, linewidth=1.2)
    ax.set_ylim(0, 1.25)
    ax.set_xticks(th)
    ax.set_xticklabels(labels, fontsize=5.8)
    ax.set_yticks([])
    ax.spines["polar"].set_visible(False)
    for t, v in zip(th, vals):
        ax.text(t, 1.13, f"{v}\n{v/sum(vals)*100:.1f}%", ha="center", va="center",
                color=TEXT, fontsize=4.4)
    return save(fig, "2022年上半年年龄分布")


# ---------------------------------------------------------------- 28 极坐标柱
def c28():
    fig = new_card("2022年上半年各部门人数",
                   "公司总人数1664，销服部人数最多451，占比27%",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.06.30")
    ax = polar_area(fig, h=0.62, cy=0.11)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    labels = ["营销部", "销售部", "技术部", "财务部", "人事部", "客服部", "供应链", "法务"]
    vals = [451, 384, 262, 198, 156, 142, 48, 23]
    n = len(vals)
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    cols = [RED, ORANGE, YELLOW, CYAN, BLUE, GREEN, PURPLE, PINK]
    ax.bar(th, np.array(vals) / max(vals) * 1.0, width=2 * np.pi / n * 0.55, color=cols)
    ax.set_ylim(0, 1.35)
    ax.set_xticks(th)
    ax.set_xticklabels(labels, fontsize=5.4)
    ax.set_yticks([])
    ax.spines["polar"].set_visible(False)
    for t, v in zip(th, vals):
        ax.text(t, 1.22, f"{v}", ha="center", va="center", color=TEXT, fontsize=4.6)
    return save(fig, "2022年上半年各部门人数")


# ---------------------------------------------------------------- 29 环形+外圈折线
def c29():
    fig = new_card("2021年各部门人数分布",
                   "公司总人数1664，销服部人数最多451，占比29.2%",
                   "数据来源:营销中心大区数据看板 · 统计口径2021.12.31")
    ax = polar_area(fig, h=0.60, cy=0.11, polar=False)
    ax.set_xlim(-1.12, 1.12)
    ax.set_ylim(-1.05, 1.05)
    ax.axis("off")
    vals = [451, 384, 262, 198, 156, 142, 71]
    cols = [RED, YELLOW, CYAN, GREEN, BLUEL, ORANGE, PURPLE]
    start = 90
    for v, c in zip(vals, cols):
        ext = v / sum(vals) * 360
        ax.add_patch(Wedge((0, 0), 0.46, start - ext, start, width=0.24,
                           facecolor=c, edgecolor=CARD, linewidth=0.8))
        mid = np.radians(start - ext / 2)
        ax.plot([0.54 * np.cos(mid), 0.74 * np.cos(mid)],
                [0.54 * np.sin(mid), 0.74 * np.sin(mid)], color=TICK, lw=0.7)
        ax.text(0.86 * np.cos(mid), 0.86 * np.sin(mid),
                f"{v}\n{v/sum(vals)*100:.1f}%", ha="center", va="center",
                color=TEXT, fontsize=4.8)
        start -= ext
    ax.text(0, 0.02, "1664", ha="center", va="center", color=TEXT,
            fontsize=8, fontweight="bold")
    return save(fig, "2021年各部门人数分布_环形")


# ---------------------------------------------------------------- 30 增长折线
def c30():
    fig = new_card("2022年1-8月商品呈现持续增长状况",
                   "8月份销量最高，订单量达1.01万单",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.08.31")
    ax = area(fig)
    m = np.arange(1, 9)
    v = [3620, 4510, 4890, 5140, 5740, 6160, 6742, 7583]
    ax.plot(m, v, color=BLUE, lw=1.6, marker="o", ms=4, mfc=CARD, mew=1.2)
    ax.fill_between(m, v, 2900, color=BLUE, alpha=0.12)
    ax.set_ylim(2900, 8300)
    ax.set_xticks(m)
    ax.set_xticklabels(["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月"], fontsize=6.2)
    gridlines(ax, "y")
    for xi, vi in zip(m, v):
        ax.annotate(f"{vi:,}", (xi, vi), textcoords="offset points", xytext=(0, 7),
                    ha="center", color=TEXT, fontsize=5.0)
    return save(fig, "2022年1-8月商品呈现持续增长状况")


# ---------------------------------------------------------------- 31 双折线
def c31():
    fig = new_card("2022年1-8月商品呈持续增长状况",
                   "8月份销量最高，订单量达1.01万单",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.08.31")
    ax = area(fig)
    m = np.arange(1, 9)
    v = [3620, 4371, 4890, 5140, 5740, 6162, 6742, 7563]
    ax.plot(m, v, color=BLUE, lw=1.6, marker="o", ms=4, mfc=CARD, mew=1.2)
    ax.set_ylim(3000, 8300)
    ax.set_xticks(m)
    ax.set_xticklabels(["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月"], fontsize=6.2)
    gridlines(ax, "y")
    for xi, vi in zip(m, v):
        ax.annotate(f"{vi:,}", (xi, vi), textcoords="offset points", xytext=(0, 7),
                    ha="center", color=TEXT, fontsize=5.0)
    return save(fig, "2022年1-8月商品呈持续增长状况")


# ---------------------------------------------------------------- 32 双折线同比
def c32():
    fig = new_card("2022年上半年各年月同比去年销量",
                   "上半年同比去年销量最高是华南地区，增长达40%",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.06.30")
    ax = area(fig)
    m = np.arange(1, 7)
    cur = [1389, 1458, 1504, 1880, 2534, 2108]
    last = [1156, 1288, 1402, 1602, 1812, 2244]
    ax.plot(m, cur, color=BLUE, lw=1.7, marker="o", ms=4, label="2022年")
    ax.plot(m, last, color=RED, lw=1.5, marker="s", ms=3.4, label="2021年")
    ax.set_ylim(800, 3100)
    ax.set_xticks(m)
    ax.set_xticklabels(["1月", "2月", "3月", "4月", "5月", "6月"], fontsize=6.2)
    gridlines(ax, "y")
    ax.annotate("", xy=(5, 2534), xytext=(5, 1812),
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.1))
    ax.text(5.15, 2170, "+40%", color=ORANGE, fontsize=5.6, fontweight="bold")
    ax.legend(loc="upper left", frameon=False, fontsize=5.4, labelcolor=TICK, ncol=2)
    return save(fig, "2022年上半年各年月同比去年销量")


# ---------------------------------------------------------------- 33 棒棒糖图
def c33():
    fig = new_card("2023年1-8月公司计划完成率",
                   "公司整体完成率95%，4月份和超7%，2月份同比去年增长40%",
                   "数据来源:营销中心大区数据看板 · 统计口径2023.08.31")
    ax = area(fig, 0.11, 0.17, 0.83, 0.58)
    m = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月"]
    v = [53.98, 49.08, 62.56, 70, 61.36, 58.06, 69.04, 50.40]
    x = np.arange(8)
    cols = [RED if i % 2 == 0 else PURPLE for i in range(8)]
    for xi, vi in zip(x, v):
        ax.plot([xi, xi], [46, vi], color=cols[xi], lw=1.2)
        ax.scatter([xi], [vi], s=22, color=cols[xi], zorder=5)
        ax.text(xi, vi + 2.4, f"{vi}%", ha="center", color=TEXT, fontsize=5.2, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(m, fontsize=6.0)
    ax.set_xlim(-0.6, 7.6)
    ax.set_ylim(44, 80)
    ax.set_yticks([])
    gridlines(ax, "y")
    return save(fig, "2023年1-8月公司计划完成率")


# ---------------------------------------------------------------- 34 多色柱
def c34():
    fig = new_card("2021年商品销售情况",
                   "口红总销量最高同比增长24.13%，同期增长43至35万",
                   "数据来源:营销中心大区数据看板 · 统计口径2021.12.31")
    ax = area(fig)
    cats = ["口红", "面膜", "眼影", "粉底液", "精华", "防晒"]
    vals = [1240, 1420, 980, 2180, 1060, 920]
    bars = ax.bar(cats, vals, width=0.52, color=[BLUEL, GREEN, ORANGE, YELLOW, PURPLE, CYAN])
    ax.set_ylim(0, 2600)
    gridlines(ax, "y")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 45, f"{v:,}",
                ha="center", color=TEXT, fontsize=6.0, fontweight="bold")
    return save(fig, "2021年商品销售情况_多色")


# ---------------------------------------------------------------- 35 半环目标
def c35():
    fig = new_card("2022年上半年目标完成率",
                   "截至6月30日销售目标完成率为85%",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.06.30")
    ax = polar_area(fig, h=0.54, cy=0.16, polar=False)
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.22, 1.22)
    ax.axis("off")
    ax.add_patch(Wedge((0, 0), 1.0, 0, 180, width=0.28, facecolor=CYAN, edgecolor="none"))
    ax.add_patch(Wedge((0, 0), 1.0, 0, 117, width=0.28, facecolor=BLUE, edgecolor="none"))
    ax.text(0, 0.34, "65%", ha="center", va="center", color=TEXT,
            fontsize=19, fontweight="bold")
    ax.text(0, 0.16, "目标完成率", ha="center", va="center", color=SUB, fontsize=6.5)
    return save(fig, "2022年上半年目标完成率_青")


# ---------------------------------------------------------------- 36 圆环分割
def c36():
    fig = new_card("本科及以上学历占比",
                   "6月30日最新统计数据显示本科及以上占比65%",
                   "数据来源:营销中心大区数据看板")
    ax = polar_area(fig, h=0.56, cy=0.14, polar=False)
    ax.set_xlim(-1.12, 1.12)
    ax.set_ylim(-1.12, 1.12)
    ax.axis("off")
    ax.add_patch(Wedge((0, 0), 1.0, -90, -90 + 360 * 0.65, width=0.52,
                       facecolor=CYAN, edgecolor="none"))
    ax.add_patch(Wedge((0, 0), 1.0, -90 + 360 * 0.65, 270, width=0.52,
                       facecolor=BLUE, edgecolor="none"))
    ax.text(0, 0, "65%", ha="center", va="center", color=TEXT,
            fontsize=19, fontweight="bold")
    return save(fig, "本科及以上学历占比")


# ---------------------------------------------------------------- 37 气泡图
def c37():
    fig = new_card("2022年世界人口数量排名Top10",
                   "截止2022年01月世界人口排名TOP10，一带一路世界人口第一",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.06.30")
    ax = polar_area(fig, h=0.58, cy=0.13, polar=False)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    rng = np.random.default_rng(7)
    items = [("中国", 1412, 0.32, 0.62), ("印度", 1408, 0.68, 0.62),
             ("美国", 333, 0.14, 0.22), ("印度尼西亚", 275, 0.46, 0.20),
             ("巴基斯坦", 231, 0.86, 0.22), ("巴西", 214, 0.46, 0.86),
             ("尼日利亚", 213, 0.82, 0.86), ("孟加拉国", 169, 0.15, 0.62),
             ("俄罗斯", 145, 0.68, 0.90), ("墨西哥", 130, 0.90, 0.52)]
    for name, v, x, y in items:
        r = 0.040 + np.sqrt(v / 1412) * 0.135
        ax.add_patch(Circle((x, y), r, facecolor=BLUE, alpha=0.85, edgecolor=CARD, lw=1.0))
        ax.text(x, y + r * 0.15, f"{v}", ha="center", va="center", color=TEXT,
                fontsize=4.8, fontweight="bold")
        ax.text(x, y - r - 0.045, name, ha="center", va="top", color=SUB, fontsize=5.0)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return save(fig, "2022年世界人口数量排名Top10")


# ---------------------------------------------------------------- 38/39 分组柱+折线
def c38():
    fig = new_card("近六年各月销售额及增长率",
                   "平台整体销售额整体下降，但是历年增长率依旧",
                   "数据来源:营销中心大区数据看板 · 统计口径2023.11.21")
    ax = area(fig)
    months = ["7月", "8月", "9月", "10月", "11月"]
    y2023 = [2136, 2342, 2678, 2970, 3188]
    y2022 = [2326, 2240, 2432, 2524, 2802]
    x = np.arange(5)
    ax.bar(x - 0.19, y2023, width=0.34, color=BLUE, label="2023年")
    ax.bar(x + 0.19, y2022, width=0.34, color=CYAN, label="2022年")
    for i, (a, b) in enumerate(zip(y2023, y2022)):
        ax.text(i - 0.19, a + 40, f"{a:,}", ha="center", color=TEXT, fontsize=4.8)
        ax.text(i + 0.19, b + 40, f"{b:,}", ha="center", color=TEXT, fontsize=4.8)
    ax.set_ylim(0, 4100)
    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=6.2)
    gridlines(ax, "y")
    ax.tick_params(axis="y", labelsize=5.6)
    for i, g in enumerate([-8.9, 8.6, 1.4, 17.7, 13.8]):
        col = RED if g < 0 else GREEN
        ax.text(i, 3750, f"{g:+.1f}%", ha="center", color=col, fontsize=5.2, fontweight="bold")
        ax.annotate("", xy=(i, 3620), xytext=(i, 3520),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.0))
    ax.legend(loc="upper left", frameon=False, fontsize=5.4, labelcolor=TICK, ncol=2)
    return save(fig, "近六年各月销售额及增长率")


def c39():
    fig = new_card("近六年销售额及增长率",
                   "平台整体销售额整体下降，但是历年增长率依旧",
                   "数据来源:营销中心大区数据看板 · 统计口径2023.11.21")
    ax = area(fig)
    months = ["7月", "8月", "9月", "10月", "11月"]
    y2023 = [2136, 2342, 2678, 2970, 3188]
    y2022 = [2326, 2240, 2432, 2524, 2802]
    x = np.arange(5)
    ax.bar(x - 0.19, y2023, width=0.34, color=BLUE, label="2023年")
    ax.bar(x + 0.19, y2022, width=0.34, color=CYAN, label="2022年")
    ax.set_ylim(0, 4100)
    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=6.2)
    gridlines(ax, "y")
    ax.tick_params(axis="y", labelsize=5.6)
    for i, g in enumerate([-8.9, 8.6, 1.4, 17.7, 13.8]):
        col = RED if g < 0 else GREEN
        ax.scatter([i], [3560], marker="v" if g < 0 else "^", s=26, color=col, zorder=6)
        ax.text(i, 3700, f"{g:+.1f}%", ha="center", color=col, fontsize=5.2, fontweight="bold")
    ax.legend(loc="upper left", frameon=False, fontsize=5.4, labelcolor=TICK, ncol=2)
    return save(fig, "近六年销售额及增长率")


# ---------------------------------------------------------------- 40 横向条+气泡
def c40():
    fig = new_card("2023年各品牌漂亮促分布情况",
                   "各美妆的爆款数量再创新高，其中高姿有两个品牌登数位居首位",
                   "数据来源:营销中心大区数据看板 · 统计口径2023.12.31")
    ax = area(fig, 0.20, 0.14, 0.72, 0.62)
    cats = ["高姿", "花西子", "自然堂", "百雀羚", "珀莱雅", "完美日记"]
    vals = [15600, 12400, 8600, 7400, 5200, 4100]
    y = np.arange(len(cats))
    bars = ax.barh(y, vals, height=0.42, color=BLUE)
    for b, v in zip(bars, vals):
        ax.text(v + 300, b.get_y() + b.get_height() / 2, f"{v:,}", va="center",
                color=TEXT, fontsize=5.4)
    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=6.2)
    ax.invert_yaxis()
    ax.set_xlim(0, 19500)
    ax.set_xticks([])
    gridlines(ax, "x")
    return save(fig, "2023年各品牌情况")


# ---------------------------------------------------------------- 41 分组柱+箭头
def c41():
    fig = new_card("2021年各区域销售额及同比情况",
                   "相关区域销售额连续两年下降，其中华中下降最",
                   "数据来源:营销中心大区数据看板 · 统计口径2021.12.31")
    ax = area(fig)
    months = ["1月", "2月", "3月", "4月", "5月"]
    v1 = [2366, 2245, 2706, 2536, 2430]
    v2 = [2066, 2002, 2140, 2266, 2212]
    growth = [-13.3, -11.5, -2.6, -18.0, 5.2]
    x = np.arange(5)
    ax.bar(x - 0.19, v1, width=0.34, color=BLUE, label="2021年")
    ax.bar(x + 0.19, v2, width=0.34, color="#2e9fd8", label="2020年")
    ax.set_ylim(0, 3700)
    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=6.2)
    gridlines(ax, "y")
    ax.tick_params(axis="y", labelsize=5.6)
    for i, (a, b) in enumerate(zip(v1, v2)):
        ax.text(i - 0.19, a + 50, f"{a:,}", ha="center", color=TEXT, fontsize=4.6)
        ax.text(i + 0.19, b + 50, f"{b:,}", ha="center", color=TEXT, fontsize=4.6)
    for i, g in enumerate(growth):
        col = RED if g < 0 else GREEN
        ax.annotate("", xy=(i, 3320), xytext=(i, 3160),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.2))
        ax.text(i, 3420, f"{g:+.1f}%", ha="center", color=col, fontsize=5.4, fontweight="bold")
    ax.legend(loc="upper left", frameon=False, fontsize=5.4, labelcolor=TICK, ncol=2)
    return save(fig, "2021年各区域销售额及同比情况")


# ---------------------------------------------------------------- 42 分组柱+折线
def c42():
    fig = new_card("上半年各月商品销售额同比去年情况",
                   "2022年截至7月销售额整体下降，除个别商品逆势上升",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.07.31")
    ax = area(fig)
    months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月"]
    cur = [2442, 1862, 1963, 2762, 3334, 2962, 2418]
    last = [2180, 1906, 1863, 2486, 2706, 2262, 2263]
    growth = [12.0, -2.3, 5.4, 11.1, 23.2, 31.0, 6.8]
    x = np.arange(7)
    ax.bar(x - 0.19, cur, width=0.34, color=RED, label="2022年")
    ax.bar(x + 0.19, last, width=0.34, color=BLUE, label="2021年")
    ax.set_ylim(0, 4400)
    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=5.8)
    gridlines(ax, "y")
    ax.tick_params(axis="y", labelsize=5.4)
    for i, (a, b) in enumerate(zip(cur, last)):
        ax.text(i - 0.19, a + 60, f"{a:,}", ha="center", color=TEXT, fontsize=4.4)
        ax.text(i + 0.19, b + 60, f"{b:,}", ha="center", color=TEXT, fontsize=4.4)
    ax2 = ax.twinx()
    ax2.set_facecolor("none")
    for s in ax2.spines.values():
        s.set_visible(False)
    ax2.set_ylim(0, 60)
    ax2.plot(x, growth, color=ORANGE, lw=1.5, marker="o", ms=3.6)
    ax2.tick_params(colors=TICK, labelsize=5.6, length=0)
    for xi, g in zip(x, growth):
        ax2.annotate(f"{g}%", (xi, g), textcoords="offset points", xytext=(0, 6),
                     ha="center", color=ORANGE, fontsize=4.6, fontweight="bold")
    ax.legend(loc="upper left", frameon=False, fontsize=5.2, labelcolor=TICK, ncol=2)
    return save(fig, "上半年各月商品销售额同比去年情况")


# ---------------------------------------------------------------- 43 迷你折线
def c43():
    fig = new_card("近六年销售量及增长率",
                   "平台整体销售额整体下降，但是历年增长率依旧",
                   "数据来源:营销中心大区数据看板 · 统计口径2023.11.21")
    months = ["7月", "8月", "9月", "10月", "11月"]
    v1 = [2136, 2242, 2536, 2970, 3188]
    v2 = [2326, 2240, 2432, 2524, 2802]
    growth = [-8.9, 8.6, 1.4, 17.7, 13.8]
    for i, m in enumerate(months):
        left = 0.06 + i * 0.185
        ax = fig.add_axes([left, 0.32, 0.165, 0.34])
        ax.set_facecolor("none")
        for s in ax.spines.values():
            s.set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.bar([0, 1], [v1[i], v2[i]], width=0.5, color=[BLUE, CYAN])
        ax.set_ylim(0, 4300)
        fig.text(left + 0.082, 0.29, m, ha="center", color=TICK, fontsize=6.0)
        col = RED if growth[i] < 0 else GREEN
        fig.text(left + 0.082, 0.76, f"{growth[i]:+.1f}%", ha="center", color=col,
                 fontsize=5.8, fontweight="bold")
        fig.text(left + 0.082, 0.70, "▲" if growth[i] > 0 else "▼", ha="center",
                 color=col, fontsize=5.0)
    return save(fig, "近六年销售量及增长率_迷你")


# ---------------------------------------------------------------- 44 分组柱+圆标
def c44():
    fig = new_card("各区域上半年销量同比",
                   "华东区域销售同比增长明显，华东和中南领跑销量最多",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.06.30")
    ax = area(fig, 0.19, 0.15, 0.72, 0.60)
    cats = ["华东", "华西", "华北", "华中", "华南", "西南"]
    cur = [112, 94, 86, 76, 102, 68]
    last = [96, 82, 78, 70, 88, 60]
    growth = [16.7, 14.6, 10.3, 8.6, 15.9, 13.3]
    y = np.arange(len(cats))
    ax.barh(y - 0.17, last, height=0.30, color=BLUE, label="2021年")
    ax.barh(y + 0.17, cur, height=0.30, color=RED, label="2022年")
    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=6.2)
    ax.set_xlim(0, 148)
    ax.set_xticks([])
    ax.invert_yaxis()
    for i, g in enumerate(growth):
        ax.add_patch(Circle((131, i), 4.6, facecolor=BLUE, edgecolor="none"))
        ax.text(131, i, f"{g}%", ha="center", va="center", color=TEXT,
                fontsize=4.8, fontweight="bold")
    ax.legend(loc="lower right", frameon=False, fontsize=5.2, labelcolor=TICK, ncol=2,
              bbox_to_anchor=(1.0, -0.02))
    return save(fig, "各区域上半年销量同比")


# ---------------------------------------------------------------- 45 折线+分组柱
def c45():
    fig = new_card("下半年各月对比去年销量",
                   "2024年指标对比去年销量增长明显，其中同比超20%最多",
                   "数据来源:营销中心大区数据看板 · 统计口径2024.06.30")
    ax = area(fig)
    months = ["8月", "9月", "10月", "11月", "12月"]
    v2023 = [1018, 1152, 1240, 1318, 1420]
    v2024 = [862, 1092, 1218, 1352, 1668]
    last24 = [892, 1058, 1190, 1240, 1320]
    x = np.arange(5)
    ax.bar(x - 0.19, v2024, width=0.34, color=BLUE, label="2024年")
    ax.bar(x + 0.19, last24, width=0.34, color=RED, label="2023年")
    ax.plot(x, v2023, color=YELLOW, lw=1.6, marker="o", ms=3.6, label="2023年月均")
    ax.set_ylim(0, 2250)
    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=6.2)
    gridlines(ax, "y")
    ax.tick_params(axis="y", labelsize=5.4)
    growth = [15.9, 9.4, 17.6, 19.0, 15.1]
    for i, g in enumerate(growth):
        ax.text(i, 2080, f"{g}%", ha="center", color=GREEN, fontsize=5.2, fontweight="bold")
    for i, (a, b) in enumerate(zip(v2024, last24)):
        ax.text(i - 0.19, a + 45, f"{a:,}", ha="center", color=TEXT, fontsize=4.4)
        ax.text(i + 0.19, b + 45, f"{b:,}", ha="center", color=TEXT, fontsize=4.4)
    ax.legend(loc="upper left", frameon=False, fontsize=5.2, labelcolor=TICK, ncol=3)
    return save(fig, "下半年各月对比去年销量")


# ---------------------------------------------------------------- 46 柱+黄折线
def c46():
    fig = new_card("年度销售额同比分析",
                   "2023年7月和2022年销售业绩同步达成，但下半年回落",
                   "数据来源:营销中心大区数据看板 · 统计口径2023.12.31")
    ax = area(fig)
    months = ["7月", "8月", "9月", "10月", "11月", "12月"]
    v2023 = [1262, 1392, 1368, 1189, 1180, 1180]
    v2022 = [1066, 1192, 1268, 1442, 1358, 1141]
    growth = [0, 21.7, 14.9, 21.1, 8.2, 5.7]
    x = np.arange(6)
    ax.bar(x - 0.19, v2023, width=0.34, color=BLUE, label="2023年")
    ax.bar(x + 0.19, v2022, width=0.34, color="#2e9fd8", label="2022年")
    gy = [g * 62 + 1900 for g in growth]
    ax.plot(x, gy, color=YELLOW, lw=1.6, marker="o", ms=3.8)
    ax.set_ylim(0, 3800)
    ax.set_yticks([0, 500, 1000, 1500])
    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=6.0)
    gridlines(ax, "y")
    ax.tick_params(axis="y", labelsize=5.4)
    for i, g in enumerate(gy):
        ax.text(i, g + 140, f"{growth[i]}%", ha="center", color=YELLOW,
                fontsize=5.0, fontweight="bold")
    ax.legend(loc="upper left", frameon=False, fontsize=5.2, labelcolor=TICK, ncol=2)
    return save(fig, "年度销售额同比分析")


# ---------------------------------------------------------------- 47 横向条+圆标
def c47():
    fig = new_card("各区域上半年销量同比",
                   "东北区域销量同比增长第一，华东和中南领跑销量最多",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.06.30")
    ax = area(fig, 0.19, 0.15, 0.72, 0.60)
    cats = ["东北", "华东", "华中", "华南", "华西", "西北", "西南"]
    vals = [4634, 4266, 3898, 3534, 2714, 2254, 1962]
    growth = [22.9, 20.0, 13.6, 12.9, 9.3, 8.6, 7.1]
    y = np.arange(len(cats))
    bars = ax.barh(y, vals, height=0.44, color=RED)
    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=6.2)
    ax.set_xlim(0, 5700)
    ax.set_xticks([])
    ax.invert_yaxis()
    gridlines(ax, "x")
    for i, (v, g) in enumerate(zip(vals, growth)):
        ax.text(v + 90, i, f"{v:,}", va="center", color=TEXT, fontsize=5.4)
        ax.add_patch(Circle((5300, i), 5.4, facecolor=BLUE, edgecolor="none"))
        ax.text(5300, i, f"{g}%", ha="center", va="center", color=TEXT,
                fontsize=4.8, fontweight="bold")
    return save(fig, "各区域上半年销量同比_红条")


# ---------------------------------------------------------------- 48 横向条+括号
def c48():
    fig = new_card("各区域上半年销量同比",
                   "东北区域销量同比增长第一，销量和增长率平衡",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.06.30")
    ax = area(fig, 0.20, 0.15, 0.70, 0.60)
    cats = ["东北", "华东", "华中", "华南", "华西", "西南"]
    vals = [68, 57, 46, 34, 26, 20]
    y = np.arange(len(cats))
    bars = ax.barh(y, vals, height=0.44, color=BLUE)
    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=6.2)
    ax.set_xlim(0, 88)
    ax.set_xticks([])
    ax.invert_yaxis()
    for i, v in enumerate(vals):
        ax.text(v + 1.4, i, f"{v}", va="center", color=TEXT, fontsize=5.6)
    ax.annotate("", xy=(80, -0.5), xytext=(80, 5.5),
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.9))
    for i, g in enumerate([22.9, 18.6, 12.9, 9.7, 6.4]):
        ax.text(83, i, f"{g}%", va="center", color=ORANGE, fontsize=5.8, fontweight="bold")
    ax.text(80, 6.0, "同比去年", ha="center", color=ORANGE, fontsize=5.4)
    return save(fig, "各区域上半年销量同比_括号")


# ---------------------------------------------------------------- 49 斜率图
def c49():
    fig = new_card("各区域上半年销量同比",
                   "东北区域销量同比增长第一，销量和增长率平衡",
                   "数据来源:营销中心大区数据看板 · 统计口径2022.06.30")
    ax = area(fig, 0.16, 0.16, 0.76, 0.58)
    cats = ["华东", "华西", "华北", "华中", "华南", "西南", "东北"]
    v2021 = [2266, 1866, 2412, 2204, 2198, 1142, 1682]
    v2022 = [2426, 1942, 2534, 2282, 2314, 1268, 2046]
    y = np.arange(len(cats))
    ax.hlines(y, v2021, v2022, color=BLUE, lw=2.0, alpha=0.75)
    ax.scatter(v2021, y, s=34, color=GRAYD, zorder=5)
    ax.scatter(v2022, y, s=40, color=BLUE, zorder=6)
    for i, (a, b) in enumerate(zip(v2021, v2022)):
        ax.text(a - 70, i, f"{a:,}", va="center", ha="right", color=TICK, fontsize=5.0)
        ax.text(b + 70, i, f"{b:,}", va="center", ha="left", color=TEXT,
                fontsize=5.0, fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=6.2)
    ax.set_xlim(800, 3100)
    ax.set_xticks([])
    ax.invert_yaxis()
    return save(fig, "各区域上半年销量同比_斜率")


ALL = [c01, c02, c03, c04, c05, c06, c07, c08, c09, c10,
       c11, c12, c13, c14, c15, c16, c17, c18, c19, c20,
       c21, c22, c23, c24, c25, c26, c27, c28, c29, c30,
       c31, c32, c33, c34, c35, c36, c37, c38, c39, c40,
       c41, c42, c43, c44, c45, c46, c47, c48, c49]

if __name__ == "__main__":
    for fn in ALL:
        fn()
    print(f"generated {len(ALL)} charts -> {OUT}")