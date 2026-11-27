# 运行所有图表前，请先执行此公共配置块
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Wedge, Polygon, FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime

# 全局中文与样式配置
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'PingFang SC']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 120


# 数据
regions = ['华北', '华南', '东北', '西北', '西南', '华东']
sales = [2354, 1902, 3524, 2698, 2896, 2563]
x = np.arange(len(regions))

# 创建渐变颜色
cmap = LinearSegmentedColormap.from_list('blue_grad', ['#003366', '#0099FF'])
colors = [cmap(i/len(regions)) for i in range(len(regions))]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(x, sales, color=colors, width=0.6)

# 样式设置
ax.set_xticks(x)
ax.set_xticklabels(regions)
ax.set_title('各区域销售量渐变柱形图', fontsize=14, pad=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 数据标签
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x()+bar.get_width()/2, height+30, f'{int(height)}',
            ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()


regions = ['华北', '华南', '东北', '西北', '西南', '华东']
sales = [2354, 1902, 3524, 2698, 2896, 2563]
avg_value = np.mean(sales)
x = np.arange(len(regions))

fig, ax = plt.subplots(figsize=(10, 6))
# 深色背景
fig.patch.set_facecolor('#16213E')
ax.set_facecolor('#16213E')

bars = ax.bar(x, sales, color='#007ACC', width=0.55)

# 均值线
ax.axhline(y=avg_value, color='#F2C94C', linewidth=2, zorder=0)
ax.text(len(regions)-0.5, avg_value+60, f'平均值：{int(avg_value)}',
        color='#F2C94C', fontsize=10, va='center')

# 数据标签
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x()+bar.get_width()/2, height+40, f'{int(height)}',
            ha='center', va='bottom', color='white', fontsize=10)

# 标题
ax.set_title('3月各区域销量分布', color='white', fontsize=20, fontweight='bold', pad=25)
ax.text(0.5, 0.91, '东北销量最多占比总销量的22%，华南销量最低',
        transform=ax.transAxes, ha='center', color='white', fontsize=14)

# 坐标轴
ax.set_xticks(x)
ax.set_xticklabels(regions, color='white', fontsize=12)
ax.yaxis.set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color('white')

# 备注
fig.text(0.11, 0.05, '*注：数据来源于公司销售系统，统计日期截至2022.03.31',
         color='white', fontsize=9)

plt.subplots_adjust(bottom=0.15, top=0.8)
plt.show()


products = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
sales = [653, 523, 648, 856, 714, 785]
x = np.arange(len(products))

fig, ax = plt.subplots(figsize=(8, 5))

# 渐变色
cmap = LinearSegmentedColormap.from_list('pink_grad', ['#FF99CC', '#FF3399'])

# 绘制圆角柱子
bar_width = 0.6
for i in range(len(products)):
    rect = FancyBboxPatch((x[i]-bar_width/2, 0), bar_width, sales[i],
                          boxstyle="round,pad=0,rounding_size=8",
                          facecolor=cmap(i/len(products)), edgecolor='none')
    ax.add_patch(rect)
    ax.text(x[i], sales[i]+15, str(sales[i]), ha='center', va='bottom', fontsize=9)

