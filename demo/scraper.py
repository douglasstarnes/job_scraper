import requests
from bs4 import BeautifulSoup
import json
import time

page = 1
jobs_url = 'https://stackoverflow.com/jobs?sort=p'
jobs_url += '&pg={}'
jobs = []

while page <= 40:
    print('page {}'.format(str(page)))
    q = requests.get(jobs_url.format(page))
    html = q.text
    soup = BeautifulSoup(html, 'html.parser')

    job_list = soup.find_all('div', class_='-job')
    for el_job in job_list:
        job_id = el_job['data-jobid']
        el_title = el_job.find('h2', class_='job-details__spaced')
        job_title = el_title.find('a')['title']
        el_company = el_job.find('div', class_='-company')
        job_company = el_company.find('span').text.strip()
        job_location = el_company.find('span', class_='fc-black-500').text.strip()[1:].strip()
        job_remote = False
        job_relocation = False 
        el_perks = el_job.find('div', class_='-perks')
        if el_perks is not None:
            job_remote = el_perks.find('span', class_='-remote') is not None 
            job_relocation = el_perks.find('span', class_='-relocation') is not None 
        tag_div = el_job.find('div', class_='-tags')
        tags = []
        if tag_div is not None:
            tag_list = tag_div.find_all('a', class_='post-tag')
            tags = [tag.text for tag in tag_list]
        jobs.append({
            'soc_id': job_id,
            'title': job_title,
            'company': job_company,
            'location': job_location,
            'remote': job_remote,
            'relocation': job_relocation,
            'tags': tags
        })
    page += 1
    time.sleep(.1)

with open('jobs_40.json', 'w') as f:
    f.write(json.dumps(jobs))
