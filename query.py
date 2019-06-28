#!/usr/bin/env python3
import sys
from jinja2 import Environment, FileSystemLoader
from sqlitedict import SqliteDict


with open(sys.argv[1], 'r') as f:
    names = [line.split('|') for line in f.read().strip().split('\n')]

with open(sys.argv[2], 'r') as f:
    problems = [line.split('|') for line in f.read().strip().split('\n')]

with SqliteDict('./db.sqlite', autocommit=True) as d:
    body = []
    for i, (username, name) in enumerate(names):
        row = [0, username, name]
        scorelist = []
        total = 0
        for (_, chapter, problem) in problems:
            score = d.get('{}|{}|{}'.format(username, chapter, problem))
            if score is None:
                scorelist.append('')
            else:
                scorelist.append(score)
                total += score
        row.append(total)
        row.extend(scorelist)
        body.append(row)

body.sort(key=lambda x:x[3], reverse=True)
for i in range(len(body)):
    body[i][0] = i+1
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader,
                  extensions=['jinja2_time.TimeExtension'])
template = env.get_template('index.html')
output = template.render(problems=problems, body=body)

with open(sys.argv[3], "w") as f:
    f.write(output)
