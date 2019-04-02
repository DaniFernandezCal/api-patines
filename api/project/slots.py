from flask import Flask, request, jsonify, Blueprint
from mongo_utils import slots, patines, rents
from bson.json_util import dumps


slots_api = Blueprint('slots', __name__)

class Slot():
    _id = 0
    patin = 0
    location = ""
    def __init__(self, id, location):
        self._id = id
        self.location = location
		

@slots_api.route("/api/slots/add", methods=['POST'])
def add_slot():
    id = request.json['_id']
    location = request.json['location']
    slot = Slot(id, location)
    data = {
        '_id': slot._id,
		'patin': slot.patin,
		'location': slot.location
	}
    try:
        result = slots.insert(data)
        return jsonify({
			'ok': True, 
			'message': 'Slot created'}), 200
    except:
        return jsonify({
			'ok': False, 
			'message': 'Error adding slot'}), 400

@slots_api.route("/api/slots/list", methods=['GET'])
def list_slots():
    try:
        result = slots.find()
        return dumps(result), 200
    except:
        return jsonify({
			'ok': False, 
			'message': 'Internal Error'}), 500

@slots_api.route("/api/slots/dejar_patin", methods=['POST'])
def dejar_patin_en_slot():
    slot = request.json['slot']
    patin = request.json['patin']
    patin_exist = patines.find_one({
		'_id': patin
	})
    if patin_exist != None:
        slot_exist = slots.find_one({
			'_id': slot
		})
        if slot_exist == None:
            return jsonify({
			    'ok': False,
			    'message': 'Id of slot provided doesnt exist'
		    }), 400	
        else:
            if slot_exist['patin'] != 0:
                return jsonify({
					'ok': False,
					'message': 'Slot already has a patin in it'
				}), 400
            else:
                slots.update_one(
					{ '_id': slot },
					{ '$set': {
						"patin": patin
					}}
				)
                rents.update(
					{'id_patin': patin, 'status': True}, 
					{'$set': 
					{
						'status': False
					}}, upsert=False, multi=True
				)
                return jsonify({
					'ok': True,
					'message': 'Slot updated'
				}), 200
    else:
        return jsonify({
			'ok': False,
			'message': 'Id of patin provided doesnt exist'
		}), 400

@slots_api.route("/api/slots/list/location", methods=['GET'])
def list_slots_by_location():
    print(request.args.get)
    location = request.args['location']
    try:
        result = slots.find({
			'location': location
		})
        return dumps(result)
    except:
        return jsonify({
			'ok': False,
			'message': 'Internal Error'
		}), 500
