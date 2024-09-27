import Common as utils
import os
import unittest
import numpy as np
import torch
import os
import tempfile

# Assuming the functions are in a file named utils.py

class TestUtilFunctions(unittest.TestCase):

    def test_open_yaml(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp:
            temp.write("key1: value1\nkey2: value2")
            temp_name = temp.name
        
        result = utils.open_yaml(temp_name)
        self.assertEqual(result, {"key1": "value1", "key2": "value2"})
        
        result_with_key = utils.open_yaml(temp_name, "key1")
        self.assertEqual(result_with_key, "value1")
        
        os.unlink(temp_name)

    def test_open_json(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp:
            temp.write('{"key1": "value1", "key2": "value2"}')
            temp_name = temp.name
        
        result = utils.open_json(temp_name)
        self.assertEqual(result, {"key1": "value1", "key2": "value2"})
        
        os.unlink(temp_name)

    def test_dump_to_json(self):
        data = {"key1": "value1", "key2": "value2"}
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as temp:
            temp_name = temp.name
        
        utils.dump_to_json(temp_name, data)
        
        with open(temp_name, 'r') as f:
            result = f.read()
        
        self.assertIn('"key1": "value1"', result)
        self.assertIn('"key2": "value2"', result)
        
        os.unlink(temp_name)

    def test_dump_to_text(self):
        text = "Hello, world!"
        with tempfile.TemporaryDirectory() as tempdir:
            path = os.path.join(tempdir, "subdir", "test.txt")
            utils.dump_to_text(text, path)
            
            with open(path, 'r') as f:
                result = f.read()
            
            self.assertEqual(result, text)

    def test_tokenize(self):
        text = "Hello, world!"
        tokens = utils.tokenize(text)
        self.assertIsInstance(tokens, list)
        self.assertTrue(all(isinstance(token, int) for token in tokens))

    def test_ends_with(self):
        self.assertTrue(utils.ends_with("test.txt", [".txt", ".pdf"]))
        self.assertFalse(utils.ends_with("test.doc", [".txt", ".pdf"]))

    def test_normalize_text(self):
        text = "  Hello,   World!  "
        normalized = utils.normalize_text(text)
        self.assertEqual(normalized, "hello, world!")

    def test_remove_stopwords(self):
        text = "The quick brown fox jumps over the lazy dog"
        stopwords = ["the", "over"]
        result = utils.remove_stopwords(text, stopwords)
        self.assertEqual(result, "quick brown fox jumps lazy dog")

    def test_get_device(self):
        device = utils.get_device()
        self.assertIsInstance(device, torch.device)

    def test_compute_similarity(self):
        v1 = np.array([1, 2, 3])
        v2 = np.array([2, 4, 6])
        similarity = utils.compute_similarity(v1, v2)
        self.assertAlmostEqual(similarity, 1.0)

    def test_safe_divide(self):
        self.assertEqual(utils.safe_divide(10, 2), 5)
        self.assertEqual(utils.safe_divide(10, 0), 0)

    def test_moving_average(self):
        data = [1, 2, 3, 4, 5]
        result = utils.moving_average(data, 3)
        self.assertEqual(result, [2, 3, 4])

    def test_flatten_dict(self):
        nested_dict = {"a": 1, "b": {"c": 2, "d": {"e": 3}}}
        flattened = utils.flatten_dict(nested_dict)
        self.assertEqual(flattened, {"a": 1, "b_c": 2, "b_d_e": 3})

    def test_chunk_list(self):
        lst = [1, 2, 3, 4, 5, 6, 7]
        chunks = utils.chunk_list(lst, 3)
        self.assertEqual(chunks, [[1, 2, 3], [4, 5, 6], [7]])

if __name__ == '__main__':
    unittest.main()
