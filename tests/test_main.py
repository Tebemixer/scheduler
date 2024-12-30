import unittest
class TestMainMethods(unittest.TestCase):
    def test_resource_path(self):
        path = resource_path("test_file.txt")
        self.assertTrue(path.endswith("test_file.txt"))

if __name__ == "__main__":
    unittest.main()
