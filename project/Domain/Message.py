import json

class Message:

    def __init__(self, json_data=None):
        self.fields = {}
        if json_data:
            self.fields = json.loads(json_data)

    def set_field(self, field, data):
        self.fields[field] = data

    def to_json(self):
        return json.dumps(self.fields)

