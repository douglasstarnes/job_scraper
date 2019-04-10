from flask import Flask, render_template, request
import pandas as pd
import json
import utils

app = Flask(__name__)

def _get_us_jobs():
    with open('jobs_250.json', 'r') as f:
        product = utils.tag_job_product(json.loads(''.join(f.readlines())))
        df = pd.DataFrame(product, columns=['soc_id', 'title', 'company', 'location', 'remote', 'relocation', 'tag'])
    tmp_columns = df.location.str.split(',', expand=True)
    df['city'] = tmp_columns[0].str.strip()
    df['state'] = tmp_columns[1].str.strip()
    df = df.drop('location', axis=1)
    return df[df.state.apply(lambda state: state in utils.get_states())]

df = _get_us_jobs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    jobs = df[df.tag == request.form['search_term']]
    return render_template('search.html', no_jobs=len(jobs), jobs=[job[1] for job in jobs.iterrows()], search_term=request.form['search_term'])


@app.route('/details/<soc_id>')
def details(soc_id):
    jobs = df[df.soc_id == soc_id]
    tags = [job[1]['tag'] for job in jobs.iterrows()]
    return render_template('details.html', 
        title = jobs.iloc[0]['title'], 
        company = jobs.iloc[0]['company'],
        city = jobs.iloc[0]['city'],
        state = jobs.iloc[0]['state'],
        remote = jobs.iloc[0]['remote'],
        relocation = jobs.iloc[0]['relocation'],
        tags = ', '.join(tags))


@app.route('/state', methods=['GET', 'POST'])
def state():
    if request.method == 'POST':
        jobs = df[df.state == request.form['state']].groupby('soc_id').first().reset_index()
        jobs = [job[1] for job in jobs.iterrows()]
        return render_template('state_list.html', jobs=jobs, no_jobs=len(jobs), state=request.form['state'])
    else:
        return render_template('state_search.html', states=utils.get_states())