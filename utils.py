def get_states():
    f = open('states.txt', 'r')
    lines = f.readlines()
    f.close()

    return [line.strip()[-2:] for line in lines]

def tag_job_product(json_data):
    product = []
    for job in json_data:
        for tag in job['tags']:
            product.append([
                job['soc_id'], 
                job['title'],
                job['company'],
                job['location'],
                job['remote'],
                job['relocation'],
                tag])
    return product
