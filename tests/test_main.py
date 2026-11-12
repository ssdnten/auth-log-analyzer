import unittest
from main import analyze

def event(second, status='failure', user='alice'):
    return dict(timestamp=f'2026-01-01T00:{second//60:02}:{second%60:02}Z', ip='192.0.2.1', user=user, status=status)

class Tests(unittest.TestCase):
    def test_burst_and_success(self):
        self.assertEqual([a['kind'] for a in analyze([event(0),event(1),event(2),event(3,'success')])], ['failure_burst','success_after_burst'])
    def test_outside_window(self):
        self.assertEqual(analyze([event(0),event(61),event(122)]), [])
    def test_inclusive_boundary(self):
        self.assertEqual(len(analyze([event(0),event(30),event(60)])), 1)
    def test_users_are_separate(self):
        self.assertEqual(analyze([event(0),event(1,user='bob'),event(2)]), [])
    def test_unsorted(self):
        self.assertEqual(analyze([event(2),event(0),event(1)])[0]['count'], 3)
    def test_invalid(self):
        with self.assertRaises(ValueError): analyze([dict(event(0),timestamp='2026-01-01')])
        with self.assertRaises(ValueError): analyze([], threshold=0)
