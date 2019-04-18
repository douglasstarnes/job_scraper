class Job(object):
    def __init__(self, id, title, company, location, tags=[], remote=False, relocation=False):
        self.id = id
        self.title = title
        self.company = company
        self.location = location
        self.tags = tags
        self.remote = remote
        self.relocation = relocation 

    def __repr__(self):
        return '<Job {}>'.format(self.title)

    def add_tag(self, tag):
        """
        Adds ``tag`` if it does not already exist
        """
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
        """
        Removes ``tag`` if it already exists
        """
        if tag in self.tags:
            self.tags.remove(tag)

    @classmethod
    def from_json(cls, json_data):
        return cls(json_data['soc_id'], json_data['title'], json_data['company'], json_data['location'], json_data['tags'], json_data['remote'], json_data['relocation'])
    