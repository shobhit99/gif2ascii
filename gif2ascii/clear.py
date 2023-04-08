from os import linesep

def clear(width, rows=-1, rows_max=None, *, calling_line=True, absolute=None,
          store_max=[]):
    width = int(width)
    if rows_max and rows_max != -1:
        store_max[:] = [rows_max, False]
    elif not store_max or store_max[1] or rows_max == -1 or absolute:
        try:
            from shutil import get_terminal_size
            columns_max, rows_max = get_terminal_size()
        except ImportError:
            columns_max, rows_max = width, 24
        if absolute is None:
            store_max[:] = [rows_max, True]
    if store_max:
        if rows == -1:
            rows = store_max[0]
        elif isinstance(rows, float):
            rows = round(store_max[0] * rows)
        if rows > store_max[0] - 2:
            rows = store_max[0] - 2
    if absolute is None:
        s = ('\033[1A' + ' ' * 30 if calling_line else '') + linesep * rows
    else:
        s = '\033[{}A'.format(absolute + 2) + linesep
        if absolute > rows_max - 2:
            absolute = rows_max - 2
        s += (' ' * width + linesep) * absolute + ' ' * width
        rows = absolute
    print(s + '\033[{}A'.format(rows + 1))