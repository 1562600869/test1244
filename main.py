import argparse
import sys

from studio import add_studio, book_studio, cancel_booking
from tasks import add_edit_task, monthly_income
from storage import STUDIO_TYPES


def main():
    parser = argparse.ArgumentParser(description="播客工作室管理工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    add_studio_parser = subparsers.add_parser("add-studio", help="添加录音棚")
    add_studio_parser.add_argument("studio_id", help="棚编号，如 S01")
    add_studio_parser.add_argument("name", help="棚名称，如 A棚")
    add_studio_parser.add_argument("--type", required=True, dest="studio_type",
                                   help=f"棚类型: {', '.join(STUDIO_TYPES)}")
    add_studio_parser.add_argument("--hourly-rate", required=True, type=int,
                                   help="每小时费用（整数）")

    book_parser = subparsers.add_parser("book", help="预约录音棚")
    book_parser.add_argument("studio_id", help="棚编号")
    book_parser.add_argument("--client", required=True, help="客户名称")
    book_parser.add_argument("--phone", default="", help="联系电话")
    book_parser.add_argument("--date", required=True, help="预约日期 (YYYY-MM-DD)")
    book_parser.add_argument("--start", required=True, help="开始时间 (HH:MM)")
    book_parser.add_argument("--end", required=True, help="结束时间 (HH:MM)")

    cancel_parser = subparsers.add_parser("cancel", help="取消预约")
    cancel_parser.add_argument("booking_id", help="预约编号")

    add_edit_parser = subparsers.add_parser("add-edit-task", help="添加剪辑任务")
    add_edit_parser.add_argument("--client", required=True, help="客户名称")
    add_edit_parser.add_argument("--desc", required=True, help="任务描述")
    add_edit_parser.add_argument("--hours", required=True, type=float, help="工时（小时）")
    add_edit_parser.add_argument("--rate", required=True, type=float, help="时费")

    income_parser = subparsers.add_parser("monthly-income", help="月度收入统计")
    income_parser.add_argument("--month", required=True, help="月份 (YYYY-MM)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "add-studio":
            add_studio(args.studio_id, args.name, args.studio_type, args.hourly_rate)
        elif args.command == "book":
            book_studio(args.studio_id, args.client, args.phone, args.date, args.start, args.end)
        elif args.command == "cancel":
            cancel_booking(args.booking_id)
        elif args.command == "add-edit-task":
            add_edit_task(args.client, args.desc, args.hours, args.rate)
        elif args.command == "monthly-income":
            monthly_income(args.month)
    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"发生错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
