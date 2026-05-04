# Imports
from pathlib import Path
import io
import sys
import tempfile
import unittest

sys.path.append('../')
import acd

# Example variables
example_file_name = 'example.acd'
example_file = Path.cwd() / example_file_name
example_encryption_key = '66-35-39-166-60-105-70-101'
example_encrypted_data = b'\x0c\x00\x00\x00example-file\x15\x00\x00\x00\x9b\x00\x00\x00\xae\x00\x00\x00\x8e\x00\x00\x00\xa0\x00\x00\x00\xa5\x00\x00\x00\x99\x00\x00\x00\x98\x00\x00\x00Y\x00\x00\x00\x93\x00\x00\x00\x9a\x00\x00\x00\xa2\x00\x00\x00\x9b\x00\x00\x00M\x00\x00\x00\x99\x00\x00\x00\x9f\x00\x00\x00\x9b\x00\x00\x00\xa5\x00\x00\x00\x95\x00\x00\x00\xa3\x00\x00\x00\xa1\x00\x00\x00\xaa\x00\x00\x00'
example_dict = {'example-file': 'example file contents'}

# Testing if the example file exists.
class TestFile(unittest.TestCase):
  def test_example_file_exists(self):
    self.assertTrue(example_file.is_file())

  def test_example_file_data(self):
    with open(example_file, 'rb') as file:
      data = file.read()
    self.assertEqual(data, example_encrypted_data)

# Testing reading and writing acd file objects/bytes/files.
class TestLibrary(unittest.TestCase):
  def test_encyrption_key_generation(self):
    encryption_key = acd.get_encryption_key_for_file(example_file)
    self.assertEqual(encryption_key, example_encryption_key)
    another_encryption_key = acd.get_encryption_key_for_string(example_file_name)
    self.assertEqual(another_encryption_key, encryption_key)

  def test_read(self):
    with open(example_file, 'rb') as file:
      data = acd.read(file, example_encryption_key)
    self.assertEqual(data, example_dict)

  def test_read_bytes(self):
    data = acd.read_bytes(example_encrypted_data, example_encryption_key)
    self.assertEqual(data, example_dict)
    data = acd.read_bytes(bytearray(example_encrypted_data), example_encryption_key)
    self.assertEqual(data, example_dict)

  def test_read_file(self):
    data = acd.read_file(example_file)
    self.assertEqual(data, example_dict)
    data = acd.read_file(str(example_file))
    self.assertEqual(data, example_dict)

  def test_write(self):
    fp = io.BytesIO()
    acd.write(example_dict, fp, example_encryption_key)
    b = fp.getvalue()
    self.assertEqual(b, example_encrypted_data)

  def test_write_bytes(self):
    b = acd.write_bytes(example_dict, example_encryption_key)
    self.assertEqual(b, example_encrypted_data)

  def test_write_file(self):
    with tempfile.TemporaryDirectory() as tmp:
      out_file = Path(tmp) / 'data.acd'
      acd.write_file(example_dict, out_file)
      data1 = acd.read_file(out_file)
      data2 = acd.read_file(str(out_file))
    self.assertEqual(data1, data2)
    self.assertEqual(data1, example_dict)
