import unittest
from datetime import datetime
from app.last_update import last_update


class LastUpdateTestCase(unittest.TestCase):
    def test_last_update(self):
        with open('.lastUpdate', encoding='utf-8') as f:
            test_update_date = datetime.strptime(f.read(), '%Y-%m-%d').date()
        self.assertEqual(last_update(), test_update_date)
