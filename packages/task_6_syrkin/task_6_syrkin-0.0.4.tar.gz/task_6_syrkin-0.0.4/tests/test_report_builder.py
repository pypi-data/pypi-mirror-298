# tests/test_report_builder.py

import unittest
from task_6_syrkin.monaco_qualifying_report.report_builder import calculate_best_lap_times, build_report, sort_racers_by_lap_time
from task_6_syrkin.monaco_qualifying_report.record import Record
from datetime import datetime

class TestReportBuilder(unittest.TestCase):
    def setUp(self):
        self.records = [
            Record(
                abbreviation='DRR',
                name='Daniel Ricciardo',
                team='RED BULL RACING TAG HEUER',
                start_time=datetime.strptime('2018-05-24_12:14:12.054', '%Y-%m-%d_%H:%M:%S.%f'),
                end_time=datetime.strptime('2018-05-24_12:15:24.067', '%Y-%m-%d_%H:%M:%S.%f')
            ),
            Record(
                abbreviation='SVF',
                name='Sebastian Vettel',
                team='FERRARI',
                start_time=datetime.strptime('2018-05-24_12:02:58.917', '%Y-%m-%d_%H:%M:%S.%f'),
                end_time=datetime.strptime('2018-05-24_12:04:03.332', '%Y-%m-%d_%H:%M:%S.%f')
            ),
            Record(
                abbreviation='LHM',
                name='Lewis Hamilton',
                team='MERCEDES',
                start_time=datetime.strptime('2018-05-24_12:18:20.125', '%Y-%m-%d_%H:%M:%S.%f'),
                end_time=datetime.strptime('2018-05-24_12:19:32.585', '%Y-%m-%d_%H:%M:%S.%f')
            ),
        ]

    def test_calculate_best_lap_times(self):
        lap_times = calculate_best_lap_times(self.records)
        self.assertEqual(len(lap_times), 3)

        lap_time_dict = {record.abbreviation: record.lap_time for record in lap_times}

        self.assertEqual(lap_time_dict['DRR'], '01:12.013')
        self.assertEqual(lap_time_dict['SVF'], '01:04.415')
        self.assertEqual(lap_time_dict['LHM'], '01:12.460')

    def test_sort_racers_by_lap_time_asc(self):
        lap_times = calculate_best_lap_times(self.records)
        sorted_records = sort_racers_by_lap_time(lap_times, order='asc')

        self.assertEqual(sorted_records[0].abbreviation, 'SVF')  # Самое быстрое время
        self.assertEqual(sorted_records[1].abbreviation, 'DRR')
        self.assertEqual(sorted_records[2].abbreviation, 'LHM')

    def test_sort_racers_by_lap_time_desc(self):
        lap_times = calculate_best_lap_times(self.records)
        sorted_records = sort_racers_by_lap_time(lap_times, order='desc')

        self.assertEqual(sorted_records[0].abbreviation, 'LHM')  # Самое медленное время
        self.assertEqual(sorted_records[1].abbreviation, 'DRR')
        self.assertEqual(sorted_records[2].abbreviation, 'SVF')

    def test_build_report(self):
        lap_times = calculate_best_lap_times(self.records)
        sorted_records = sort_racers_by_lap_time(lap_times, order='asc')
        report = build_report(sorted_records, top_n=2)

        self.assertEqual(len(report['top_15']), 2)
        self.assertEqual(len(report['eliminated']), 1)

        self.assertEqual(report['top_15'][0].abbreviation, 'SVF')
        self.assertEqual(report['top_15'][1].abbreviation, 'DRR')
        self.assertEqual(report['eliminated'][0].abbreviation, 'LHM')

if __name__ == '__main__':
    unittest.main()