ax.set_xlim(-0.8, len(products)-0.2)
ax.set_ylim(0, max(sales)*1.15)
ax.set_xticks(x)
ax.set_xticklabels(products)
ax.set_title('商品销量渐变圆角柱形图', fontsize=14, pad=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()


products = ['口红', '面膜', '隔离', '防晒', '精华', '面霜', '眼影', '气垫']
sales = [9221, 5102, 6571, 5760, 6321, 8612, 2645, 5321]
x = np.arange(len(products))

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(x, sales, color='#2D9CDB', width=0.6)

# 顶部数值标注
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x()+bar.get_width()/2, height+150, f'{int(height)}',
            ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(products)
ax.set_title('各商品销量标注柱形图', fontsize=14, pad=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()


quarters = ['2021Q1', 'Q2', 'Q3', 'Q4', '2022Q1', 'Q2']
sales = [3121, 4086, 4321, 4601, 4936, 4231]
profit = [1020, 1421, 1502, 1623, 1781, 1432]
x = np.arange(len(quarters))

fig, ax = plt.subplots(figsize=(9, 5))

# 堆叠柱形
ax.bar(x, sales, label='销售额', color='#007ACC', width=0.6)
ax.bar(x, profit, bottom=sales, label='利润额', color='#F2994A', width=0.6)

# 数据标签
for i in range(len(quarters)):
    ax.text(x[i], sales[i]/2, str(sales[i]), ha='center', va='center', color='white', fontsize=9)
    ax.text(x[i], sales[i]+profit[i]/2, str(profit[i]), ha='center', va='center', color='white', fontsize=9)

ax.set_xticks(x)
ax.set_xticklabels(quarters)
ax.set_title('季度销售额与利润额层叠柱形图', fontsize=14, pad=15, fontweight='bold')
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()


regions = ['华东', '西北', '东北', '华北', '华南']
sales_2022 = [1215, 1321, 1426, 1531, 2238]
sales_2021 = [1003, 1265, 1531, 1436, 2066]
y = np.arange(len(regions))

fig, ax = plt.subplots(figsize=(10, 5))

# 左右双向条形
ax.barh(y, [-v for v in sales_2022], height=0.6, color='#007ACC', label='2022年')
ax.barh(y, sales_2021, height=0.6, color='#F2C94C', label='2021年')

# 中间标签
ax.set_yticks(y)
ax.set_yticklabels(regions, fontsize=11)
ax.set_xticks([])

# 数值标签
for i, v in enumerate(sales_2022):
    ax.text(-v-40, i, str(v), va='center', ha='right', color='white', fontsize=9)
for i, v in enumerate(sales_2021):
    ax.text(v+40, i, str(v), va='center', ha='left', fontsize=9)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.set_title('各区域两年销量对比蝴蝶图', fontsize=14, pad=15, fontweight='bold')
ax.legend(loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.08))
plt.tight_layout()
plt.show()


regions = ['华东', '西北', '东北', '华北', '华南']
rate_2022 = [36, 31, 18, 13, 9]
rate_2021 = [42, 26, 19, 12, 5]
y = np.arange(len(regions))

fig, ax = plt.subplots(figsize=(9, 5))

ax.barh(y, [-v for v in rate_2022], height=0.6, color='#2D9CDB', label='2022年占比')
ax.barh(y, rate_2021, height=0.6, color='#EB5757', label='2021年占比')

ax.set_yticks(y)
ax.set_yticklabels(regions)
ax.set_xticks([])

for i, v in enumerate(rate_2022):
    ax.text(-v-1, i, f'{v}%', va='center', ha='right', color='white', fontsize=9)
for i, v in enumerate(rate_2021):
    ax.text(v+1, i, f'{v}%', va='center', ha='left', fontsize=9)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.set_title('各区域销售占比两年对比蝴蝶图', fontsize=14, pad=15, fontweight='bold')
ax.text(0.5, 0.93, '华东区域完成率最高达到36%，相比去年的42%有所下降',
        transform=ax.transAxes, ha='center', fontsize=10, color='#666')
ax.legend(loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.1))
plt.tight_layout()
plt.show()


regions = ['华北', '华南', '东北', '西北', '西南', '华东']
sales = [4321, 1946, 1536, 1872, 1369, 2109]
yoy = [-13.6, -20.8, -9.3, -15.9, -17.9, -5.8]
y = np.arange(len(regions))

fig, ax = plt.subplots(figsize=(9, 5))

# 背景占位条
ax.barh(y, [5400]*len(regions), height=0.5, color='#F0F2F5')
# 实际销量条
bars = ax.barh(y, sales, height=0.5, color='#007ACC')

# 同比标签
for i in range(len(regions)):
    ax.text(sales[i]+100, i, f'{yoy[i]}%', va='center', color='#EB5757', fontsize=9)
    ax.text(50, i, str(sales[i]), va='center', color='white', fontsize=9)

ax.set_yticks(y)
ax.set_yticklabels(regions)
ax.set_xticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)

ax.set_title('各区域销量与同比百分比图', fontsize=14, pad=15, fontweight='bold')
plt.tight_layout()
plt.show()


