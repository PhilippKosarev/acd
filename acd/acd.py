# Imports
import os
import io


def get_encryption_key_for_string(string: str) -> str:
  """Generates the encryption key using the given string.

  To get the right encryption key for a given file, use its basename as
  as the string, unless it starts with 'data' (case-insensitive).

  If the file's basename does start with 'data', then the basename of
  the directory that the file is in should be used.
  """
  # Prerequisites
  string = string.lower()
  n_chars = len(string)
  string_ord = [ord(char) for char in string]
  # 1
  items = [sum(string_ord)]
  # 2
  num = 0
  for i in range(0, n_chars - 1, 2):
    num = num * string_ord[i] - string_ord[i+1]
  items.append(num)
  # 3
  num = 0
  for i in range(1, n_chars - 3, 3):
    num *= string_ord[i]
    divisor = string_ord[i+1] + 27
    num = int(num / divisor)
    num += -27 - string_ord[i-1]
  items.append(num)
  # 4
  num = 5763
  for i in range(1, n_chars):
    num -= string_ord[i]
  items.append(num)
  # 5
  num = 66
  for i in range(1, n_chars - 4, 4):
    num = num * (string_ord[i] + 15) * (string_ord[i-1] + 15) + 22
  items.append(num)
  # 6
  num = 101
  for i in range(0, n_chars - 2, 2):
    num -= ord(string[i])
  items.append(num)
  # 7
  num = 171
  for i in range(0, n_chars - 2, 2):
    num = num % string_ord[i]
  items.append(num)
  # 8
  num = 171
  for i in range(n_chars - 1):
    num = int(num / string_ord[i]) + string_ord[i + 1]
  items.append(num)
  # Returning
  return '-'.join([str(item % 256) for item in items])


def get_encryption_key_for_file(file) -> str:
  """Generates the encryption key for the given `file` (a `str` or
  path-like object).
  """
  file = os.path.abspath(file)
  basename = os.path.basename(file)
  if basename.lower().startswith('data'):
    parent = os.path.dirname(file)
    basename = os.path.basename(parent)
  return get_encryption_key_for_string(basename)


def _decrypt_bytes(data: bytes, encryption_key: str) -> str:
  # Getting every 4th byte
  full = data[::4]
  data = bytearray(len(full))
  i = 0
  while i < len(full):
    data[i] = full[i]
    i += 1
  # Decrypting
  i = 0
  n_bytes = len(data)
  n_chars = len(encryption_key)
  num = 0
  while i < n_bytes:
    temp = data[i] - ord(encryption_key[num])
    temp = temp % 256
    data[i] = temp
    if num == n_chars - 1:
      num = 0
    else:
      num += 1
    i += 1
  # Returning
  return data.decode()


def _encrypt_bytes(data: bytes, encryption_key: str) -> bytes:
  data = bytearray(data)
  # Encrypting
  i = 0
  n_bytes = len(data)
  n_chars = len(encryption_key)
  num = 0
  while i < n_bytes:
    temp = data[i] + ord(encryption_key[num])
    temp = temp % 256
    data[i] = temp
    if num == n_chars - 1:
      num = 0
    else:
      num += 1
    i += 1
  # Adding padding
  padded_data = bytearray(len(data) * 4)
  for i in range(len(data)):
    padded_data[i * 4] = data[i]
    for n in range(1, 4):
      padded_data[i * 4 + n] = 0
  # Returning
  return bytes(padded_data)


def read(fp, encryption_key: str) -> dict:
  """Deserialises `fp` (a `.read()`-supporting file-like object) to a
  dictionary where all the keys and values are strings.

  The `encryption_key` can be obtained using either
  `get_encryption_key_for_string` or `get_encryption_key_for_file`.
  """
  sections = {}
  while True:
    key_size = fp.read(4)
    if not key_size:
      break
    key_size = int.from_bytes(key_size, byteorder='little')
    key = fp.read(key_size).decode()
    value_size = fp.read(4)
    value_size = int.from_bytes(value_size, byteorder='little')
    value = fp.read(value_size * 4)
    value = _decrypt_bytes(value, encryption_key)
    sections[key] = value
  return sections


def write(data: dict, fp, encryption_key: str):
  """Serialises `data` (a dictionary where all the keys and values are
  strings) to `fp` (a `.write()`-supporting file-like object).

  The `encryption_key` can be obtained using either
  `get_encryption_key_for_string` or `get_encryption_key_for_file`.
  """
  # Checking the given dictionary
  for i, (key, value) in enumerate(data.items()):
    if not isinstance(key, str):
      raise TypeError(f"Key '{key}' in given dictionary is not a string")
    if not isinstance(value, str):
      raise TypeError(f"Value '{value}' in given dictionary is not a string")
  # Writing to the file object
  for key, value in data.items():
    # Writing key
    key = key.encode()
    key_size = len(key).to_bytes(4, byteorder='little')
    fp.write(key_size)
    fp.write(key)
    # Writing value
    value = value.encode()
    value = _encrypt_bytes(value, encryption_key)
    value_size = len(value) // 4
    value_size = value_size.to_bytes(4, byteorder='little')
    fp.write(value_size)
    fp.write(value)


def read_bytes(data: bytes or bytearray, encryption_key: str) -> dict:
  """Deserialises `data` (a `bytes` or `bytearray` instance) to a
  dictionary where all the keys and values are strings.

  The `encryption_key` can be obtained using either
  `get_encryption_key_for_string` or `get_encryption_key_for_file`.
  """
  with io.BytesIO(data) as fp:
    return read(fp, encryption_key)


def write_bytes(data: dict, encryption_key: str) -> bytes:
  """Serialises `data` (a dictionary where all the keys and values are
  strings) to `bytes`.

  The `encryption_key` can be obtained using either
  `get_encryption_key_for_string` or `get_encryption_key_for_file`.
  """
  file = io.BytesIO()
  write(data, file, encryption_key)
  return file.getvalue()


def read_file(file) -> dict:
  """Deserialises the contents of the `file` (a `str` or path-like
  object) to a dictionary where all the keys and values are strings.
  """
  encryption_key = get_encryption_key_for_file(file)
  with open(file, 'rb') as fp:
    return read(fp, encryption_key)


def write_file(data: dict, file):
  """Serialises `data` (a dictionary where all the keys and values are
  strings) and writes the result to the `file` (a `str` or path-like
  object).
  """
  encryption_key = get_encryption_key_for_file(file)
  with open(file, 'wb') as fp:
    write(data, fp, encryption_key)
