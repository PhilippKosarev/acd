#! /usr/bin/env python3

# Imports
from libjam import Captain, typewriter, flashcard
from pathlib import Path
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
  def view(self, acd_file: str):
    'View a given ACD file'
    data = acd.read_file(acd_file)
    data = dict(sorted(data.items()))
    keys = list(data.keys())
    print(typewriter.bolden('Available files:'))
    try:
      chosen_key = flashcard.choose(
        'Select which file to view',
        keys,
        typewriter.Style.BOLD,
      )
    except KeyboardInterrupt:
      print('^C')
      return 130
    if not chosen_key:
      return
    text = data.get(chosen_key).strip()
    title = typewriter.bolden(chosen_key + ':')
    print(title + '\n' + text)

  def pack(self, directory: str, acd_file: str):
    'Packs a directory into an ACD file'
    directory = Path(directory)
    files = [file for file in directory.iterdir() if file.is_file()]
    data = {file.name: file.read_text() for file in files}
    data = dict(sorted(data.items()))
    acd.write_file(acd_file, data)

  def unpack(self, acd_file: str, directory: str):
    'Unpacks an ACD file into a directory'
    directory = Path(directory)
    directory.mkdir()
    data = acd.read_file(acd_file)
    for key, value in sorted(data.items()):
      file = directory / key
      file.write_text(value)


# Creating the cli
cli = CLI()
captain = Captain(cli, 'acd', compact_help=True)

def main():
  function, args = captain.parse()
  return function(*args)

if __name__ == '__main__':
  sys.exit(main())