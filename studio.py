import math
from datetime import datetime

from storage import load_data, save_data, STUDIO_TYPES


def add_studio(studio_id, name, studio_type, hourly_rate):
    if studio_type not in STUDIO_TYPES:
        raise ValueError(f"棚类型必须是以下之一: {', '.join(STUDIO_TYPES)}")

    hourly_rate = int(hourly_rate)
    if hourly_rate <= 0:
        raise ValueError("每小时费用必须是正整数")

    data = load_data()

    if studio_id in data["studios"]:
        raise ValueError(f"棚编号 {studio_id} 已存在")

    data["studios"][studio_id] = {
        "id": studio_id,
        "name": name,
        "type": studio_type,
        "hourly_rate": hourly_rate,
    }

    save_data(data)
    print(f"已添加棚: {studio_id} - {name} ({studio_type})，{hourly_rate}/小时")


def _parse_time(time_str):
    return datetime.strptime(time_str, "%H:%M")


def _time_to_minutes(time_str):
    t = _parse_time(time_str)
    return t.hour * 60 + t.minute


def _check_overlap(start1, end1, start2, end2):
    return start1 < end2 and start2 < end1


def book_studio(studio_id, client, phone, date, start, end):
    data = load_data()

    if studio_id not in data["studios"]:
        raise ValueError(f"棚 {studio_id} 不存在")

    if not client:
        raise ValueError("客户名称不能为空")

    start_min = _time_to_minutes(start)
    end_min = _time_to_minutes(end)

    if end_min <= start_min:
        raise ValueError("结束时间必须晚于开始时间")

    for booking_id, booking in data["bookings"].items():
        if booking["studio_id"] == studio_id and booking["date"] == date and booking["status"] == "active":
            b_start = _time_to_minutes(booking["start"])
            b_end = _time_to_minutes(booking["end"])
            if _check_overlap(start_min, end_min, b_start, b_end):
                raise ValueError(f"该时段与预约 {booking_id} 冲突 ({booking['start']}-{booking['end']})")

    hours = (end_min - start_min) / 60.0
    hourly_rate = data["studios"][studio_id]["hourly_rate"]
    total_fee = math.ceil(hours * hourly_rate)

    data["booking_seq"] += 1
    booking_id = f"B{data['booking_seq']:04d}"

    data["bookings"][booking_id] = {
        "id": booking_id,
        "studio_id": studio_id,
        "client": client,
        "phone": phone,
        "date": date,
        "start": start,
        "end": end,
        "hours": hours,
        "total_fee": total_fee,
        "status": "active",
    }

    save_data(data)
    print(f"预约成功: {booking_id}")
    print(f"  棚: {studio_id} ({data['studios'][studio_id]['name']})")
    print(f"  客户: {client} ({phone})")
    print(f"  日期: {date} {start}-{end}")
    print(f"  时长: {hours} 小时")
    print(f"  费用: {total_fee}")


def cancel_booking(booking_id):
    data = load_data()

    if booking_id not in data["bookings"]:
        raise ValueError(f"预约 {booking_id} 不存在")

    if data["bookings"][booking_id]["status"] != "active":
        raise ValueError(f"预约 {booking_id} 已取消")

    data["bookings"][booking_id]["status"] = "cancelled"
    save_data(data)
    print(f"已取消预约: {booking_id}")
