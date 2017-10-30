import json
from Domain.Command import Command
from Domain.MessageKeys import MessageKeys


"""
A class to be used for serializing json messages
"""
class Message:

    """
    Constructor

    json_data:  data as json object to be
                converted to a Message object
    """
    def __init__(self, json_data=None):
        self.fields = {}
        if json_data:
            self.fields = json.loads(json_data)

    """
    Sets the value of a Message object field
    
    field:  the field to populate
    data:   the data to populate the field with
    """
    def set_field(self, field, data):
        self.fields[field] = data

    """
    Returns the value of a Message object's field
    
    key:        the name of the field to retrieve data from
    returns:    None if the field is not found, 
                the field's value otherwise
    """
    def get_field(self, key):
        if key in self.fields:
            return self.fields[key]
        return None

    """
    Returns the message as a json object
    """
    def to_json(self):
        return json.dumps(self.fields)

    """
    Returns the Message object's command-field's value
    
    returns:    an integer corresponding to a Command enumeration
    """
    def get_command(self):
        command_key = MessageKeys.command_key
        if command_key in self.fields:
            if self.fields[command_key] in list(map(int, Command)):
                return self.fields[command_key]
        return Command.INVALID_COMMAND.value

    """
    Returns the Message object's responseTo-field's value
    
    returns:    an integer corresponding to a Command enumeration
    """
    def get_response(self):
        response_to_key = MessageKeys.response_key
        if response_to_key in self.fields:
            if self.fields[response_to_key] in list(map(int, Command)):
                return self.fields[response_to_key]
        return Command.INVALID_COMMAND.value

    """
    Returns the Message object's data-field's value

    returns:    an object
    """
    def get_data(self):
        data_key = MessageKeys.data_key
        if data_key in self.fields:
            return self.fields[data_key]
        return None