import argparse

from task_6_syrkin.monaco_qualifying_report.file_parser import parse_racing_data
from task_6_syrkin.monaco_qualifying_report.report_builder import calculate_best_lap_times, build_report, sort_racers_by_lap_time  # Импортируем из модуля report_builder


def main():
    # Настраиваем парсер аргументов командной строки
    parser = argparse.ArgumentParser (description='Generate Formula 1 Qualifying Report')

    # Аргумент для указания папки с лог-файлами
    parser.add_argument ('--files', required=True,
                         help='Path to the folder containing the log files (start.log, end.log, abbreviations.txt)')

    # Опции сортировки
    parser.add_argument ('--asc', action='store_true', help='Sort in ascending order (default)')
    parser.add_argument ('--desc', action='store_true', help='Sort in descending order')

    # Опция для фильтрации по имени гонщика
    parser.add_argument ('--driver', help='Show statistics for a specific driver')

    # Парсим аргументы
    args = parser.parse_args ()

    # Определяем порядок сортировки
    order = 'desc' if args.desc else 'asc'

    # Шаг 1: Парсим данные из файлов
    racing_data = parse_racing_data (args.files)

    # Шаг 2: Вычисляем лучшее время круга для каждого гонщика
    lap_times = calculate_best_lap_times (racing_data['start_times'], racing_data['end_times'],
                                          racing_data['abbreviations'])

    # Шаг 3: Сортируем гонщиков по времени круга
    sorted_lap_times = sort_racers_by_lap_time (lap_times, order=order)

    # Если пользователь указал конкретного гонщика, выводим информацию только о нем
    if args.driver:
        driver = args.driver.lower ()
        for racer in sorted_lap_times:
            if racer['name'].lower () == driver:
                print (f"Гонщик: {racer['name']}")
                print (f"Команда: {racer['team']}")
                print (f"Время круга: {racer['lap_time']:.3f} сек")
                break
        else:
            print (f"Гонщик '{args.driver}' не найден.")
    else:
        # Шаг 4: Строим и выводим полный отчет
        report = build_report (sorted_lap_times)

        # Выводим топ-15 гонщиков
        print ("Топ-15 гонщиков:")
        for i, racer in enumerate (report['top_15'], 1):
            print (f"{i}. {racer['name']:20} | {racer['team']:30} | {racer['lap_time']:.3f} сек")

        # Разделитель
        print ("-" * 72)

        # Выводим выбывших гонщиков
        print ("Выбывшие гонщики:")
        for i, racer in enumerate (report['eliminated'], 16):
            print (f"{i}. {racer['name']:20} | {racer['team']:30} | {racer['lap_time']:.3f} сек")


# Точка входа в программу
if __name__ == "__main__":
    main ()
