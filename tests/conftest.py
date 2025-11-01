"""
Общие настройки для всех тестов
"""
import sys
from unittest.mock import MagicMock

# Мокаем common.config для ВСЕХ тестов
sys.modules['common'] = MagicMock()
sys.modules['common.config'] = MagicMock()