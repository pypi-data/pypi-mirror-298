from typing import List, Dict
from .record import Record


def calculate_best_lap_times(records: List[Record]) -> List[Record]:
    """
    Вычисляет лучшее время круга для каждого гонщика.
    Args:
        records (List[Record]): Список объектов Record для всех гонщиков.
    Returns:
        List[Record]: Список объектов Record с вычисленными временами круга.
    """
    return [record for record in records if record.lap_time is not None]


def sort_racers_by_lap_time(records: List[Record], order: str = 'asc') -> List[Record]:
    """
    Сортирует гонщиков по времени круга.
    Args:
        records (List[Record]): Список объектов Record.
        order (str): Порядок сортировки ('asc' для возрастания, 'desc' для убывания).
    Returns:
        List[Record]: Отсортированный список объектов Record.
    Raises:
        ValueError: Если указанный порядок сортировки недопустим.
    """
    if order not in {'asc', 'desc'}:
        raise ValueError ("order must be 'asc' or 'desc'")
    return sorted (records, key=lambda record: record.lap_time if record.lap_time is not None else float ('inf'),
                   reverse=(order == 'desc'))


def build_report(records: List[Record]) -> Dict[str, List[Record]]:
    """
    Строит отчет на основе времени круга каждого гонщика.
    Args:
        records (List[Record]): Список объектов Record.
    Returns:
        dict: Словарь с отсортированными результатами: топ-15 гонщиков и остальные.
    """
    # Сортируем гонщиков по времени круга (от наименьшего к наибольшему)
    sorted_records = sorted (records,
                             key=lambda record: record.lap_time if record.lap_time is not None else float ('inf'))
    return {
        'top_15': sorted_records[:15],
        'eliminated': sorted_records[15:]
    }