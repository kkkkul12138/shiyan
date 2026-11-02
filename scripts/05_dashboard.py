# -*- coding: utf-8 -*-
"""05_dashboard.py 交互式可视化大屏（Pyecharts 全 Python 实现，暗色主题）
组件：KPI卡 ×5 + 年龄再入院柱状(联动源) + 诊断构成饼图(联动目标，点击柱下钻)
     + 卫生支出预测折线 + 诊疗漏斗 + 同期群热力 + 关联规则散点 + 诊断雷达
联动：点击左侧柱图的年龄段 → 右侧饼图切换为该年龄段的诊断构成（下钻）
输出：outputs/dashboard.html（双击即可在浏览器打开，无需服务器）"""
import json
import pandas as pd
from pathlib import Path
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Line, Funnel, HeatMap, Scatter, Radar
from pyecharts.commons.utils import JsCode

BASE = Path(__file__).resolve().parent.parent
CLEAN = BASE / "data" / "clean"
TAB = BASE / "outputs" / "tables"
FIGDIR = BASE / "outputs" / "figures"

df = pd.read_csv(CLEAN / "encounters_clean.csv")
kpi = json.load(open(TAB / "kpi_summary.json", encoding="utf-8"))
wb = pd.read_csv(CLEAN / "us_health_expenditure.csv")
fc = pd.read_csv(TAB / "model6_sarima_forecast.csv")
fun = pd.read_csv(TAB / "model5_funnel.csv")
cohort = pd.read_csv(TAB / "model3_cohort_readmit_rate.csv", index_col=0)
rules = pd.read_csv(TAB / "model4_apriori_rules.csv")

BG, CARD, TEXT = "#eef2f8", "#ffffff", "#22344d"
SUB = "#5a6b80"
GRID = {"left": "6%", "right": "5%", "containLabel": True}  # 通用边距：标签不溢出卡片
age_order = sorted(df["age_group"].unique(), key=lambda s: int(s.split("-")[0]))
C = ["#2E6FB7", "#E8833A", "#4CAF7D", "#C0504D", "#9B59B6", "#16A085", "#F1C40F", "#7F8C8D"]

def base():
    """图表初始化：宽度跟随格子自适应，高度330px，明亮主题"""
    return opts.InitOpts(width="100%", height="330px", bg_color=CARD, theme="white")

def fit_grid(chart, top=58, bottom=48):
    """为图表设置安全边距，防止坐标轴/图例溢出卡片"""
    g = dict(GRID); g["top"] = top; g["bottom"] = bottom
    chart.options["grid"] = g
    return chart

# ---------- 组件1：年龄段再入院率柱状图（联动源） ----------
rate = df.groupby("age_group")["readmit_30d"].mean().reindex(age_order) * 100
bar = Bar(init_opts=base()).add_xaxis(age_order).add_yaxis(
    "30天再入院率%", [round(v, 1) for v in rate.values],
    itemstyle_opts=opts.ItemStyleOpts(color=C[0])).set_global_opts(
    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
    legend_opts=opts.LegendOpts(is_show=False),
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=10, margin=10)),
    title_opts=opts.TitleOpts(title="年龄段30天再入院率（点击柱子下钻诊断构成）", pos_left="center",
                              title_textstyle_opts=opts.TextStyleOpts(color=TEXT, font_size=13)))
fit_grid(bar, top=50, bottom=42)  # 年龄段标签短，横排即可，无需旋转

# ---------- 组件2：诊断构成饼图（联动目标） ----------
overall = (df["diag_1_group"].value_counts(normalize=True).head(6) * 100).round(1)
pie = Pie(init_opts=base()).add(
    "诊断构成", [(k, float(v)) for k, v in overall.items()],
    radius=["38%", "62%"], label_opts=opts.LabelOpts(formatter="{b}: {d}%", color=TEXT, font_size=10)
).set_global_opts(title_opts=opts.TitleOpts(title="主诊断构成：全部患者（随左图点击联动）", pos_left="center",
                                            title_textstyle_opts=opts.TextStyleOpts(color=TEXT, font_size=13)),
                  legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color=TEXT), pos_bottom="0%"))

