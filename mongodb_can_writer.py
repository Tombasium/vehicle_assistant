from can import Listener
import pymongo, bson


class mongodb_can_writer(Listener):

    def __init__(self, local=True):
        if local:
            self.client = pymongo.MongoClient('localhost', 27017)
        else:
            self.client = pymongo.MongoClient('')

        self.db = self.client.can_msgs

        self.collection = self.db.raw_can_data

    def on_message_received(self, msg):
        post = {'timestamp': msg.timestamp,
                'ID': msg.arbitration_id,
                'data': bson.Binary(msg.data)
                }
        self.collection.insert_one(post)