import logging
from logger import logging_handler
from os import path, uname
from pymongo import MongoClient
from configuration import get_db_creds

env = get_db_creds('env')
test_uri = get_db_creds('test_uri')
prod_uri = get_db_creds('prod_uri')

if env == 'test':
    client = MongoClient(test_uri)
    db = client.raspgen_test
else:
    client = MongoClient(prod_uri)
    db = client.raspgen

if uname()[1] == 'DietPi':
    db = client.raspgen
else:
    db = client.raspgen_test
print(db)


def set_initial_db_state():
    msg = 'Setting db state on boot on off'
    logging_handler(msg)
    db.generator_state.update_one({'_id': 'gen_state'}, {"$set": {"state": False}}, upsert=True)
    success_msg = 'status set successfully'
    logging.info(success_msg)


def set_gen_state(state, time_stamp):
    if state:
        state_print = "up"
    else:
        state_print = "down"
    msg = '{} {}'.format('Setting state to:', state_print)
    logging_handler(msg)
    db.generator_state.update_one({'_id':'gen_state'}, {"$set": {"state": state}}, upsert=True)
    db.generator_log.insert_one({"state": state_print, "time_stamp": time_stamp})


def set_time_spent(time_spent):
    db.time_spent.insert_one({"time_span": time_spent})


def get_gen_state():
    msg = 'Getting generator status'
    logging_handler(msg)
    cursor = db.generator_state.find({})
    for document in cursor:
        if document['state'] is False:
            gen_state = 'down'
        else:
            gen_state = 'up'
        msg = '{} {}'.format('Generator status is:', gen_state)
        logging_handler(msg)
        return str(gen_state)