# 联动数据：各年龄段诊断构成（Top5 + 其他）
drill = {}
for age in age_order:
    sub = df[df["age_group"] == age]["diag_1_group"].value_counts(normalize=True).head(5)
    data = [(k, round(float(v) * 100, 1)) for k, v in sub.items()]
    other = round(100 - sum(v for _, v in data), 1)
    if other > 0.1:
        data.append(("其他", other))
    drill[age] = data
drill_js = json.dumps(drill, ensure_ascii=False)
# 饼图主体下移并缩小，给标题与底部图例留出空间
pie.options["series"][0]["center"] = ["50%", "54%"]
pie.options["series"][0]["radius"] = ["34%", "56%"]

# ---------- 组件3：世行支出 + SARIMA 预测折线 ----------
line = Line(init_opts=base()).add_xaxis([str(y) for y in wb["year"]] + [str(y) for y in fc["year"]]).add_yaxis(
    "历史实际值", [round(float(v), 0) for v in wb["expenditure_usd"]], is_smooth=True,
    linestyle_opts=opts.LineStyleOpts(width=2.5, color=C[1]), itemstyle_opts=opts.ItemStyleOpts(color=C[1]),
    label_opts=opts.LabelOpts(is_show=False),
    symbol_size=5,
).add_yaxis(
    "SARIMA预测(95%CI见明细表)", [None] * len(wb) + [round(float(v), 0) for v in fc["预测值(美元/人)"]],
    is_smooth=True, linestyle_opts=opts.LineStyleOpts(width=2.5, type_="dashed", color=C[3]),
    itemstyle_opts=opts.ItemStyleOpts(color=C[3]),
    label_opts=opts.LabelOpts(is_show=False),
    symbol_size=6,
).set_global_opts(
    title_opts=opts.TitleOpts(
        title="美国人均卫生支出及SARIMA预测\n（回测MAPE=%.2f%%）" % kpi["sarima_MAPE%"],
        pos_left="center", pos_top="2%",
        title_textstyle_opts=opts.TextStyleOpts(color=TEXT, font_size=13)),
    tooltip_opts=opts.TooltipOpts(trigger="axis"),
    legend_opts=opts.LegendOpts(pos_bottom="0%", textstyle_opts=opts.TextStyleOpts(color=TEXT)),
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=4)))
fit_grid(line, top=78, bottom=56)  # 双行标题 + 底部图例都需要留白

# ---------- 组件4：诊疗路径漏斗 ----------
funnel = Funnel(init_opts=base()).add(
    "诊疗路径", [(r["阶段"], int(r["人数"])) for _, r in fun.iterrows()],
    sort_="descending", gap=4,
    label_opts=opts.LabelOpts(formatter="{b}: {c}人", color="#ffffff", font_size=10, position="inside"),
).set_global_opts(
    legend_opts=opts.LegendOpts(is_show=False),  # 层内标签已完整，避免图例压住底层
    title_opts=opts.TitleOpts(
        title="糖尿病住院诊疗路径漏斗",
        subtitle="A1C检测率仅%.1f%%，为路径最大瓶颈" % kpi["funnel_A1C检测率%"],
        pos_left="center", pos_top="2%",
        title_textstyle_opts=opts.TextStyleOpts(color=TEXT, font_size=13),
        subtitle_textstyle_opts=opts.TextStyleOpts(color=SUB, font_size=11)))
# 漏斗最宽层下移并收窄，避免压住标题
funnel.options["series"][0]["top"] = "30%"
funnel.options["series"][0]["bottom"] = "6%"
funnel.options["series"][0]["left"] = "12%"
funnel.options["series"][0]["width"] = "76%"

# ---------- 组件5：同期群热力图 ----------
heat = HeatMap(init_opts=base()).add_xaxis(list(cohort.columns)).add_yaxis(
    "再入院率%", list(cohort.index),
    [[j, i, round(float(cohort.iloc[i, j]) * 100, 1)] for i in range(len(cohort)) for j in range(cohort.shape[1])],
    label_opts=opts.LabelOpts(is_show=False),
).set_global_opts(
    title_opts=opts.TitleOpts(title="同期群：年龄 × 既往住院次数 再入院率热力", pos_left="center",
                              title_textstyle_opts=opts.TextStyleOpts(color=TEXT, font_size=13)),
    visualmap_opts=opts.VisualMapOpts(min_=0, max_=40, pos_bottom="0%", textstyle_opts=opts.TextStyleOpts(color=TEXT)),
    xaxis_opts=opts.AxisOpts(name="既往住院次数"), yaxis_opts=opts.AxisOpts(name="年龄", type_="category"))
