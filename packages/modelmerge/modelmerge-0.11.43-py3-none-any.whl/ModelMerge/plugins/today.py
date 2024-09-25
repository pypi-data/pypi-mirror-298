import datetime
import pytz

# Plugins 获取日期时间
def get_date_time_weekday():
    tz = pytz.timezone('Asia/Shanghai')  # 为东八区设置时区
    now = datetime.datetime.now(tz)  # 获取东八区当前时间
    weekday = now.weekday()
    weekday_str = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'][weekday]
    return "今天是：" + str(now.date()) + "，现在的时间是：" + str(now.time())[:-7] + "，" + weekday_str