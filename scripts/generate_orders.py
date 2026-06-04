import random
from datetime import datetime, timedelta

# --- 配置区：定义模拟数据的范围和规则 ---
# 生成4000个用户ID (U01000 - U04999)
user_ids = [f"U{str(i).zfill(5)}" for i in range(1000, 5000)]
# 商品品类列表
goods_cate = ["数码", "服饰", "生鲜", "美妆", "家电", "零食"]
# 支付方式列表
pay_type = ["微信", "支付宝", "银行卡", "货到付款"]
# 订单状态列表
order_status = ["已完成", "已取消", "待付款", "退款成功"]

# 设置起始日期和总数据量
start_day = datetime(2025, 1, 1)
total = 100000

print(f"正在生成 {total} 条模拟数据...")

# 打开文件准备写入 (UTF-8编码防止中文乱码)
with open("data/order_data.csv", "w", encoding="utf-8") as f:
    # 写入CSV表头
    f.write("order_id,user_id,category,pay_type,order_amount,order_status,create_time\n")

    for i in range(total):
        # 1. 生成唯一订单号 (ORD + 8位数字)
        oid = f"ORD{str(i).zfill(8)}"
        # 2. 随机抽取用户、品类、支付方式和状态
        uid = random.choice(user_ids)
        cate = random.choice(goods_cate)
        pay = random.choice(pay_type)
        status = random.choice(order_status)

        # 3. 生成随机金额 (9.9 ~ 2999.9)，保留两位小数
        money = round(random.uniform(9.9, 2999.9), 2)

        # 4. 生成随机时间 (从2025-01-01开始往后推0-180天内的任意时刻)
        create_dt = start_day + timedelta(days=random.randint(0, 180), hours=random.randint(0, 23))

        # 将一行数据格式化并写入文件
        f.write(f"{oid},{uid},{cate},{pay},{money},{status},{create_dt.strftime('%Y-%m-%d %H:%M:%S')}\n")

print("10万条模拟电商订单生成完毕 → data/order_data.csv")