fit_grid(heat, top=52, bottom=70)  # 底部要容纳 visualmap 与轴名称

# ---------- 组件6：关联规则散点（支持度×置信度，大小=lift） ----------
rules_biz = rules[~rules["consequents"].isin(["A1C异常", "A1C已检测"])].sort_values("lift", ascending=False).reset_index(drop=True)
# 用 dataIndex 索引 JS 数组承载规则名/lift，规避 pyecharts 散点多维数据的限制
RULE_TIPS = json.dumps([f"{r['antecedents']}→{r['consequents']}<br/>支持度={r['support']:.3f}，置信度={r['confidence']*100:.1f}%<br/>lift={r['lift']:.2f}"
                        for _, r in rules_biz.iterrows()], ensure_ascii=False)
RULE_LIFTS = json.dumps([float(r["lift"]) for _, r in rules_biz.iterrows()])
scatter = Scatter(init_opts=base()).add_xaxis([round(float(v), 3) for v in rules_biz["support"]]).add_yaxis(
    "关联规则", [round(float(v) * 100, 1) for v in rules_biz["confidence"]],
    symbol_size=JsCode(f"function(value, params){{ return RULE_LIFTS[params.dataIndex] * 22; }}"),
    label_opts=opts.LabelOpts(is_show=False),
    tooltip_opts=opts.TooltipOpts(formatter=JsCode("function(p){ return RULE_TIPS[p.dataIndex]; }")),
).set_global_opts(
    title_opts=opts.TitleOpts(title="临床标志关联规则（气泡=Lift，悬停看明细）", pos_left="center",
                              title_textstyle_opts=opts.TextStyleOpts(color=TEXT, font_size=13)),
    xaxis_opts=opts.AxisOpts(name="支持度", min_=0, max_=0.4), yaxis_opts=opts.AxisOpts(name="置信度%", min_=0, max_=90))
fit_grid(scatter, top=52, bottom=56)

# ---------- 组件7：诊断大类雷达 ----------
radar_groups = ["循环系统", "呼吸系统", "消化系统", "糖尿病", "泌尿生殖系统", "损伤中毒"]
met = df[df["diag_1_group"].isin(radar_groups)].groupby("diag_1_group").agg(
    就诊量=("encounter_id", "count"), 平均住院日=("time_in_hospital", "mean"),
    再入院率=("readmit_30d", "mean"), 平均用药=("num_medications", "mean"),
    平均化验=("num_lab_procedures", "mean"))
met_n = (met - met.min()) / (met.max() - met.min())
radar = Radar(init_opts=base()).add_schema(
    schema=[opts.RadarIndicatorItem(name=n, max_=1) for n in ["就诊量", "平均住院日", "再入院率", "平均用药", "平均化验"]],
    splitarea_opt=opts.SplitAreaOpts(is_show=True),
)
for i, (gname, row) in enumerate(met_n.iterrows()):
    radar.add(gname, [[round(float(v), 3) for v in row]],
              color=C[i % len(C)], linestyle_opts=opts.LineStyleOpts(width=2),
              areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
              label_opts=opts.LabelOpts(is_show=False))
radar.set_global_opts(
    legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color=TEXT), pos_bottom="0%"),
    title_opts=opts.TitleOpts(title="主要诊断大类多维指标雷达（0-1归一化）", pos_left="center",
                              title_textstyle_opts=opts.TextStyleOpts(color=TEXT, font_size=13)))
# 雷达主体下移缩小，避免压住标题与底部图例
radar.options["radar"][0]["center"] = ["50%", "52%"]
radar.options["radar"][0]["radius"] = "58%"

# ---------- 组装 HTML（暗色大屏布局） ----------
charts = [("bar", bar), ("pie", pie), ("line", line), ("funnel", funnel),
          ("heat", heat), ("scatter", scatter), ("radar", radar)]
embeds = {name: ch.render_embed() for name, ch in charts}

