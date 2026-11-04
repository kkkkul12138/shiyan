核心代码片段（完整代码见仓库scripts/目录，一键复现入口run_all.py）：

```python
# scripts/02_clean.py 关键清洗逻辑（节选）
df = df.drop_duplicates(subset="patient_nbr", keep="first")  # 患者级去重
df = df[(df["diag_1"] != "?") & (df["diag_2"] != "?") & (df["diag_3"] != "?")]
df = df[~df["discharge_disposition_id"].isin(EXPIRED)]       # 剔除死亡/临终
df["readmit_30d"] = (df["readmitted"] == "<30").astype(int)  # 核心标签

# scripts/03_analysis.py SARIMA 建模与回测（节选）
log_s = np.log(series)
train, test = log_s.iloc[:-5], log_s.iloc[-5:]
model = SARIMAX(train, order=(1, 1, 0)).fit(disp=False)
pred = np.exp(model.get_forecast(5).predicted_mean)
mape = float(np.mean(np.abs((np.exp(test) - pred) / np.exp(test))) * 100)

# scripts/05_dashboard.py 联动逻辑（节选）
barChart.on('click', function(params) {
    pieChart.setOption({series: [{data: DRILL[params.name]}]});
});
```