products = ['口红', '面膜', '隔离', '防晒', '精华']
sales_2021 = [3568, 4135, 4436, 4106, 4936]
sales_2022 = [2569, 3241, 2965, 3209, 3541]
diff = [999, 894, 1471, 897, 1395]
x = np.arange(len(products))
width = 0.35

fig, ax = plt.subplots(figsize=(9, 5))

ax.bar(x-width/2, sales_2021, width, label='2021销量', color='#2D9CDB')
ax.bar(x+width/2, sales_2022, width, label='2022销量', color='#F2994A')

# 差值标注
for i in range(len(products)):
    ax.text(x[i], max(sales_2021[i], sales_2022[i])+100,
            f'差值:{diff[i]}', ha='center', fontsize=9, color='#666')

ax.set_xticks(x)
ax.set_xticklabels(products)
ax.set_title('商品两年销量对比柱形图', fontsize=14, pad=15, fontweight='bold')
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()


tasks = ['制定计划', '方案设计', '资源调配', '第一阶段', '第二阶段', '第三阶段', '项目总结']
start_dates = ['2022-03-01', '2022-03-13', '2022-03-22', '2022-04-02',
               '2022-04-16', '2022-05-11', '2022-05-26']
durations = [11, 8, 10, 13, 24, 14, 7]
progress = [0.51, 0.32, 0.21, 0.85, 0.36, 0.68, 0.68]

start_dt = [datetime.strptime(d, '%Y-%m-%d').toordinal() for d in start_dates]
y = np.arange(len(tasks))

fig, ax = plt.subplots(figsize=(11, 6))

# 总时长背景条
ax.barh(y, durations, left=start_dt, height=0.5, color='#E0E6ED', alpha=0.7)
# 已完成进度
for i in range(len(tasks)):
    ax.barh(y[i], durations[i]*progress[i], left=start_dt[i],
            height=0.5, color='#007ACC')

# 日期坐标轴
date_ticks = [datetime(2022,m,1).toordinal() for m in [3,4,5,6]]
ax.set_xticks(date_ticks)
ax.set_xticklabels(['3月', '4月', '5月', '6月'])
ax.set_yticks(y)
ax.set_yticklabels(tasks)

for spine in ['top','right','left']:
    ax.spines[spine].set_visible(False)

ax.set_title('项目进度甘特图', fontsize=14, pad=15, fontweight='bold')
plt.tight_layout()
plt.show()


months = ['21-5', '21-6', '21-7', '21-8', '21-9', '21-10',
          '21-11', '21-12', '22-1', '22-2', '22-3']
sales = [146, 198, 296, 412, 506, 615, 789, 1021, 3782, 3215, 2936]
x = np.arange(len(months))

fig, ax = plt.subplots(figsize=(10, 5))

# 平滑折线（样条插值）
from scipy.interpolate import make_interp_spline
x_smooth = np.linspace(x.min(), x.max(), 300)
y_smooth = make_interp_spline(x, sales)(x_smooth)

ax.plot(x_smooth, y_smooth, color='#007ACC', linewidth=2.5)
ax.fill_between(x_smooth, y_smooth, alpha=0.2, color='#007ACC')

