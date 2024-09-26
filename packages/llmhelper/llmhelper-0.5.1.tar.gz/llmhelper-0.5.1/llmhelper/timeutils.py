import datetime

__all__ = [
    "get_current_datetime_extra_data",
]


weekdays = [
    ["星期一", "周一", "礼拜一"],
    ["星期二", "周二", "礼拜二"],
    ["星期三", "周三", "礼拜三"],
    ["星期四", "周四", "礼拜四"],
    ["星期五", "周五", "礼拜五"],
    ["星期六", "周六", "礼拜六"],
    ["星期日", "星期天", "周日", "礼拜天", "礼拜日"],
]


def get_weekday_info(nowtime: datetime.datetime, prefix: str = "今天是"):
    return "，".join([prefix + x for x in weekdays[nowtime.weekday()]]) + "。"


def get_day_info(nowtime: datetime.datetime, prefix: str = "今天是"):
    return prefix + nowtime.strftime("%Y年%m月%d日") + "。"


def get_nowtime(nowtime: datetime.datetime, prefix: str = "现在时间是"):
    return prefix + nowtime.strftime("%H时%M分%S秒") + "。"


def get_week_range_info(nowtime: datetime.datetime, prefix: str = "本周时间范围是"):
    today_weekday = nowtime.weekday()
    monday = nowtime - datetime.timedelta(days=today_weekday)
    sunday = nowtime + datetime.timedelta(days=7 - today_weekday - 1)
    return (
        prefix
        + "从"
        + monday.strftime("%Y年%m月%d日")
        + "到"
        + sunday.strftime("%Y年%m月%d日")
        + "。"
    )


def get_year_info(year: int, prefix: str = "今年是"):
    return f"{prefix}{year}年。"


def get_lastn_days_info(
    nowtime: datetime.datetime,
    n: int,
    prefix: str = "最近7天的范围是",
):
    start = nowtime - datetime.timedelta(days=n - 1)
    return (
        prefix
        + "从"
        + start.strftime("%Y年%m月%d日")
        + "至"
        + nowtime.strftime("%Y年%m月%d日")
        + "。"
    )


def get_day_time_range(nowtime: datetime.datetime, prefix="今天的时间范围是"):
    return (
        prefix
        + nowtime.strftime("%y-%m-%d 00:00:00")
        + "至"
        + nowtime.strftime("%y-%m-%d 23:59:59")
    )


def get_current_datetime_extra_data():
    today = datetime.datetime.now()
    tomorrow = today + datetime.timedelta(days=1)
    yesterday = today - datetime.timedelta(days=1)
    last_week = today - datetime.timedelta(days=7)
    next_week = today + datetime.timedelta(days=7)
    return [
        get_day_info(nowtime=today, prefix="今天是"),
        get_nowtime(nowtime=today),
        get_weekday_info(nowtime=today, prefix="今天是"),
        get_day_info(nowtime=tomorrow, prefix="明天是"),
        get_weekday_info(nowtime=tomorrow, prefix="明天是"),
        get_day_info(nowtime=yesterday, prefix="昨天是"),
        get_weekday_info(nowtime=yesterday, prefix="昨天是"),
        get_week_range_info(nowtime=today, prefix="本周时间范围是"),
        get_week_range_info(nowtime=today, prefix="当前周时间范围是"),
        get_week_range_info(nowtime=last_week, prefix="上周时间范围是"),
        get_week_range_info(nowtime=next_week, prefix="下周时间范围是"),
        get_year_info(year=today.year, prefix="今年是"),
        get_year_info(year=today.year - 1, prefix="去年是"),
        get_year_info(year=today.year + 1, prefix="明年是"),
        get_lastn_days_info(nowtime=today, n=7, prefix="最近7天的范围是"),
        get_lastn_days_info(nowtime=today, n=14, prefix="最近14天的范围是"),
        get_lastn_days_info(nowtime=today, n=21, prefix="最近21天的范围是"),
        get_lastn_days_info(nowtime=today, n=30, prefix="最近30天的范围是"),
        get_day_time_range(nowtime=today, prefix="今天的时候范围是"),
        get_day_time_range(nowtime=yesterday, prefix="昨天的时候范围是"),
        get_day_time_range(nowtime=tomorrow, prefix="明天的时候范围是"),
        "重要：每天的时间范围总是从这一天的00:00:00到这一天的23:59:59。",
        "重要：在说到最近xx天时，总是要包含今天的。",
        "重要：总是把星期一当成是一周的开始，把星期天当成是一周的结束。",
    ]
