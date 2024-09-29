import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
import logging

# Configure logging
logging.basicConfig (level=logging.INFO)
logger = logging.getLogger (__name__)


@dataclass
class Record:
    abbreviation: str
    name: str
    team: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    errors: List[str] = field (default_factory=list, init=False)

    @property
    def lap_time(self) -> Optional[str]:
        """
        Возвращает время круга в формате 'MM:SS'. Если время не указано, возвращает None.
        """
        if self.start_time is None or self.end_time is None:
            if self.start_time is None:
                self.errors.append (f"Стартовое время не указано для {self.abbreviation}")
            if self.end_time is None:
                self.errors.append (f"Финишное время не указано для {self.abbreviation}")
            return None

        # Вычисляем время круга в секундах
        lap_time_seconds = (self.end_time - self.start_time).total_seconds ()

        # Преобразуем в минуты, секунды и миллисекунды
        minutes, seconds = divmod (lap_time_seconds, 60)
        seconds, milliseconds = divmod (seconds, 1)  # Отделяем миллисекунды
        milliseconds = int (milliseconds * 1000)  # Преобразуем долю секунды в миллисекунды

        # Возвращаем строку формата 'MM:SS.mmm'
        return f'{int (minutes):02}:{int (seconds):02}.{milliseconds:03}'

    @classmethod
    def from_data(cls, abbreviation: str, name: str, team: str, start_time: Optional[datetime],
                  end_time: Optional[datetime]) -> 'Record':
        """
        Альтернативный конструктор для создания объекта Record из отдельных данных.
        """
        return cls (abbreviation, name, team, start_time, end_time)

    def has_errors(self) -> bool:
        return len (self.errors) > 0

    def print_errors(self):
        if self.has_errors ():
            for error in self.errors:
                logger.info (f"Ошибка: {error}")
        else:
            logger.info ("Ошибок не обнаружено.")