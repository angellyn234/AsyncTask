# test_asynctask.py
"""
Tests for AsyncTask module.
"""

import unittest
from asynctask import AsyncTask

class TestAsyncTask(unittest.TestCase):
    """Test cases for AsyncTask class."""
    
    def test_initialization(self):
        """Test class initialization."""
        instance = AsyncTask()
        self.assertIsInstance(instance, AsyncTask)
        
    def test_run_method(self):
        """Test the run method."""
        instance = AsyncTask()
        self.assertTrue(instance.run())

if __name__ == "__main__":
    unittest.main()
