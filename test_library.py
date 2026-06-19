# Imports
from pathlib import Path
import io
import sys
import tempfile

import acd

# Example data
example_encryption_key = b'192-45-0-55-66-241-55-117'
example_data = {'example-file': 'example file contents'}
example_data_encrypted = b'\x0c\x00\x00\x00example-file\x15\x00\x00\x00\x96\x00\x00\x00\xb1\x00\x00\x00\x93\x00\x00\x00\x9a\x00\x00\x00\xa4\x00\x00\x00\xa1\x00\x00\x00\x92\x00\x00\x00P\x00\x00\x00\x93\x00\x00\x00\x9e\x00\x00\x00\xa1\x00\x00\x00\x92\x00\x00\x00V\x00\x00\x00\x99\x00\x00\x00\x9c\x00\x00\x00\xa0\x00\x00\x00\xa8\x00\x00\x00\x96\x00\x00\x00\x9b\x00\x00\x00\xa9\x00\x00\x00\xa8\x00\x00\x00'

# Tests
def test_get_encryption_key():
  # Testing a string
  encryption_key = acd.get_encryption_key('test')
  assert encryption_key == example_encryption_key
  # Testing a Path
  d = Path().cwd() / 'this' / 'is' / 'a' / 'test'
  encryption_key = acd.get_encryption_key(d / 'data.acd')
  assert encryption_key == example_encryption_key
  encryption_key = acd.get_encryption_key(d / 'data')
  assert encryption_key == example_encryption_key
  encryption_key = acd.get_encryption_key(d / 'dAtA.bip.bop')
  assert encryption_key == example_encryption_key
  encryption_key = acd.get_encryption_key(d / 'duck.pond')
  assert encryption_key == b'134-78-80-97-174-1-25-101'

def test_read():
  fp = io.BytesIO(example_data_encrypted)
  data = acd.read(fp, example_encryption_key)
  assert data == example_data
  assert not fp.closed

def test_write():
  fp = io.BytesIO()
  acd.write(example_data, fp, example_encryption_key)
  data = fp.getvalue()
  assert data == example_data_encrypted
  assert not fp.closed

def test_read_bytes():
  data = acd.read_bytes(example_data_encrypted, example_encryption_key)
  assert data == example_data
  encrypted_bytearray = bytearray(example_data_encrypted)
  data = acd.read_bytes(encrypted_bytearray, example_encryption_key)
  assert data == example_data

def test_write_bytes():
  data = acd.write_bytes(example_data, example_encryption_key)
  assert data == example_data_encrypted

def test_read_file():
  with tempfile.TemporaryDirectory() as tmp:
    file = Path(tmp) / 'test'
    with open(file, 'wb') as fp:
      fp.write(example_data_encrypted)
    data = acd.read_file(file)
  assert data == example_data

def test_write_file():
  with tempfile.TemporaryDirectory() as tmp:
    file = Path(tmp) / 'test'
    acd.write_file(example_data, file)
    data = acd.read_file(file)
  assert data == example_data