ax.set_xticks(x)
ax.set_xticklabels(months)
ax.set_title('月度销量平滑折线图', fontsize=14, pad=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()


months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月']
rate = [53.6, 49.8, 52.7, 70.8, 60.9, 49.6, 58.6, 70.4]
x = np.arange(len(months))

fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(x, rate, color='#2D9CDB', linewidth=2, marker='D',
        markersize=7, markerfacecolor='white', markeredgewidth=2)

# 数据标签
for i, v in enumerate(rate):
    ax.text(i, v+1.5, f'{v}%', ha='center', fontsize=9)

ax.set_xticks(x)
ax.set_xticklabels(months)
ax.set_title('月度目标完成率菱形走势图', fontsize=14, pad=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()


months = ['1月', '2月', '3月', '4月', '5月', '6月']
sales_2021 = [1686, 1345, 1934, 1658, 1865, 1936]
sales_2022 = [1385, 1846, 1654, 1936, 2564, 2236]
x = np.arange(len(months))

fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(x, sales_2021, marker='o', linewidth=2, label='2021年', color='#2D9CDB')
ax.plot(x, sales_2022, marker='s', linewidth=2, label='2022年', color='#EB5757')

ax.set_xticks(x)
ax.set_xticklabels(months)
ax.set_title('两年月度销量对比折线图', fontsize=14, pad=15, fontweight='bold')
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()


import matplotlib.pyplot as plt
plt.rcParams["font.family"] = ["SimHei"]  # 设置黑体，支持中文
plt.rcParams["axes.unicode_minus"] = False # 解决负号显示异常
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

rate = 85
placeholder = 15

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')

wedges, texts = ax.pie([rate, placeholder],
                       colors=['#007ACC', '#E0E6ED'],
                       startangle=90, counterclock=False,
                       wedgeprops=dict(width=0.3, edgecolor='white'))

ax.text(0, 0, f'{rate}%\n完成率', ha='center', va='center',
        fontsize=20, fontweight='bold')

ax.set_title('销售目标完成率圆环图', fontsize=14, pad=15, fontweight='bold')
plt.tight_layout()
plt.show()


def draw_liquid_gauge(percent, title=''):
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_aspect('equal')
    
    # 外圆背景
    bg = Circle((0.5, 0.5), 0.4, color='#E0E6ED', transform=ax.transAxes)
    ax.add_artist(bg)
    
    # 波浪液面
    x = np.linspace(0.1, 0.9, 300)
    y_base = 0.1 + 0.8 * percent/100
    y_wave = y_base + 0.02 * np.sin(25 * np.pi * x)
    fill = ax.fill_between(x, 0.1, y_wave, color='#007ACC', alpha=0.85)
    
    # 圆形裁剪
    clip = Circle((0.5, 0.5), 0.4, transform=ax.transAxes)
    fill.set_clip_path(clip)
    
    # 中心百分比
    ax.text(0.5, 0.5, f'{percent}%', ha='center', va='center',
            fontsize=32, fontweight='bold', color='white', transform=ax.transAxes)
    
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    ax.axis('off')
    ax.set_title(title, fontsize=14, pad=15, fontweight='bold')
    return fig, ax

fig, ax = draw_liquid_gauge(65, '2022年上半年目标完成率')
fig.text(0.5, 0.08, '*注：数据来源于公司销售系统', ha='center', fontsize=9, color='#666')
plt.tight_layout()
plt.show()


def draw_wave_gauge(percent, title=''):
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_aspect('equal')
    
    bg = Circle((0.5, 0.5), 0.42, color='#F0F2F5', transform=ax.transAxes)
    ax.add_artist(bg)
    
    # 双层波浪效果
    x = np.linspace(0.08, 0.92, 400)
    y_base = 0.08 + 0.84 * percent/100
    
    # 下层波浪
    y1 = y_base + 0.025 * np.sin(20 * np.pi * x + 0.5)
    fill1 = ax.fill_between(x, 0.08, y1, color='#2D9CDB', alpha=0.5)
    
    # 上层波浪
    y2 = y_base + 0.018 * np.sin(28 * np.pi * x)
    fill2 = ax.fill_between(x, 0.08, y2, color='#007ACC', alpha=0.8)
    
    # 圆形裁剪
    clip = Circle((0.5, 0.5), 0.4, transform=ax.transAxes)
    fill1.set_clip_path(clip)
    fill2.set_clip_path(clip)
    
    ax.text(0.5, 0.5, f'{percent}%', ha='center', va='center',
            fontsize=30, fontweight='bold', color='white', transform=ax.transAxes)
    
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    ax.axis('off')
    ax.set_title(title, fontsize=14, pad=15, fontweight='bold')
    return fig, ax

fig, ax = draw_wave_gauge(65, '本科及以上学历员工占比')
fig.text(0.5, 0.08, '*注：数据来源于公司人力资源系统', ha='center', fontsize=9, color='#666')
plt.tight_layout()
plt.show()


ages = ['>=50', '[40,50)', '[30,40)', '[20,30)']
ratios = [12.5, 20.8, 29.2, 37.5]
placeholders = [37.5, 29.2, 20.8, 12.5]
y = np.arange(len(ages))

fig, ax = plt.subplots(figsize=(8, 5))

# 左右对称条形（玉玦效果）
ax.barh(y, [-r for r in ratios], height=0.6, color='#007ACC')
ax.barh(y, placeholders, height=0.6, color='#E0E6ED')

# 中间标签
ax.set_yticks(y)
ax.set_yticklabels(ages, fontsize=11)
ax.set_xticks([])

# 数值标注
for i, v in enumerate(ratios):
    ax.text(-v-1, i, f'{v}%', va='center', ha='right', color='white', fontsize=9)

for spine in ax.spines.values():
    spine.set_visible(False)

ax.set_title('员工年龄分布玉玦图', fontsize=14, pad=15, fontweight='bold')
plt.tight_layout()
plt.show()


depts = ['人力部', '行政部', '财务部', '工程部', '采购部', '销售部']
nums = [130, 226, 238, 293, 326, 451]
total = 832  # 总占位长度
y = np.arange(len(depts))

fig, ax = plt.subplots(figsize=(9, 5))

# 跑道背景（圆角）
for i in range(len(depts)):
    bg = FancyBboxPatch((0, i-0.25), total, 0.5,
                        boxstyle="round,pad=0,rounding_size=10",
                        facecolor='#F0F2F5', edgecolor='none')
    ax.add_patch(bg)
    
    # 实际人数条
    bar = FancyBboxPatch((0, i-0.25), nums[i], 0.5,
                         boxstyle="round,pad=0,rounding_size=10",
                         facecolor='#007ACC', edgecolor='none')
    ax.add_patch(bar)
    
    ax.text(nums[i]+10, i, str(nums[i]), va='center', fontsize=9)

ax.set_xlim(0, total*1.1)
ax.set_ylim(-0.8, len(depts)-0.2)
ax.set_yticks(y)
ax.set_yticklabels(depts)
ax.set_xticks([])

for spine in ax.spines.values():
    spine.set_visible(False)

ax.set_title('各部门人数跑道图', fontsize=14, pad=15, fontweight='bold')
plt.tight_layout()
plt.show()


depts = ['销售部', '采购部', '工程部', '财务部', '行政部', '人力部']
ratios = [29.2, 22.7, 17.5, 13.6, 10.3, 6.7]
colors = ['#007ACC', '#2D9CDB', '#56CCF2', '#82D8F7', '#B0E2FB', '#D9EEFD']

N = len(depts)
theta = np.linspace(0, 2*np.pi, N, endpoint=False)

fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(111, polar=True)

bars = ax.bar(theta, ratios, width=2*np.pi/N, color=colors, edgecolor='white', linewidth=2)

ax.set_xticks(theta)
ax.set_xticklabels(depts, fontsize=10)
ax.set_yticks([])
ax.spines['polar'].set_visible(False)

# 数值标注
for i, bar in enumerate(bars):
    ax.text(theta[i], bar.get_height()+1, f'{ratios[i]}%',
            ha='center', va='bottom', fontsize=9)

ax.set_title('各部门人数占比南丁格尔图', fontsize=14, pad=20, fontweight='bold')
plt.tight_layout()
plt.show()


ages = ['[20,30)', '[30,40)', '[40,50)', '>=50']
ratios = [37.5, 29.2, 20.8, 12.5]
colors = ['#007ACC', '#2D9CDB', '#56CCF2', '#82D8F7']

N = len(ages)
theta = np.linspace(0, 2*np.pi, N, endpoint=False)

fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(111, polar=True)

# 空心圆环：设置底部内半径
inner_radius = 15
bars = ax.bar(theta, ratios, bottom=inner_radius, width=2*np.pi/N,
              color=colors, edgecolor='white', linewidth=2)

ax.set_xticks(theta)
ax.set_xticklabels(ages, fontsize=10)
ax.set_yticks([])
ax.spines['polar'].set_visible(False)

for i, bar in enumerate(bars):
    r = inner_radius + bar.get_height()/2
    ax.text(theta[i], r, f'{ratios[i]}%',
            ha='center', va='center', color='white', fontsize=9, fontweight='bold')

ax.set_title('员工年龄分布南丁格尔圆环图', fontsize=14, pad=20, fontweight='bold')
plt.tight_layout()
plt.show()


depts = ['销售部', '采购部', '工程部', '财务部', '行政部', '人力部']
ratios = [29.2, 22.7, 17.5, 13.6, 10.3, 5.0]
colors = ['#EB5757', '#F2994A', '#F2C94C', '#2D9CDB', '#2F80ED', '#9B51E0']

N = len(depts)
theta = np.linspace(0, 2*np.pi, N, endpoint=False)

fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(111, polar=True)

bars = ax.bar(theta, ratios, width=2*np.pi/N, color=colors, edgecolor='white', linewidth=2)

ax.set_xticks(theta)
ax.set_xticklabels(depts, fontsize=10)
ax.set_yticks([])
ax.spines['polar'].set_visible(False)

for i, bar in enumerate(bars):
    ax.text(theta[i], bar.get_height()+0.8, f'{ratios[i]}%',
            ha='center', va='bottom', fontsize=9)

ax.set_title('2021年各部门人数分布', fontsize=14, pad=20, fontweight='bold')
fig.text(0.5, 0.08, '公司总人数1664，销售部人数最多451，占比29.2%',
         ha='center', fontsize=10, color='#666')
plt.tight_layout()
plt.show()


def draw_gauge(value, min_val=50, max_val=150, title=''):
    fig, ax = plt.subplots(figsize=(8,6))
    ax.set_aspect('equal')
    
    # 背景刻度弧
    bg_wedge = Wedge((0.5, 0.5), 0.4, 180, 360, width=0.08, color='#E0E6ED')
    ax.add_artist(bg_wedge)
    
    # 指针角度计算
    ratio = (value - min_val) / (max_val - min_val)
    angle = np.radians(180 + ratio * 180)
    
    # 指针
    pointer = Polygon([[0.5, 0.5],
                       [0.5+0.35*np.cos(angle), 0.5+0.35*np.sin(angle)]],
                      color='#F2994A', linewidth=3)
    ax.add_artist(pointer)
    ax.scatter(0.5, 0.5, s=120, color='#F2994A', zorder=5)
    
    # 刻度
    for i in range(6):
        val = min_val + i*(max_val-min_val)/5
        ang = np.radians(180 + i*36)
        x = 0.5 + 0.47*np.cos(ang)
        y = 0.5 + 0.47*np.sin(ang)
        ax.text(x, y, str(int(val)), ha='center', va='center', fontsize=9)
    
    # 中心数值
    ax.text(0.5, 0.3, f'{value}', ha='center', va='center',
            fontsize=22, fontweight='bold', color='#333')
    
    ax.set_xlim(0,1)
    ax.set_ylim(0.2, 1)
    ax.axis('off')
    ax.set_title(title, fontsize=14, pad=15, fontweight='bold')
    return fig, ax

fig, ax = draw_gauge(76, title='销售目标完成仪表盘')
plt.tight_layout()
plt.show()


years = ['2017', '2018', '2019', '2020', '2021', '2022']
sales = [1603, 2106, 2406, 3265, 3721, 3921]
growth = [27, 31, 14, 36, 14, 5]
x = np.arange(len(years))

fig, ax1 = plt.subplots(figsize=(9, 5))

# 左轴：柱形
bars = ax1.bar(x, sales, color='#007ACC', width=0.5, label='销售量')
ax1.set_ylabel('销售量', fontsize=10)
ax1.set_xticks(x)
ax1.set_xticklabels(years)

# 右轴：折线
ax2 = ax1.twinx()
line, = ax2.plot(x, growth, color='#F2994A', marker='o', linewidth=2, label='同比增速')
ax2.set_ylabel('同比增速(%)', fontsize=10)

# 数据标签
for bar in bars:
    ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+50,
             f'{int(bar.get_height())}', ha='center', va='bottom', fontsize=9)
for i, v in enumerate(growth):
    ax2.text(i, v+1, f'{v}%', ha='center', va='bottom', fontsize=9, color='#F2994A')

# 合并图例
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1+l2, loc='upper left')

