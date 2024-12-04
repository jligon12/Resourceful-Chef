from flask import Flask, jsonify, request
import pymongo
import json
from bson import json_util

#MongoDB connection 
connection_url = 'mongodb+srv://jligon:journal@recipejournal.zrbtp.mongodb.net/'
app = Flask(__name__)
client = pymongo.MongoClient(connection_url)

#Database
db = client.get_database("RecipeJournal")
#Collection
notes = db.notes
dates = db.dates

# Date routes
@app.route('/addDate', methods=['POST'])
def addDate():
    dateData = request.get_json()
    recipe = dateData.get('recipe')
    date = dateData.get('date')
    recipe_date = {
        'recipe': recipe,
        'date': date
    }
    dates.insert_one(recipe_date)
    return jsonify({'message': f'Date added successfully.'}), 201

@app.route('/getDates', methods = ['GET'])
def getDates():
    #data = request.get_json()
    recipe_dates = dates.find({}, {'_id':0, 'recipe':1, 'date':1})
    documents = list(recipe_dates)
    json_string = json.dumps(documents, default=json_util.default)
    return json_string, 200


# Note routes
@app.route('/addNote', methods=['POST'])
def addNote():
    noteData = request.get_json()
    recipe = noteData.get('recipe')
    note = noteData.get('note')
    recipe_note = {
        'recipe': recipe, 
        'note': note
    }
    notes.insert_one(recipe_note)
    return jsonify({'message': f'Note added successfully.'}), 201

@app.route('/getNotes', methods = ['GET'])
def getNotes():
    #data = request.get_json()
    recipe_notes = notes.find({},{'_id':0, 'recipe':1, 'note':1})
    documents = list(recipe_notes)
    json_string = json.dumps(documents, default=json_util.default)
    return json_string, 200

if __name__ == '__main__':
    app.run(port=5004, debug=True)