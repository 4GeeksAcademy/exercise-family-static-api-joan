"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
jackson_family = FamilyStructure("Jackson")

Michael = {
    "first_name": "Michael",
    "last_name": jackson_family.last_name,
    "age": 30,
    "lucky_numbers": [5,15]
}

Janet = {
    "first_name": "Janet",
    "last_name": jackson_family.last_name,
    "age": 28,
    "lucky_numbers": [3,23]
}

Tito = {
    "first_name": "Tito",
    "last_name": jackson_family.last_name,
    "age": 45,
    "lucky_numbers": [4,54]
}

jackson_family.add_member(Michael)
jackson_family.add_member(Janet)
jackson_family.add_member(Tito)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_one_member(id):
    member = jackson_family.get_member(id)
    return jsonify(member), 200

@app.route('/member', methods=['POST'])
def create_member():
    member = request.json
    jackson_family.add_member(member)
    if member is not None:
        return {
            "member": member,
            "message": "Member created successfully"
        }, 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_one_member(id):
    member = jackson_family.get_member(id)
    if member:
        jackson_family.delete_member(id)
        return {
            "member": member,
            "message": "Member deleted successfully"
            }, 200
    else:
        return jsonify({
            "error": "Member not found"
            }), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