ax1.set_title('历年销售量与同比增速', fontsize=14, pad=15, fontweight='bold')
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

plt.tight_layout()
plt.show()


products = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
actual = [653, 523, 648, 856, 714, 785]
target = [700, 500, 600, 900, 600, 600]
x = np.arange(len(products))
width = 0.35

fig, ax = plt.subplots(figsize=(9, 5))

ax.bar(x-width/2, actual, width, label='实际销量', color='#007ACC')
ax.bar(x+width/2, target, width, label='目标销量', color='#E0E6ED')

# 完成率标注
for i in range(len(products)):
    rate = actual[i]/target[i]
    color = '#27AE60' if rate >=1 else '#EB5757'
    ax.text(x[i], max(actual[i], target[i])+20,
            f'完成率{rate:.1%}', ha='center', fontsize=9, color=color)

ax.set_xticks(x)
ax.set_xticklabels(products)
ax.set_title('商品实际与目标销量对比图', fontsize=14, pad=15, fontweight='bold')
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()


products = ['口红', '面膜', '隔离', '防晒', '精华', '面霜']
actual = [653, 523, 648, 856, 714, 785]
target = [700, 500, 600, 900, 600, 600]
pass_line = 600
good = 200
excellent = 200
y = np.arange(len(products))

fig, ax = plt.subplots(figsize=(10, 5))

