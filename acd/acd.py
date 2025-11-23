# Imports
import os, io

# Returns the encryption key for a given file.
def get_encryption_key(filename: str) -> str:
  # Getting string
  filename = os.path.abspath(filename)
  string = os.path.basename(filename)
  if string.lower().startswith('data'):
    string = os.path.basename(os.path.dirname(filename))
  # Getting key
  items = []
  string = string.lower()
  n_chars = len(string)
  string_ord = [ord(char) for char in string]
  # Getting byte1
  items.append(sum(string_ord))
  # Getting byte2
  num = 0
  for i in range(0, n_chars - 1, 2):
    num = num * string_ord[i] - string_ord[i+1]
  items.append(num)
  # Getting byte3
  escape_char = '\u001b'
  escape_ord = ord(escape_char)
  num = 0
  for i in range(1, n_chars - 3, 3):
    num *= string_ord[i]
    divisor = string_ord[i+1] + escape_ord
    num = int(num / divisor)
    num += -27 - string_ord[i-1]
  items.append(num)
  # Getting byte4
  num = 5763
  for i in range(1, n_chars):
    num -= string_ord[i]
  items.append(num)
  # Getting byte5
  shift_in_char = '\u000f'
  shift_in_ord = ord(shift_in_char)
  num = 66
  for i in range(1, n_chars - 4, 4):
    num = num * (string_ord[i] + shift_in_ord) * (string_ord[i-1] + shift_in_ord) + 22
  items.append(num)
  # Getting byte6
  num = 101
  for i in range(0, n_chars - 2, 2):
    num -= ord(string[i])
  items.append(num)
  # Getting byte7
  num = 171
  for i in range(0, n_chars - 2, 2):
    num = num % string_ord[i]
  items.append(num)
  # Getting byte8
  num = 171
  for i in range(n_chars - 1):
    num = int(num / string_ord[i]) + string_ord[i+1]
  items.append(num)
  # Returning
  return '-'.join([str(item % 256) for item in items])

# Decrypts an enctyped string.
def decrypt_bytes(data: bytes, encryption_key: str) -> str:
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

# Encrypts bytes.
def encrypt_bytes(data: bytes, encryption_key: str) -> bytes:
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
  # Adding padding bytes
  padded_data = bytearray(len(data) * 4)
  for i in range(len(data)):
    padded_data[i*4] = data[i]
    for n in range(1, 4):
      padded_data[i*4+n] = 0
  # Returning
  return padded_data

# Encrypts a string.
def encrypt_string(string: str, encryption_key: str) -> bytes:
  data = string.encode()
  return encrypt_bytes(data, encryption_key)

# Reads given bytes as file.
def read_bytes(data: bytes, encryption_key: str) -> dict:
  sections = {}
  file = io.BytesIO(data)
  while True:
    key_size = file.read(4)
    if not key_size:
      break
    key_size = int.from_bytes(key_size, byteorder='little')
    key = file.read(key_size).decode()
    value_size = file.read(4)
    value_size = int.from_bytes(value_size, byteorder='little')
    value = file.read(value_size * 4)
    sections[key] = decrypt_bytes(value, encryption_key)
  file.close()
  return sections

# Reads an acd file and returns a dict.
def read_file(filename: str) -> dict:
  key = get_encryption_key(filename)
  with open(filename, 'rb') as file:
    data = read_bytes(file.read(), key)
  return data

# Writes an acd from dict.
# The given dictionary can only have strings as its keys and values.
def write_file(filename: str, data: dict):
  data = dict(sorted(data.items()))
  encryption_key = get_encryption_key(filename)
  result_bytes = bytearray()
  for key in data:
    value = data.get(key)
    value = encrypt_string(value, encryption_key)
    value_size = (len(value) // 4).to_bytes(4, byteorder='little')
    key_size = len(key).to_bytes(4, byteorder='little')
    result_bytes.extend(key_size)
    result_bytes.extend(key.encode())
    result_bytes.extend(value_size)
    result_bytes.extend(value)
  with open(filename, 'wb') as file:
    file.write(result_bytes)