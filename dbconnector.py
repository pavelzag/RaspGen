from pymongo import MongoClient


client = MongoClient()
db = client.generator


def set_gen_state(state):
    print('setting')
    db.generator_state.update_one({'_id':'59663b5df344225ae3d823cb'}, {"$set": {"state": state}}, upsert=True)
    cursor = db.generator_state.find({'state': state})
    for document in cursor:
        print(document)
        return bool(document['state'])


def get_gen_state():
    print('getting generator status')
    cursor = db.generator_state.find({})
    for document in cursor:
        print'The generator status is: ' + str(document['state'])
        return str(document['state'])
