"""A utility for working with Assetto Corsa Data (.acd) files."""

# Imports
import os
import sys
import math
import shutil
import argparse

# Trying to import readline so that input() will have history and such
try:
  import readline
except ModuleNotFoundError:
  pass

# Importing the backend
from . import acd


def _bold(s: str) -> str:
  """Wraps the string in ANSII escape codes so it appears bold in the
  terminal.
  """
  return f'\x1b[1m{s}\x1b[22m'


def _to_columns(items: list) -> str:
  """Arranges a list of strings in columns."""
  prefix = '  '
  lengths = [len(s) + len(prefix) for s in items]
  column_width = max(lengths)
  term_width = shutil.get_terminal_size()[0]
  n_columns = math.floor(term_width / (column_width + len(prefix)))
  n_rows = math.ceil(len(items) / n_columns)
  rows = [[] for i in range(n_rows)]
  for i, item in enumerate(items):
    j = i % n_rows
    item = f'{prefix}{item:<{column_width}}'
    rows[j].append(item)
  text = '\n'.join([''.join(r).rstrip() for r in rows])
  return text


def _select(title: str, items: list, prompt: str) -> str or None:
  """Asks the user to select one item from a list."""
  # Creating the prompt
  title = _bold(title + ':')
  n_items = len(items)
  prompt = _bold(f'{prompt} (1-{n_items}, 0 to abort): ')
  # Printing available items
  text = [f'{i}) {item}' for i, item in enumerate(items, start=1)]
  text = _to_columns(text)
  print(f'{title}\n{text}\n')
  # Getting user input
  while True:
    choice = input(prompt).strip()
    if choice == '0':
      return None
    elif choice in [str(n) for n in range(1, n_items + 1)]:
      return items[int(choice) - 1]
    elif choice in items:
      return choice


def _read_file(file) -> str:
  with open(file) as fp:
    return fp.read()


def _write_file(value: str, file):
  with open(file, 'w') as fp:
    fp.write(value)


_error_messages = {
  FileNotFoundError: 'no such file or directory',
  FileExistsError: 'already exists',
  IsADirectoryError: 'not a file',
  PermissionError: 'permission denied',
  UnicodeDecodeError: 'invalid encoding',
  EOFError: 'unexpected end of file',
}


def _file_op(
  parser, func: callable, *args, ignore: list = [],
) -> any:
  """Performs a specified file operation while handling possible
  exceptions.
  """
  assert len(args) > 0
  try:
    return func(*args)
  except tuple(_error_messages.keys()) as e:
    exception = type(e)
  if exception in ignore:
    return
  message = _error_messages[exception]
  parser.error(f'{args[-1]}: {message}')


def view(parser, filename: str, item: str = None):
  """Prints the selected item from a file."""
  data = _file_op(parser, acd.read_file, filename)
  data = dict(sorted(data.items()))
  items = list(data.keys())
  if not item:
    try:
      item = _select(
        'Available items', items,
        'Select which item to view',
      )
    except KeyboardInterrupt:
      print('^C', file=sys.stderr)
      return 130
    if not item:
      return
    value = data[item]
  else:
    value = data.get(item)
    if value is None:
      parser.error(f'{filename}: {item}: no such item')
  print(value.strip())


def pack(parser, directory: str, filename: str):
  """Packs a directory into a file."""
  data = {}
  for name in sorted(os.listdir(directory)):
    file = os.path.join(directory, name)
    if not os.path.isfile(file):
      continue
    data[name] = _file_op(parser, _read_file, file)
  _file_op(parser, acd.write_file, data, filename)


def unpack(parser, filename: str, directory: str):
  """Unpacks a file into a directory."""
  data = _file_op(parser, acd.read_file, filename)
  _file_op(parser, os.mkdir, directory, ignore=[FileExistsError])
  for name, value in data.items():
    file = os.path.join(directory, name)
    _file_op(parser, _write_file, value, file)


# Creating the parser
main_parser = argparse.ArgumentParser(
  'acd', description=__doc__, add_help=False,
)
main_parser.add_argument(
  '-h', '--help', action='help', default=argparse.SUPPRESS,
  help='Prints this page.',
)
subparsers = main_parser.add_subparsers(
  title='commands', dest='command', required=True,
)
# View command
view_parser = subparsers.add_parser(
  'view', help=view.__doc__, description=view.__doc__,
)
view_parser.add_argument('filename')
view_parser.add_argument('item', nargs='?')
# Pack command
pack_parser = subparsers.add_parser(
  'pack', help=pack.__doc__, description=pack.__doc__,
)
pack_parser.add_argument('directory')
pack_parser.add_argument('filename')
# Unpack command
unpack_parser = subparsers.add_parser(
  'unpack', help=unpack.__doc__, description=unpack.__doc__,
)
unpack_parser.add_argument('filename')
unpack_parser.add_argument('directory')


def main(args: list = None) -> int:
  """Runs the CLI and returns the exit code."""
  args = tuple(vars(main_parser.parse_args(args)).values())
  command, args = args[0], args[1:]
  match command:
    case 'view':
      function, parser = view, view_parser
    case 'pack':
      function, parser = pack, pack_parser
    case 'unpack':
      function, parser = unpack, unpack_parser
  return function(parser, *args) or 0


if __name__ == '__main__':
  sys.exit(main())
