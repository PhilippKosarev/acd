#! /usr/bin/env python3

# Imports
from libjam import Captain, typewriter
import os
import sys

# Trying to import readline so that input() will have history and such
try:
  import readline
except ModuleNotFoundError:
  pass

# Backend
from . import acd


class CLI:
  'A CLI tool for viewing, packing and unpacking Assetto Corsa Data (.acd) files'
  def view(self, filename: str):
    'View a given ACD file'
    data = acd.read_file(filename)
    keys = list(data.keys())
    lines = [typewriter.bolden('Available files:')]
    printable_keys = []
    for i, key in enumerate(keys):
      printable_keys.append(f'{i+1}) {key}')
    lines.append(typewriter.list_to_columns(printable_keys, spacing=2))
    lines.append('')
    print('\n'.join(lines))
    n_keys = len(keys)
    try:
      while True:
        choice = input(typewriter.bolden(
          f'Input which file to view (1-{n_keys}, 0 to abort): '
        )).strip()
        if choice == '':
          continue
        elif choice == '0':
          return 1
        elif choice in [str(n) for n in range(1, n_keys+1)]:
          chosen_key = keys[int(choice) - 1]
          break
        elif choice in keys:
          chosen_key = choice
          break
        else:
          print('Invalid input.')
    except KeyboardInterrupt:
      print()
      return 1
    text = data.get(chosen_key)
    print(f"{typewriter.bolden(f'{chosen_key}:')}\n{text.strip()}")

  def pack(self, input_directory: str, output_file: str):
    'Packs a directory into an ACD file'
    files = os.listdir(input_directory)
    # Converting to absolute paths
    files = [os.path.join(input_directory, file) for file in files]
    files = [file for file in files if os.path.isfile(file)]
    data = {}
    for file in files:
      basename = os.path.basename(file)
      with open(file, 'r') as f:
        contents = f.read()
      data[basename] = contents
    acd.write_file(output_file, data)

  def unpack(self, input_file: str, output_directory: str):
    'Unpacks an ACD file into a directory'
    data = acd.read_file(input_file)
    os.mkdir(output_directory)
    for key in data:
      value = data.get(key)
      path = os.path.join(output_directory, key)
      with open(path, 'w') as file:
        file.write(value)

cli = CLI()
captain = Captain(cli, 'acd', compact_help=True)

# Running
def main():
  function, args = captain.parse()
  return function(*args)

if __name__ == '__main__':
  sys.exit(main())