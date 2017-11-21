import logging
from pymongo import MongoClient


client = MongoClient()
db = client.generator


def set_initial_db_state():
    print('Setting db state on boot on off')
    logging.info('Setting db state on boot to off')
    db.generator_state.update_one({'_id': 'gen_state'}, {"$set": {"state": False}}, upsert=True)


def set_gen_state(state, time_stamp):
    if state:
        state_print = "up"
    else:
        state_print = "down"
    print('{} {}'.format('Setting state to:', state_print))
    logging.info('{} {}'.format('Setting state to:', state_print))
    db.generator_state.update_one({'_id':'gen_state'}, {"$set": {"state": state}}, upsert=True)
    db.generator_log.insert_one({"state": state_print, "time_stamp": time_stamp})
    # cursor = db.generator_state.find({'state': state})
    # for document in cursor:
    #     print(document)
            # return bool(document['state'])


def set_time_spent(time_spent):
    db.time_spent.insert_one({"time_span": time_spent})


def get_gen_state():
    print('Getting generator status')
    cursor = db.generator_state.find({})
    for document in cursor:
        if document['state'] is False:
            gen_state = 'down'
        else:
            gen_state = 'up'
        print('{} {}'.format('Generator status is:', gen_state))
        return gen_state
