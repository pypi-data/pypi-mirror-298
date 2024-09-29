import argparse
from .monaco_qualifying_report.file_parser import parse_racing_data
from .monaco_qualifying_report.report_builder import calculate_best_lap_times, build_report, sort_racers_by_lap_time

TOP_RACERS_LIMIT = 15


def main():
    parser = argparse.ArgumentParser(description='Generate Formula 1 Qualifying Report')
    parser.add_argument('--files', required=True,
                        help='Path to the folder containing the log files (start.log, end.log, abbreviations.txt)')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--asc', action='store_true', help='Sort in ascending order')
    group.add_argument('--desc', action='store_true', help='Sort in descending order')
    parser.add_argument('--driver', help='Show statistics for a specific driver')

    args = parser.parse_args()
    order = 'desc' if args.desc else 'asc'

    try:
        records = parse_racing_data(args.files)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    lap_times = calculate_best_lap_times(records)
    sorted_lap_times = sort_racers_by_lap_time(lap_times, order=order)

    if args.driver:
        driver = args.driver.lower()
        for racer in sorted_lap_times:
            if racer.name.lower() == driver:
                print(f"Гонщик: {racer.name}")
                print(f"Команда: {racer.team}")
                print(f"Время круга: {racer.lap_time} сек")  # Убрано .3f, так как lap_time теперь строка
                break
        else:
            print(f"Гонщик '{args.driver}' не найден.")
    else:
        report = build_report(sorted_lap_times)
        print(f"Топ-{TOP_RACERS_LIMIT} гонщиков:")
        for i, racer in enumerate(report['top_15'], 1):
            print(f"{i}. {racer.name:20} | {racer.team:30} | {racer.lap_time} сек")  # Убрано .3f
        print("-" * 72)
        print("Выбывшие гонщики:")
        for i, racer in enumerate(report['eliminated'], TOP_RACERS_LIMIT + 1):
            print(f"{i}. {racer.name:20} | {racer.team:30} | {racer.lap_time} сек")  # Убрано .3f


if __name__ == "__main__":
    main()