cards = [
    ("总就诊数(去重患者)", f"{kpi['总就诊数']:,}"),
    ("30天再入院率", f"{kpi['再入院率%']}%"),
    ("30天再入院人数", f"{kpi['30天再入院人数']:,}"),
    ("平均住院天数", f"{kpi['平均住院天数']}天"),
    ("HbA1c检测率", f"{kpi['funnel_A1C检测率%']}%"),
    ("2028年人均卫生支出预测", f"${kpi['sarima_2028预测']:,.0f}"),
]
cards_html = "".join(
    f'<div class="card"><div class="card-v">{v}</div><div class="card-l">{l}</div></div>' for l, v in cards)

grid = """
<div class="row"><div class="cell">{bar}</div><div class="cell">{pie}</div></div>
<div class="row"><div class="cell">{line}</div><div class="cell">{funnel}</div></div>
<div class="row"><div class="cell">{heat}</div><div class="cell">{scatter}</div></div>
<div class="row"><div class="cell full">{radar}</div></div>
""".format(**embeds)

link_js = f"""
<script>
// 联动：点击年龄段柱状图 → 饼图下钻为该年龄段诊断构成
var DRILL = {drill_js};
var pieChart = echarts.getInstanceByDom(document.getElementById('{charts[1][1].chart_id}'));
var barChart = echarts.getInstanceByDom(document.getElementById('{charts[0][1].chart_id}'));
if (pieChart && barChart) {{
    barChart.on('click', function(params) {{
        var data = DRILL[params.name];
        if (!data) return;
        pieChart.setOption({{
            title: {{text: '主诊断构成：' + params.name + '岁（下钻结果）'}},
            series: [{{data: data.map(function(d) {{ return {{name: d[0], value: d[1]}}; }})}}]
        }});
    }});
}}
</script>"""

echarts_js = (BASE / "assets" / "echarts.min.js").read_text(encoding="utf-8")
assert "</script" not in echarts_js.lower()  # 确保可安全内联

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>糖尿病住院运营商业分析大屏</title>
<script>{echarts_js}</script>
<script>
var RULE_TIPS = {RULE_TIPS};
var RULE_LIFTS = {RULE_LIFTS};
</script>
<style>
  body {{ margin:0; background:{BG}; font-family:"Microsoft YaHei",sans-serif; color:{TEXT}; }}
  .title {{ text-align:center; font-size:22px; font-weight:bold; padding:16px 0 4px; letter-spacing:2px; }}
  .subtitle {{ text-align:center; font-size:12px; color:{SUB}; padding-bottom:10px; }}
  .cards {{ display:flex; gap:14px; justify-content:center; padding:8px 24px 16px; flex-wrap:wrap; }}
  .card {{ background:{CARD}; border:1px solid #d5deea; border-radius:8px; padding:12px 26px; text-align:center; min-width:150px; box-shadow:0 1px 3px rgba(30,60,110,.08); }}
  .card-v {{ font-size:22px; font-weight:bold; color:#2E6FB7; }}
  .card-l {{ font-size:12px; color:{SUB}; margin-top:4px; }}
  .row {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; padding:0 24px 16px; }}
  .cell {{ background:{CARD}; border:1px solid #d5deea; border-radius:8px; padding:10px; min-width:0; overflow:hidden; box-shadow:0 1px 3px rgba(30,60,110,.08); }}
</style>
</head>
<body>
<div class="title">糖尿病住院运营商业分析大屏</div>
<div class="subtitle">数据源：UCI Diabetes 130-US Hospitals（CC BY 4.0）× 世界银行开放数据 ｜ 全 Python（Pyecharts）实现 ｜ 点击左侧柱图可下钻诊断构成</div>
<div class="cards">{cards_html}</div>
{grid}
{link_js}
<script>
// 窗口尺寸变化时让所有图表自适应，防止窄窗口下画布超出格子
window.addEventListener('resize', function () {{
  document.querySelectorAll('div[_echarts_instance_]').forEach(function (d) {{
    var inst = echarts.getInstanceByDom(d);
    if (inst) inst.resize();
  }});
}});
</script>
</body>
</html>"""

out = FIGDIR / "dashboard.html"
out.write_text(html, encoding="utf-8")
print("大屏已生成:", out)
print("组件数：KPI卡×6 + 图表×7（含柱图→饼图点击下钻联动）")
