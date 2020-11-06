import locale
from itertools import islice

import petl
from petl import config
from petl.compat import text_type
from petl.io.sources import MemorySource

# code from https://petl.readthedocs.io/en/stable/_modules/petl/util/vis.html#displayall
# TODO: no way to make it work out of the box, i had to recopy a part of the file, should be owk with a table.display()


# Ugly, Monkey Patch some function to add some css class, will need a full refactoring
def _write_begin(f, flds, lineterminator, caption, index_header, truncate):
    f.write("<table class='table'>" + lineterminator)
    if caption is not None:
        f.write(('<caption>%s</caption>' % caption) + lineterminator)
    f.write('<thead class="thead-light">' + lineterminator)
    f.write('<tr>' + lineterminator)
    for i, h in enumerate(flds):
        if index_header:
            h = '%s|%s' % (i, h)
        if truncate:
            h = h[:truncate]
        f.write(('<th scope="col">%s</th>' % h) + lineterminator)
    f.write('</tr>' + lineterminator)
    f.write('</thead>' + lineterminator)
    f.write('<tbody>' + lineterminator)


petl.io.html._write_begin = _write_begin

from petl.io.html import tohtml


def _vis_overflow(table, limit):
    overflow = False
    if limit:
        # try reading one more than the limit, to see if there are more rows
        table = list(islice(table, 0, limit + 2))
        if len(table) > limit + 1:
            overflow = True
            table = table[:-1]
    return table, overflow


def display_html(table, limit=0, vrepr=None, index_header=None, caption=None,
                 tr_style=None, td_styles=None, encoding=None,
                 truncate=None, epilogue=None):
    # determine defaults
    if limit == 0:
        limit = config.display_limit
    if vrepr is None:
        vrepr = config.display_vrepr
    if index_header is None:
        index_header = config.display_index_header
    if encoding is None:
        encoding = locale.getpreferredencoding()

    table, overflow = _vis_overflow(table, limit)
    buf = MemorySource()
    tohtml(table, buf, encoding=encoding, index_header=index_header,
           vrepr=vrepr, caption=caption, tr_style=tr_style,
           td_styles=td_styles, truncate=truncate)
    output = text_type(buf.getvalue(), encoding)

    if epilogue:
        output += '<p>%s</p>' % epilogue
    elif overflow:
        output += '<p><strong>...</strong></p>'

    return output