# 三档背景
ax.barh(y, pass_line, height=0.6, color='#E0E6ED', label='及格')
ax.barh(y, good, left=pass_line, height=0.6, color='#B0C4DE', label='良好')
ax.barh(y, excellent, left=pass_line+good, height=0.6, color='#87CEEB', label='优秀')

# 实际值
ax.barh(y, actual, height=0.25, color='#007ACC', label='实际')

# 目标线
for i in range(len(products)):
    ax.vlines(target[i], y[i]-0.3, y[i]+0.3, color='#EB5757', linewidth=2, label='目标' if i==0 else "")

ax.set_yticks(y)
ax.set_yticklabels(products)
ax.set_title('商品销量子弹图', fontsize=14, pad=15, fontweight='bold')
ax.legend(loc='lower right', ncol=4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()


regions = ['华北', '华南', '东北', '西北', '西南', '华东']
sales = [2354, 1902, 3524, 2698, 2896, 2563]
total = 4500
yoy = [12, 25, 16, 21, 18, 25]
y = np.arange(len(regions))

fig, ax = plt.subplots(figsize=(9, 5))

# 背景跑道
for i in range(len(regions)):
    bg = FancyBboxPatch((0, i-0.25), total, 0.5,
                        boxstyle="round,pad=0,rounding_size=15",
                        facecolor='#F0F2F5', edgecolor='none')
    ax.add_patch(bg)
    
    # 实际销量柱
    bar = FancyBboxPatch((0, i-0.25), sales[i], 0.5,
                         boxstyle="round,pad=0,rounding_size=15",
                         facecolor='#007ACC', edgecolor='none')
    ax.add_patch(bar)
    
    # 同比标签
    ax.text(sales[i]+80, i, f'同比+{yoy[i]}%', va='center', color='#27AE60', fontsize=9)

ax.set_xlim(0, total*1.15)
ax.set_ylim(-0.8, len(regions)-0.2)
ax.set_yticks(y)
ax.set_yticklabels(regions)
ax.set_xticks([])

for spine in ax.spines.values():
    spine.set_visible(False)

ax.set_title('各区域销量柱形圆图', fontsize=14, pad=15, fontweight='bold')
plt.tight_layout()
plt.show()


regions = ['华北', '华南', '东北', '西北', '西南', '华东']
sales_2022 = [2354, 1902, 3524, 2698, 2896, 2563]
sales_2021 = [2021, 1563, 3213, 2531, 2631, 2361]
yoy = [16, 22, 10, 7, 10, 9]
x = np.arange(len(regions))
width = 0.35

fig, ax1 = plt.subplots(figsize=(10, 5))

# 柱形：两年销量
ax1.bar(x-width/2, sales_2022, width, label='2022销量', color='#007ACC')
ax1.bar(x+width/2, sales_2021, width, label='2021销量', color='#B0E2FB')
ax1.set_ylabel('销售量', fontsize=10)
ax1.set_xticks(x)
ax1.set_xticklabels(regions)

# 折线：同比
ax2 = ax1.twinx()
ax2.plot(x, yoy, color='#F2994A', marker='o', linewidth=2, label='同比去年')
ax2.set_ylabel('同比增速(%)', fontsize=10)

# 数据标签
for i, v in enumerate(yoy):
    ax2.text(i, v+0.5, f'{v}%', ha='center', color='#F2994A', fontsize=9)

h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1+l2, loc='upper left')

