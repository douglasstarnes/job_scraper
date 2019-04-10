import requests
from bs4 import BeautifulSoup
from collections import Counter
import json

page = 1
jobs_url = 'https://stackoverflow.com/jobs?sort=p'
jobs_url += '&pg={}'
tag_counter = Counter()

while page <= 40:
    q = requests.get(jobs_url.format(str(page)))
    html = q.text
    soup = BeautifulSoup(html, 'html.parser')

    job_list = soup.find_all('div', class_='-job')
    for el_job in job_list:
        tag_div = el_job.find('div', class_='-tags')
        if tag_div is not None:
            tag_list = tag_div.find_all('a', class_='post-tag')
            for tag in tag_list:
                tag_counter[tag.text] += 1

    page += 1

for (index, (tag, count)) in enumerate(tag_counter.most_common(25)):
    print('Tag {}: {}, {} job{}'.format(str(index + 1), tag, str(count), 's' if count > 1 else ''))

with open('tags.json', 'w') as f:
    f.write(json.dumps(tag_counter))
