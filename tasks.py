import math
import calendar
from datetime import datetime

from storage import load_data, save_data


def add_edit_task(client, desc, hours, rate):
    if hours <= 0:
        raise ValueError("工时必须为正数")
    if rate <= 0:
        raise ValueError("时费必须为正数")
    if not client:
        raise ValueError("客户名称不能为空")
    if not desc:
        raise ValueError("任务描述不能为空")

    total_fee = math.ceil(hours * rate)

    data = load_data()
    data["edit_task_seq"] += 1
    task_id = f"E{data['edit_task_seq']:04d}"

    today = datetime.now().strftime("%Y-%m-%d")

    data["edit_tasks"][task_id] = {
        "id": task_id,
        "client": client,
        "desc": desc,
        "hours": hours,
        "rate": rate,
        "total_fee": total_fee,
        "date": today,
    }

    save_data(data)
    print(f"剪辑任务已添加: {task_id}")
    print(f"  客户: {client}")
    print(f"  描述: {desc}")
    print(f"  工时: {hours} 小时")
    print(f"  时费: {rate}")
    print(f"  总费用: {total_fee}")


def monthly_income(month):
    try:
        year, month_num = month.split("-")
        year = int(year)
        month_num = int(month_num)
        if month_num < 1 or month_num > 12:
            raise ValueError
    except (ValueError, IndexError):
        raise ValueError("月份格式不正确，请使用 YYYY-MM 格式")

    data = load_data()

    studio_income = 0
    booking_count = 0
    for booking_id, booking in data["bookings"].items():
        if booking["status"] != "active":
            continue
        if booking["date"].startswith(month):
            studio_income += booking["total_fee"]
            booking_count += 1

    edit_income = 0
    edit_count = 0
    for task_id, task in data["edit_tasks"].items():
        if task["date"].startswith(month):
            edit_income += task["total_fee"]
            edit_count += 1

    total_income = studio_income + edit_income

    print(f"=== {year}年{month_num}月 收入统计 ===")
    print(f"录音预约收入: {studio_income} ({booking_count} 笔)")
    print(f"剪辑任务收入: {edit_income} ({edit_count} 笔)")
    print(f"-------------------------")
    print(f"总收入: {total_income}")
