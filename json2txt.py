import os
import json
import demjson


def get_text(sub):
    text = ''

    if 'c' in sub and sub['t'] != 'note':
        for word in sub['c']:
            # word
            if isinstance(word, unicode):
                text += word
            # dict
            else:
                text += get_text(word)

        if sub['t'] == 'p':
            text += '\n'

    #if text and text[-1] != '.':
    #    text += '.'

    return text


def json_load(d):
    return demjson.decode(d)
    d = d.replace('c:', '"c":') \
        .replace('t:', '"t":') \
        .replace('xp:', '"xp":') \
        .replace('role:', '"role":') \
        .replace('f:', '"f":')\
        .replace('href:', '"href":')
    return json.loads(d)


def conv(d):
    out = ['']
    titles = ['Start']

    for sub in d:
        paragraph = False
        if sub['t'] == 'title':
            titles += [get_text(sub)]
            out += ['']

        elif 'c' in sub:
            out[-1] += get_text(sub)

            if paragraph:
                out[-1] += '\n'

    return titles, out


all = []
root_dir = 'path_to_js_files'  # path to .js files from litres
for f in sorted(os.listdir(root_dir)):
    if os.path.isdir(root_dir + '/' + f):
        continue

    print '-------->', f
    d = open(root_dir + '/' + f, 'r').read()
    all += json_load(d)

titles, out = conv(all)
for i, (t, o) in enumerate(zip(titles, out)):
    text = t.upper() + '\n' + o
    out_name = '%0.2i' % i + '.txt'
    open(root_dir + 'txt/' + out_name, 'w').write(text.encode('utf-8'))
