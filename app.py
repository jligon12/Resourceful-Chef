# import flask
# render_template finds the app by default in the templates folder
# uses the name of the template instead of the entire path to the template
from flask import Flask, render_template, request, redirect
import pymongo

client = pymongo.MongoClient("mongodb+srv://ligonj:<password>@resourceful-chef.ib2ej.mongodb.net/")
db = client["recipe-library"]
recipe_collection = db["recipes"]
pantry_collection = db["pantry"]


# reference file
app = Flask(__name__)

# create index route for browsing to the url
# in flask use the @ route decorator - route means function is bound with URL
# pass in the url string of your route
@app.route('/')
# define the function for the route
def index():
    #pulls the name of the file index.html
    return render_template('index.html')

# create recipe library route for browsing to the url
# in flask use the @ route decorator - route means function is bound with URL
# pass in the url string of your route
@app.route('/full_recipe_library')
# define the function for the route
def full_recipe_library():
    recipes=[]
    ingredients=[]
    for recipe in recipe_collection.find({}, {'_id':0, 'Name':1, 'Ingredients':1}):
        recipes.append(recipe['Name'])
        ingredients.append(recipe['Ingredients'])
    return render_template('full_recipe_library.html', recipes=recipes, ingredients=ingredients)

@app.route('/recipe_library')
# define the function for the route
def recipe_library():
    recipes=[]
    for recipe in recipe_collection.find({}, {'_id':0, 'Name':1}):
        recipes.append(recipe['Name'])
    return render_template('recipe_library.html', recipes=recipes)


@app.route('/pantry')
def pantry():
    items=[]
    for item in pantry_collection.find({}, {'_id':0, 'Name':1}):
        items.append(item['Name'])
    return render_template('pantry.html', items=items)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        added_item = request.form['additem']
        pantry_collection.insert_one({'Name':added_item})
        return redirect('/add_item')
        #return 'item added'
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

# @app.route('/remove_item', methods=['POST', 'DELETE'])
# def remove_item():
#     if request.method == 'DELETE':
#         removed_item = request.form['removeitem']
#         pantry_collection.delete_many({'Name':removed_item})
#         return 'item removed'
#     else:
#         return render_template('remove_item.html')

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



#
if __name__ == "__main__":
    app.run(debug=True)