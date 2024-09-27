def calculate_best_lap_times(start_times: dict, end_times: dict, abbreviations: dict):
    """
    Вычисляет лучшее время круга для каждого гонщика.

    Args:
        start_times (dict): Словарь с аббревиатурами гонщиков и их стартовыми временами.
        end_times (dict): Словарь с аббревиатурами гонщиков и их финишными временами.
        abbreviations (dict): Словарь с аббревиатурами гонщиков и их именами и командами.

    Returns:
        list: Список словарей с данными о каждом гонщике, включая его имя, команду и время круга в секундах.
    """
    lap_times = []

    # Проходим по каждому гонщику, у которого есть и стартовое, и финишное время
    for racer in start_times:
        if racer in end_times:
            # Вычисляем время круга как разницу между финишным и стартовым временем
            start_time = start_times[racer]
            end_time = end_times[racer]
            lap_time = end_time - start_time  # Разница во времени
            lap_time_seconds = lap_time.total_seconds ()  # Переводим в секунды

            # Получаем имя и команду гонщика
            name, team = abbreviations.get (racer, ("Unknown", "Unknown"))

            # Добавляем результат в список
            lap_times.append ({
                'abbreviation': racer,
                'name': name,
                'team': team,
                'lap_time': lap_time_seconds
            })

    return lap_times


def sort_racers_by_lap_time(lap_times: list, order: str = 'asc'):
    """
    Сортирует гонщиков по времени круга.

    Args:
        lap_times (list): Список словарей с информацией о гонщиках и их времени круга.
        order (str): Порядок сортировки ('asc' для возрастания, 'desc' для убывания).

    Returns:
        list: Отсортированный список гонщиков по времени круга.
    """
    return sorted (lap_times, key=lambda x: x['lap_time'], reverse=(order == 'desc'))


def build_report(lap_times: list):
    """
    Строит отчет на основе времени круга каждого гонщика.

    Args:
        lap_times (list): Список словарей с информацией о времени круга каждого гонщика.

    Returns:
        dict: Словарь с отсортированными результатами: топ-15 гонщиков и остальные.
    """
    # Сортируем гонщиков по времени круга (от наименьшего к наибольшему)
    sorted_lap_times = sorted (lap_times, key=lambda x: x['lap_time'])

    # Разделяем гонщиков на топ-15 и остальных
    top_15 = sorted_lap_times[:15]
    eliminated = sorted_lap_times[15:]

    return {
        'top_15': top_15,
        'eliminated': eliminated
    }
