# tests/test_file_parser.py

import unittest
import tempfile
import os
from datetime import datetime
from task_6_syrkin.monaco_qualifying_report.file_parser import parse_racing_data
from task_6_syrkin.monaco_qualifying_report.record import Record

class TestFileParser(unittest.TestCase):
    def setUp(self):
        # Создаем временную директорию и файлы для тестов
        self.temp_dir = tempfile.TemporaryDirectory()
        self.start_log_path = os.path.join(self.temp_dir.name, 'start.log')
        self.end_log_path = os.path.join(self.temp_dir.name, 'end.log')
        self.abbreviations_path = os.path.join(self.temp_dir.name, 'abbreviations.txt')

    def tearDown(self):
        # Удаляем временную директорию после тестов
        self.temp_dir.cleanup()

    def test_parse_racing_data(self):
        with open(self.start_log_path, 'w') as f:
            f.write('DRR2018-05-24_12:14:12.054\n')
            f.write('SVF2018-05-24_12:02:58.917\n')

        with open(self.end_log_path, 'w') as f:
            f.write('DRR2018-05-24_12:15:24.067\n')
            f.write('SVF2018-05-24_12:04:03.332\n')

        with open(self.abbreviations_path, 'w') as f:
            f.write('DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER\n')
            f.write('SVF_Sebastian Vettel_FERRARI\n')

        records = parse_racing_data(self.temp_dir.name)

        self.assertEqual(len(records), 2)

        record_dict = {record.abbreviation: record for record in records}

        drr_record = record_dict.get('DRR')
        svf_record = record_dict.get('SVF')

        self.assertIsNotNone(drr_record)
        self.assertIsNotNone(svf_record)

        # Проверяем данные DRR
        self.assertEqual(drr_record.name, 'Daniel Ricciardo')
        self.assertEqual(drr_record.team, 'RED BULL RACING TAG HEUER')
        self.assertEqual(drr_record.start_time, datetime.strptime('2018-05-24_12:14:12.054', '%Y-%m-%d_%H:%M:%S.%f'))
        self.assertEqual(drr_record.end_time, datetime.strptime('2018-05-24_12:15:24.067', '%Y-%m-%d_%H:%M:%S.%f'))
        self.assertEqual(drr_record.lap_time, '01:12.013')

        # Проверяем данные SVF
        self.assertEqual(svf_record.name, 'Sebastian Vettel')
        self.assertEqual(svf_record.team, 'FERRARI')
        self.assertEqual(svf_record.start_time, datetime.strptime('2018-05-24_12:02:58.917', '%Y-%m-%d_%H:%M:%S.%f'))
        self.assertEqual(svf_record.end_time, datetime.strptime('2018-05-24_12:04:03.332', '%Y-%m-%d_%H:%M:%S.%f'))
        self.assertEqual(svf_record.lap_time, '01:04.415')

    def test_parse_racing_data_missing_files(self):
        # Удаляем файлы, чтобы проверить обработку ошибок
        os.remove(self.start_log_path)

        with self.assertRaises(FileNotFoundError):
            parse_racing_data(self.temp_dir.name)

if __name__ == '__main__':
    unittest.main()
