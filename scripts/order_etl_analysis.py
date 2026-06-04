import os
import shutil
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, sum, count, desc, format_number

# --- 环境准备 ---
# 如果 output 文件夹已存在，先删除它，防止 Spark 写入时报错 (FileAlreadyExistsException)
if os.path.exists("output"):
    shutil.rmtree("output")

# 初始化 Spark Session，使用本地所有核心运行
spark = SparkSession.builder.appName("EcommerceOrderETL").master("local[*]").getOrCreate()

# --- 1. 数据读取与预览 ---
# 读取 CSV 文件，自动识别表头，指定 UTF-8 编码
df_raw = spark.read.option("header", "true").option("encoding", "utf-8").csv("data/order_data.csv")
print("原始订单数据预览：")
df_raw.show(8, truncate=False)

# --- 2. 数据清洗 (ETL) ---
# 新增一列 'order_date' (仅提取日期部分用于按天统计)
# 过滤掉金额为 0 或负数的异常数据
df_clean = df_raw.withColumn("order_date", to_date(col("create_time"))) \
                 .filter(col("order_amount") > 0)

# --- 3. 业务分析 ---

# 分析 A: 各品类营收排行 (按总销售额降序)
cate_sales = df_clean.groupBy("category") \
    .agg(
        format_number(sum("order_amount"), 2).alias("total_sales"), # 格式化金额保留2位小数
        count("order_id").alias("order_cnt")                        # 统计订单量
    ) \
    .orderBy(desc("total_sales"))

# 分析 B: 支付方式统计
pay_stat = df_clean.groupBy("pay_type").count()

# 分析 C: 每日营收趋势
day_revenue = df_clean.groupBy("order_date") \
    .agg(format_number(sum("order_amount"), 2).alias("day_income")) \
    .orderBy("order_date")

# --- 4. 结果展示 ---
print("===== 商品品类营收排行 =====")
cate_sales.show()
print("===== 支付方式订单统计 =====")
pay_stat.show()
print("===== 每日营收数据 =====")
day_revenue.show()

# --- 5. 结果保存 ---
# 将分析结果保存为 CSV 文件，模式设为 overwrite (覆盖)
# header=True 表示保存时包含列名
cate_sales.write.mode("overwrite").csv("output/category_sales", header=True, encoding="utf-8")
pay_stat.write.mode("overwrite").csv("output/payment_stats", header=True, encoding="utf-8")
day_revenue.write.mode("overwrite").csv("output/daily_revenue", header=True, encoding="utf-8")

print("分析完成，结果已保存到 output 目录")

# 停止 Spark 会话，释放资源
spark.stop()