import logging
from pymongo import MongoClient


client = MongoClient()
db = client.generator


def set_initial_db_state():
    print('Setting db state on boot on off')
    logging.info('Setting db state on boot to off')
    db.generator_state.update_one({'_id': '59663b5df344225ae3d823cb'}, {"$set": {"state": False}}, upsert=True)


def set_gen_state(state, time_stamp):
    if state:
        state_print = "up"
    else:
        state_print = "down"
    print('{} {}'.format('Setting state to:', state_print))
    logging.info('{} {}'.format('Setting state to:', state_print))
    db.generator_state.update_one({'_id':'59663b5df344225ae3d823cb'}, {"$set": {"state": state}}, upsert=True)
    db.generator_state.insert_one({"state": state_print, "time_stamp": time_stamp})
    # cursor = db.generator_state.find({'state': state})
    # for document in cursor:
    #     print(document)
            # return bool(document['state'])


def get_gen_state():
    print('getting generator status')
    cursor = db.generator_state.find({})
    for document in cursor:
        print'The generator status is: ' + str(document['state'])
        return str(document['state'])
