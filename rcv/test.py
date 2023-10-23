from datetime import datetime, time

# 定义起始时间和结束时间
start_time = time(6, 0, 0)  # 9:00 AM
end_time = time(19, 0, 0)  # 5:00 PM

# 获取当前时间
now = datetime.now().time()

# 检查当前时间是否在指定的时间段内
if start_time <= now <= end_time:
    print("当前时间在指定的时间段内")
else:
    print("当前时间不在指定的时间段内")
