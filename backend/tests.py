import re

data = '* REPORT 1 AUDIO_GAIN 18 *'

def mapping(data):
    data = data.split()
    return {"rx": data[2], "cmd": data[3], "value": data[4]}

print( mapping(data) )