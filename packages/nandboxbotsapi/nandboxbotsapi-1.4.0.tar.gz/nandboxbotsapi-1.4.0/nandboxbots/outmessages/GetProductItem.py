# Assuming OutMessage class is imported or defined elsewhere
from nandboxbots.outmessages.OutMessage import OutMessage
import json

class GetProductItemOutMessage(OutMessage):
    def __init__(self):
        super().__init__()
        self.method = "getProductDetail"
        self.id = None

    def to_json_obj(self):
        _, dictionary = super().to_json_obj()
        if self.id:
            dictionary['id'] = self.id
        return json.dumps(dictionary),  dictionary
