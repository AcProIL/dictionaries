'''Build dictionaries'''

from os import system
from glob import glob
from re import search
from csv import reader
from operator import itemgetter

with open('LaTeX/header.tex', 'r') as f:
    header = f.read()
with open('LaTeX/footer.tex', 'r') as f:
    footer = f.read()

langs = {
    'eng': 'English', 'fra': 'Français'
}

paths = glob('data/*.csv')

for path in paths:
    entries = []
    with open(path, newline='') as file:
        for row in reader(file):
            entries.append(row)

    lang = search(r'data/(.*)\.csv', path).group(1)

    # Forward dictionary
    entries = sorted(entries, key=itemgetter(1))
    content = r'\title{' + langs[lang]
    content += r' \textrightarrow{} Latino sine flexione}\maketitle'
    letter = ''
    for entry in entries:
        pos, src, tgt, ex_src, ex_tgt = entry
        if src[0].upper() != letter:
            content += '\\chapter*{%s}' % src[0].upper()
        letter = src[0].upper()
        content += '\n\\entry'
        content += '{%s}{%s}{%s}{%s}{%s}' % (pos, src, tgt, ex_tgt, ex_src)

    out = 'dictionaries/' + lang + '-lsf.tex'
    print('Export', out)
    with open(out, 'w') as f:
        f.write(header + content + footer)
    system('pdflatex -output-directory dictionaries ' + out)

    # Backward dictionary
    entries = sorted(entries, key=itemgetter(2))
    content = r'\title{Latino sine flexione \textrightarrow{} '
    content += langs[lang] + r'}\maketitle'
    letter = ''
    for entry in entries:
        pos, tgt, src, ex_tgt, ex_src = entry
        if src[0].upper() != letter:
            content += '\\chapter*{%s}' % src[0].upper()
        letter = src[0].upper()
        content += '\n\\entry'
        content += '{%s}{%s}{%s}{%s}{%s}' % (pos, src, tgt, ex_tgt, ex_src)

    out = 'dictionaries/lsf-' + lang + '.tex'
    print('Export', out)
    with open(out, 'w') as f:
        f.write(header + content + footer)
    system('pdflatex -output-directory dictionaries ' + out)
