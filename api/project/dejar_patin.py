import requests
import json
import config

def dejar_patin(id_patin, id_slot):
    endpoint = "http://" + config.api_host + "/api/slots/dejar_patin"
    body = {
	    "patin": id_patin,
		"slot": id_slot
    }
    r = requests.post(url = endpoint, json = body)
    print(r.text)

dejar_patin(1, 1)