import sys
from unittest.mock import patch
import pytest
from src.generate_summary_of_injuries import main

def test_main_function():
    with patch('src.generate_summary_of_injuries.process_pdf_files') as mock_process:
        with patch('src.generate_summary_of_injuries.sort_records') as mock_sort:
            with patch('src.generate_summary_of_injuries.create_summary_pdf') as mock_create_pdf:
                mock_process.return_value = [{'date': '2023-01-01', 'diagnosis': 'Test'}]
                mock_sort.return_value = [{'date': '2023-01-01', 'diagnosis': 'Test'}]
                
                main('input_folder', 'output_folder')
                
                mock_process.assert_called_once_with('input_folder')
                mock_sort.assert_called_once()
                mock_create_pdf.assert_called_once()

def test_command_line_interface():
    with patch('src.generate_summary_of_injuries.create_summary_pdf') as mock_create_pdf:
        test_args = ['main.py', 'input_folder', 'output_folder']
        with patch.object(sys, 'argv', test_args):
            import src.main as main
            main.main()
        mock_create_pdf.assert_called_once_with('input_folder', 'output_folder')

def test_version_command():
    with patch('builtins.print') as mock_print:
        test_args = ['main.py', '--version']
        with patch.object(sys, 'argv', test_args):
            import src.main as main
            main.main()
        mock_print.assert_called_once_with("generate-summary-of-injuries version 1.0.1")

def test_invalid_arguments():
    with patch('builtins.print') as mock_print:
        test_args = ['main.py']
        with patch.object(sys, 'argv', test_args):
            import src.main as main
            main.main()
        mock_print.assert_called_once_with("Usage: generate-summary-of-injuries [--version] <input_folder> <output_folder>")
