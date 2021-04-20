import json
import hashlib

def gerarHash(jsonstr):
    h = hashlib.new('ripemd160')
    h.update(jsonstr.encode())
    return h.hexdigest()

def key_model(data):
    ret = 'model'
    for key, value in data.items():
        ret = ret + '_' + key + '_' + value

    return ret

def what_anomaly(data):
    ret = ''
    for key, value in data.items():
        ret = ret + key + ' = ' + value + ' | '

    return ret