ax1.set_title('各区域销量与同比增速', fontsize=14, pad=15, fontweight='bold')
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)

plt.tight_layout()
plt.show()


months = ['1月', '2月', '3月', '4月', '5月', '6月',
          '7月', '8月', '9月', '10月', '11月', '12月']
monthly = [2354, 1902, 3524, 2698, 2896, 2563,
           3156, 2896, 3621, 2635, 2963, 2789]
quarterly = [7780, 7780, 7780, 8157, 8157, 8157,
             9673, 9673, 9673, 8387, 8387, 8387]
x = np.arange(len(months))

fig, ax = plt.subplots(figsize=(11, 5))

# 季度背景大柱
q_colors = ['#E0E6ED']*3 + ['#D0D9E6']*3 + ['#C0CFE0']*3 + ['#B0C4DE']*3
ax.bar(x, quarterly, color=q_colors, width=1, edgecolor='white')

# 月度小柱
ax.bar(x, monthly, color='#007ACC', width=0.6)

# 季度标签
for i in range(4):
    mid = i*3 + 1
    ax.text(mid, quarterly[mid]+50, f'Q{i+1}季度', ha='center', fontsize=10, color='#333')

ax.set_xticks(x)
ax.set_xticklabels(months, fontsize=9)
ax.set_title('月度与季度销量复合柱形图', fontsize=14, pad=15, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()


regions = ['华东', '西北', '东北', '华北', '华南']
finish = [35, 51, 62, 74, 86]
unfinish = [65, 49, 38, 26, 14]
y = np.arange(len(regions))

fig, ax = plt.subplots(figsize=(9, 4))

# 背景未完成条
ax.barh(y, unfinish, left=finish, height=0.3, color='#E0E6ED')
# 完成条
ax.barh(y, finish, height=0.3, color='#007ACC')

# 滑珠（圆点标记）
for i in range(len(regions)):
    ax.scatter(finish[i], y[i], s=150, color='#007ACC', zorder=5, edgecolor='white', linewidth=2)
    ax.text(finish[i]+2, y[i], f'{finish[i]}%', va='center', fontsize=9)

ax.set_yticks(y)
ax.set_yticklabels(regions)
ax.set_xticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)

