本研究全程未使用任何爬虫技术，严格采用课程白名单方式获取数据：

1. **主数据源——官方一次性下载文件**：通过UCI Machine Learning Repository数据集页面提供的官方静态下载链接（archive.ics.uci.edu/static/public/296/...zip）直接下载ZIP压缩包，解压后得到diabetic_data.csv（18.3MB）与IDS_mapping.csv字段映射表；
2. **辅助数据源——政府/国际组织开放平台公开数据文件**：通过世界银行官方数据API（api.worldbank.org/v2/country/USA/indicator/SH.XPD.CHEX.PC.CD）以JSON格式下载公开指标序列；
3. 未使用Scrapy、Selenium、requests网页解析、模拟登录等任何形式的网页抓取行为；未使用Kaggle CLI以外的任何非官方镜像。

获取日期均为2026年10月29日，原始文件完整保存于项目仓库data/raw/目录，可供复查校验。
