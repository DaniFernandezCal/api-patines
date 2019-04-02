from flask import Flask, request, jsonify, Blueprint
from bson.json_util import dumps

from mongo_utils import rents, slots, patines


patines_api = Blueprint('patines', __name__)

class Patin():
	_id = 0

	def __init__(self, id):
		self._id = id

class Rent():
    user_name = ""
    id_patin = ""
    status = True

    def __init__(self, user_name, id_patin, status):
        self.user_name = user_name
        self.id_patin = id_patin
        self.status = status


@patines_api.route("/api/patines/add", methods=['POST'])
def add_patin():
    id = request.json['_id']
    patin = Patin(id)
    data = {
        '_id': patin._id,
    }
    patin_exist = patines.find_one({
		'_id': id
	})
    if patin_exist == None:
        patines.insert(data)
        return jsonify({
			'ok': True,
			'message': 'Patin added to db'
		}), 200
    else:
        return jsonify({
			'ok': False,
			'message': 'Patin with id provided already exist'
		}), 400

@patines_api.route("/api/patines/list", methods=['GET'])
def list_patines():
    try:
        result = patines.find()
        return dumps(result), 200
    except:
        return "", 400

@patines_api.route("/api/patines/rent",methods=['POST'])
def do_rent():
    user = request.json['user']
    patin = request.json['patin']
    slot = request.json['slot']

    rent = Rent(user,patin,True)
    try:
        rents.insert_one({
            'user_name':rent.user_name,
            'id_patin':rent.id_patin,
            'status':True
        })
        slots.update(
		    {'_id':slot},
		    {'$set':
		    {'patin': 0}},upsert=False,multi=True)
        
        return jsonify({
				'ok': True,
				'message': 'Slot updated'
            }), 200

    except:
        return jsonify({
			'ok': False,
			'message': 'Error'
        }), 400

@patines_api.route("/api/patines/rentings", methods=['GET'])
def list_rents():
    try:
        result = rents.find()
        return dumps(result), 200
    except:
        return jsonify({
            'ok': False,
			'message': 'Internal Error'}), 500