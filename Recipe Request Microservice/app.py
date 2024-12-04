from flask import Flask, request, jsonify

app = Flask(__name__)

def find_recipe(recipes, pantry):
    resourceful_score = 0 
    most_resourceful_score = 0
    most_resourceful = []
    for recipe in recipes:
        resourceful_score = 0
        ingredients = recipe['Ingredients']
        for ingredient in ingredients:
            for pantry_item in pantry:
                if ingredient == pantry_item['Name']:
                    resourceful_score += 1
        if most_resourceful_score < resourceful_score:
            most_resourceful_score = resourceful_score
            most_resourceful = []
            most_resourceful.append(recipe['Name'])
        elif most_resourceful_score == resourceful_score:
            most_resourceful.append(recipe['Name'])
    return jsonify(most_resourceful)

@app.route('/request_recipe', methods=['POST'])
def request_recipe():
    data = request.get_json()
    recipes = data.get('recipes')
    pantry = data.get('pantry')
    return find_recipe(recipes, pantry)


if __name__ == '__main__':
    app.run(port=5003, debug=True)