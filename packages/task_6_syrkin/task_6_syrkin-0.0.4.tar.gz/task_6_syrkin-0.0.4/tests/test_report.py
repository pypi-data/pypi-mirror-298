# tests/test_report.py

import unittest
import tempfile
import os
from unittest.mock import patch
from io import StringIO
from task_6_syrkin import report

class TestReportScript(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('sys.argv', ['report.py'])
        self.mock_sys_argv = self.patcher.start()

        # Создаем временную директорию и файлы для тестов
        self.temp_dir = tempfile.TemporaryDirectory()
        self.start_log_path = os.path.join(self.temp_dir.name, 'start.log')
        self.end_log_path = os.path.join(self.temp_dir.name, 'end.log')
        self.abbreviations_path = os.path.join(self.temp_dir.name, 'abbreviations.txt')

        with open(self.start_log_path, 'w') as f:
            f.write('DRR2018-05-24_12:14:12.054\n')
            f.write('SVF2018-05-24_12:02:58.917\n')

        with open(self.end_log_path, 'w') as f:
            f.write('DRR2018-05-24_12:15:24.067\n')
            f.write('SVF2018-05-24_12:04:03.332\n')

        with open(self.abbreviations_path, 'w') as f:
            f.write('DRR_Daniel Ricciardo_RED BULL RACING TAG HEUER\n')
            f.write('SVF_Sebastian Vettel_FERRARI\n')

    def tearDown(self):
        self.temp_dir.cleanup()
        self.patcher.stop()

    @patch('sys.stdout', new_callable=StringIO)
    def test_report_default_order(self, mock_stdout):
        test_args = ['report.py', '--files', self.temp_dir.name]
        with patch('sys.argv', test_args):
            report.main()
            output = mock_stdout.getvalue()
            self.assertIn('Топ-15 гонщиков:', output)
            self.assertIn('1. Sebastian Vettel', output)
            self.assertIn('2. Daniel Ricciardo', output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_report_desc_order(self, mock_stdout):
        test_args = ['report.py', '--files', self.temp_dir.name, '--desc']
        with patch('sys.argv', test_args):
            report.main()
            output = mock_stdout.getvalue()
            self.assertIn('Топ-15 гонщиков:', output)
            self.assertIn('1. Daniel Ricciardo', output)
            self.assertIn('2. Sebastian Vettel', output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_report_driver(self, mock_stdout):
        test_args = ['report.py', '--files', self.temp_dir.name, '--driver', 'Sebastian Vettel']
        with patch('sys.argv', test_args):
            report.main()
            output = mock_stdout.getvalue()
            self.assertIn('Гонщик: Sebastian Vettel', output)
            self.assertIn('Команда: FERRARI', output)
            self.assertIn('Время круга: 01:04.415 сек', output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_report_driver_not_found(self, mock_stdout):
        test_args = ['report.py', '--files', self.temp_dir.name, '--driver', 'Unknown Driver']
        with patch('sys.argv', test_args):
            report.main()
            output = mock_stdout.getvalue()
            self.assertIn("Гонщик 'Unknown Driver' не найден.", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_report_files_not_found(self, mock_stdout):
        test_args = ['report.py', '--files', 'non_existent_directory']
        with patch('sys.argv', test_args):
            report.main()
            output = mock_stdout.getvalue()
            self.assertIn('Error:', output)

if __name__ == '__main__':
    unittest.main()
