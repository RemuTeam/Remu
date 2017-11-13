import json
from Domain.Command import Command
from Domain.MessageKeys import MessageKeys


class Message:
    """
    A class to be used for serializing json messages
    """

    def __init__(self, json_data=None):
        """
        Constructor

        json_data:  data as json object to be
                    converted to a Message object
        """
        self.fields = {}
        if json_data:
            self.fields = json.loads(json_data)

    def set_field(self, field, data):
        """
        Sets the value of a Message object field

        field:  the field to populate
        data:   the data to populate the field with
        """
        self.fields[field] = data

    def get_field(self, key):
        """
        Returns the value of a Message object's field

        key:        the name of the field to retrieve data from
        returns:    None if the field is not found,
                    the field's value otherwise
        """
        if key in self.fields:
            return self.fields[key]
        return None

    def to_json(self):
        """
        Returns the message as a json object
        """
        return json.dumps(self.fields)

    def get_command(self):
        """
        Returns the Message object's command-field's value

        returns:    an integer corresponding to a Command enumeration
        """
        command_key = MessageKeys.command_key
        if command_key in self.fields:
            if self.fields[command_key] in list(map(int, Command)):
                return self.fields[command_key]
        return Command.INVALID_COMMAND.value

    def get_response(self):
        """
        Returns the Message object's responseTo-field's value

        returns:    an integer corresponding to a Command enumeration
        """
        response_to_key = MessageKeys.response_key
        if response_to_key in self.fields:
            if self.fields[response_to_key] in list(map(int, Command)):
                return self.fields[response_to_key]
        return Command.INVALID_COMMAND.value

    def get_data(self):
        """
        Returns the Message object's data-field's value

        returns:    an object
        """
        data_key = MessageKeys.data_key
        if data_key in self.fields:
            return self.fields[data_key]
        return None