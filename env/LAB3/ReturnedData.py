import json

class ReturnedData(object):

    def __init__(self, success, message, data = []):
        self.success = success
        self.message = message
        self.data = data

    def addToData(self, node):
        self.data.append(node)

    def createJSON(self):
        rdata = {}
        rdata["success"] = self.success
        rdata["message"] = self.message
        rdata["data"] = self.data

        return json.dumps(rdata)
