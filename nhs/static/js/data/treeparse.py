import json

bnf = json.loads(open('bnftree.json').read())
chapters = [c for c in bnf if c['level'] == 'chapter']
sections = [s for s in bnf if s['level'] == 'section']
paragraphs = [p for p in bnf if p['level'] == 'paragraph']

bnftree = {}

for chap in chapters:
    bnftree[chap['chapter']] = dict(
        nodeName=chap['title'],
        bnfPart = chap['bnf'],
        nodes = {}
        )

for sect in sections:
    bnftree[sect['chapter']]['nodes'][sect['section']] = dict(
        nodeName=sect['title'],
        bnfPart=sect['bnf'],
        nodes = {}
        )

for par in paragraphs:
    bnftree[par['chapter']]['nodes'][par['section']]['nodes'][par['paragraph']] = dict(
        nodeName=par['title'],
        bnfPart=par['bnf']
        )

for chapt in bnftree:
    for para in bnftree[chapt]['nodes']:
        bnftree[chapt]['nodes'][para]['nodes'] = bnftree[chapt]['nodes'][para]['nodes'].values()
    bnftree[chapt]['nodes'] = bnftree[chapt]['nodes'].values()
bnftree = bnftree.values()

print json.dumps(bnftree, indent=2)