ax.set_title('各区域目标完成率滑珠图', fontsize=14, pad=15, fontweight='bold')
plt.tight_layout()
plt.show()


regions = ['华东', '西北', '东北', '华北', '华南']
finish_2022 = [35, 51, 62, 74, 86]
finish_2021 = [45, 39, 53, 69, 92]
y = np.arange(len(regions))

fig, ax = plt.subplots(figsize=(9, 5))

# 背景条
total = 100
ax.barh(y+0.15, total, height=0.25, color='#F0F2F5')
ax.barh(y-0.15, total, height=0.25, color='#F0F2F5')

# 两年完成条
ax.barh(y+0.15, finish_2022, height=0.25, color='#007ACC', label='2022年')
ax.barh(y-0.15, finish_2021, height=0.25, color='#F2994A', label='2021年')

# 滑珠
for i in range(len(regions)):
    ax.scatter(finish_2022[i], y[i]+0.15, s=120, color='#007ACC', zorder=5, edgecolor='white')
    ax.scatter(finish_2021[i], y[i]-0.15, s=120, color='#F2994A', zorder=5, edgecolor='white')

ax.set_yticks(y)
ax.set_yticklabels(regions)
ax.set_xticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)

ax.set_title('两年区域完成率对比滑珠图', fontsize=14, pad=15, fontweight='bold')
ax.legend(loc='lower right')
plt.tight_layout()
plt.show()
