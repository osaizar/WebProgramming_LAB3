import json

class Message(object):

    def __init__(self, writer, reader, content):
        self.writer = writer
        self.reader = reader
        self.content = content

    def Message(self):
        return self

    def createJSON(self):
        rdata = {}
        rdata["writer"] = self.writer
        rdata["reader"] = self.reader
        rdata["content"] = self.content

        return json.dumps(rdata)
