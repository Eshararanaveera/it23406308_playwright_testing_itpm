"""Quick test - runs first 3 test cases only to verify everything works"""
import sys
import os

# Temporarily modify max_row to test only first few rows
original_file = 'test_automation.py'
with open(original_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Run with limited rows
import subprocess
result = subprocess.run([
    sys.executable, 'test_automation.py',
    '--excel', 'Assignment 1 - Test cases_IT23406308.xlsx',
    '--save-every', '1',
    '--wait-ms', '8000',
    '--retries', '15'
], capture_output=False, text=True)

print(f"\nTest completed with exit code: {result.returncode}")
