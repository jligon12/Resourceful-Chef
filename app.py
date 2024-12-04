from flask import Flask, render_template, request, redirect, jsonify
import pymongo
import requests
import json
from bson import json_util

client = pymongo.MongoClient('mongodb+srv://ligonj:<password>@resourceful-chef.ib2ej.mongodb.net/')
db = client["recipe-library"]
recipe_collection = db["recipes"]
pantry_collection = db["pantry"]
rating_collection = db["ratings"]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        entered_login = {'username': username, 'password': password}
        response = requests.post('http://127.0.0.1:5001/login', json=entered_login)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return response.json()
    if request.method == 'GET':
            return render_template('login.html')

@app.route('/createUser', methods=['GET', 'POST'])
def createUser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        entered_login = {'username': username, 'password': password}
        response = requests.post('http://127.0.0.1:5001/createUserLogin', json=entered_login)
        if response.status_code == 201:
            return response.json()
        elif response.status_code == 401:
            return response.json()
    if request.method == 'GET':
            return render_template('createUser.html')

@app.route('/full_recipe_library')
def full_recipe_library():
    full_recipes = recipe_collection.find({}, {'_id':0, 'Name':1, 'Ingredients':1})
    recipes = list(full_recipes)
    return render_template('full_recipe_library.html', recipes=recipes)

@app.route('/recipe_library', methods=['GET', 'POST'])
def recipe_library():
    if request.method == 'GET':
        recipe_names=[]
        for recipe in recipe_collection.find({}, {'_id':0, 'Name':1}):
            recipe_names.append(recipe['Name'])
        return render_template('recipe_library.html', recipe_names=recipe_names)
    if request.method == 'POST':
        recipe_names=[]
        for recipe in recipe_collection.find({}, {'_id':0, 'Name':1}):
            recipe_names.append(recipe['Name'])
        recipes = recipe_collection.find({}, {'_id':0, 'Name':1, 'Ingredients':1})
        pantry = pantry_collection.find({}, {'_id':0, 'Name':1})
        recipes = list(recipes)
        for recipe in recipes:
            ingredients = recipe['Ingredients']
            list_ingredients = ingredients.split(",")
            recipe['Ingredients'] = list_ingredients
        pantry = list(pantry)
        data = {'recipes': recipes, 'pantry': pantry}
        response = requests.post('http://127.0.0.1:5003/request_recipe', json=data)
        resourceful_recipe = response.json()
        resourceful_recipe = ", ".join(resourceful_recipe) 
        return render_template('recipe_library.html', recipe_names=recipe_names, resourceful_recipe=resourceful_recipe)

@app.route('/pantry')
def pantry():
    items=[]
    for item in pantry_collection.find({}, {'_id':0, 'Name':1}):
        items.append(item['Name'])
    return render_template('pantry.html', items=items)

@app.route('/recipe_journal')
def recipe_journal():
    return render_template('recipe_journal.html')

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        added_item = request.form['additem']
        pantry_collection.insert_one({'Name':added_item})
        return redirect('/add_item')
    else:
        return render_template('add_item.html')

@app.route('/remove_item', methods=['GET', 'POST'])
def remove_item():
    if request.method == 'POST':
        removed_item = request.form['removeitem']
        pantry_collection.delete_many({'Name':removed_item})
        return redirect('/remove_item')
    else:
        return render_template('remove_item.html')

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        recipe_name = request.form['rname']
        ingredients = request.form['ingr']
        recipe_collection.insert_one({'Name': recipe_name, 'Ingredients': ingredients})
        return redirect('/add_recipe')
    else:
        return render_template('add_recipe.html')
    
@app.route('/remove_recipe', methods=['GET', 'POST'])
def remove_recipe():
    if request.method == 'POST':
        remove_recipe_name = request.form['removername']
        recipe_collection.delete_one({'Name': remove_recipe_name})
        return redirect('/remove_recipe')
    else:
        return render_template('remove_recipe.html')

@app.route('/recipe_rating', methods=['GET', 'POST'])
def recipe_rating():
    if request.method == 'POST':
        rated_recipe = request.form['rname']
        rating = request.form['rating']
        rating_collection.insert_one({'recipe':rated_recipe, 'rating': rating})
        return redirect('/recipe_rating')
    else:
        return render_template('recipe_rating.html')

@app.route('/recipe_ratings', methods=['GET', 'POST'] )
def recipe_ratings():
    if request.method == 'GET':
        recipe_ratings = rating_collection.find({}, {'_id':0, 'recipe':1, 'rating':1})
        recipe_ratings_list = list(recipe_ratings)
        return render_template('recipe_ratings.html', recipe_ratings_list=recipe_ratings_list)
    
    if request.method == 'POST':
        sortby = request.form['sortby']
        params = {'sort_method': sortby}
        recipe_ratings = rating_collection.find({}, {'_id':0, 'recipe':1, 'rating':1})
        documents = list(recipe_ratings)
        response = requests.post('http://127.0.0.1:5002/sort', params=params, json=documents)
        sorted_data = response.json()
        recipe_ratings_list=list(sorted_data)
        return render_template('recipe_ratings.html', recipe_ratings_list=recipe_ratings_list)

@app.route('/recipe_dates', methods=['GET', 'POST'] )   
def recipe_dates():
    if request.method == 'GET':
        response = requests.get('http://127.0.0.1:5004/getDates')
        if response.status_code == 200:
            recipe_dates=response.json()
            recipe_dates = list(recipe_dates)
            return render_template('recipe_dates.html', recipe_dates=recipe_dates)
        else:
             return render_template('recipe_dates.html')
    if request.method == 'POST':
        recipe = request.form['rname']
        date = request.form['date']
        data = {'recipe': recipe, 'date': date}
        response = requests.post('http://127.0.0.1:5004/addDate', json=data)
        if response.status_code == 201:
            return response.json()

@app.route('/recipe_notes', methods=['GET', 'POST'] )   
def recipe_notes():
    if request.method == 'GET':
        response = requests.get('http://127.0.0.1:5004/getNotes')
        if response.status_code == 200:
            recipe_notes=response.json()
            recipe_notes = list(recipe_notes)
            return render_template('recipe_notes.html', recipe_notes=recipe_notes)
        else:
             return render_template('recipe_notes.html')
    if request.method == 'POST':
        recipe = request.form['rname']
        note = request.form['note']
        data = {'recipe': recipe, 'note': note}
        response = requests.post('http://127.0.0.1:5004/addNote', json=data)
        if response.status_code == 201:
            return response.json()

if __name__ == "__main__":
    app.run(debug=True)