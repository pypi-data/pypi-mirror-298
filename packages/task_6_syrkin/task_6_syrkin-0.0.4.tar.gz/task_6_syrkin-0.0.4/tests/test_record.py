# tests/test_record.py

import unittest
from datetime import datetime
from task_6_syrkin.monaco_qualifying_report.record import Record

class TestRecord(unittest.TestCase):
    def test_lap_time_calculation(self):
        start_time = datetime.strptime('2018-05-24_12:00:00.000', '%Y-%m-%d_%H:%M:%S.%f')
        end_time = datetime.strptime('2018-05-24_12:01:30.500', '%Y-%m-%d_%H:%M:%S.%f')
        record = Record(
            abbreviation='ABC',
            name='Test Driver',
            team='Test Team',
            start_time=start_time,
            end_time=end_time
        )
        expected_lap_time = '01:30.500'
        self.assertEqual(record.lap_time, expected_lap_time)

    def test_lap_time_missing_start_time(self):
        end_time = datetime.strptime('2018-05-24_12:01:30.500', '%Y-%m-%d_%H:%M:%S.%f')
        record = Record(
            abbreviation='ABC',
            name='Test Driver',
            team='Test Team',
            start_time=None,
            end_time=end_time
        )
        self.assertIsNone(record.lap_time)
        self.assertTrue(record.has_errors())
        self.assertIn("Стартовое время не указано для ABC", record.errors)

    def test_lap_time_missing_end_time(self):
        start_time = datetime.strptime('2018-05-24_12:00:00.000', '%Y-%m-%d_%H:%M:%S.%f')
        record = Record(
            abbreviation='ABC',
            name='Test Driver',
            team='Test Team',
            start_time=start_time,
            end_time=None
        )
        self.assertIsNone(record.lap_time)
        self.assertTrue(record.has_errors())
        self.assertIn("Финишное время не указано для ABC", record.errors)

    def test_has_errors(self):
        record = Record(
            abbreviation='ABC',
            name='Test Driver',
            team='Test Team'
        )
        self.assertFalse(record.has_errors())
        record.errors.append("Test error")
        self.assertTrue(record.has_errors())

if __name__ == '__main__':
    unittest.main()
