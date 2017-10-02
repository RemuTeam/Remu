import json
from Domain.Command import Command


class Message:

    def __init__(self, json_data=None):
        self.fields = {}
        if json_data:
            self.fields = json.loads(json_data)

    def set_field(self, field, data):
        self.fields[field] = data

    def get_field(self, key):
        return self.fields[key]

    def to_json(self):
        return json.dumps(self.fields)

    def get_command(self):
        if "command" in self.fields:
            if self.fields["command"] in Command.__dict__.values():
                return self.fields["command"]
        return Command.INVALID_COMMAND
