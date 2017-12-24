import logging
from logger import logging_handler
from os import uname
from pymongo import MongoClient, errors
from configuration import get_db_creds

env = get_db_creds('env')
test_uri = get_db_creds('test_uri')
prod_uri = get_db_creds('prod_uri')


if uname()[1] == 'DietPi':
    client = MongoClient(prod_uri)
    db = client.raspgen
else:
    client = MongoClient(test_uri)
    db = client.raspgen_test
print(db)


def set_initial_db_state():
    """"Sets the state entry in DB to off on boot"""
    msg = 'Setting db state on boot on off'
    logging_handler(msg)
    try:
        db.generator_state.update_one({'_id': 'gen_state'}, {"$set": {"state": False}}, upsert=True)
        success_msg = 'status set successfully'
        logging.info(success_msg)
    except (AttributeError, errors.OperationFailure):
        error_msg = 'There was a problem setting up db initial status'
        logging_handler(error_msg)


def get_gen_state():
    """"Gets generator's status"""
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


def set_gen_state(state, time_stamp):
    """"Sets generator state with a timestamp and adds an entry to the log"""
    if state:
        state_print = "up"
    else:
        state_print = "down"
    msg = '{} {}'.format('Setting state to:', state_print)
    success_msg = '{} {} {}'.format('Setting state to:', state_print, 'was successful')
    error_msg = '{} {} {}'.format('Setting state to:', state_print, 'was not successful')
    logging_handler(msg)
    try:
        db.generator_state.update_one({'_id':'gen_state'}, {"$set": {"state": state}}, upsert=True)
        db.generator_log.insert_one({"state": state_print, "time_stamp": time_stamp})
        logging_handler(success_msg)
    except (AttributeError, errors.OperationFailure):
        logging_handler(error_msg)


def get_time_spent(month):
    """"Gets generator's time spent on in seconds"""
    time_sum_seconds =[]
    cursor = db.time_spent.find({})
    for document in cursor:
        if month == document['time_stamp'].month:
            time_sum_seconds.append(document['time_span'])
    return sum(time_sum_seconds)


def set_time_spent(time_stamp, time_span):
    """"Sets generator's time spent on"""
    db.time_spent.insert_one({"time_stamp": time_stamp, "time_span": time_span})
