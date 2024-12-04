# Author: This microservice was written for the Resourceful Chef Program by Courtney Sanders

from flask import Flask, request, jsonify

app = Flask(__name__)

def high_low_sort(item_dict):
    """
    Sorts a list of dictionaries from high to low ratings. 
    Receives the list of dictionaries as a parameter. Returns a list of dictionaries as a JSON object.
    """
    return jsonify(sorted(item_dict, reverse=True, key=lambda item: int(item["rating"])))
def low_high_sort(item_dict):
    """
    Sorts a list of dictionaries from low to high ratings.
    Receives a list of dictionaries as a parameter. Returns a list of dictionaries as a JSON object.
    """
    return jsonify(sorted(item_dict, key=lambda item: int(item['rating'])))

def name_asc_sort(item_dict):
    """
    Sorts a list of dictionaries by name in ascending order.
    Receives a list of dictionaries as a parameter. Returns a list of dictionaries as a JSON object.
    """
    return jsonify(sorted(item_dict, key=lambda item: item['recipe']))

def name_des_sort(item_dict):
    """
    Sorts a list of dictionaries by name in descending order.
    Receives a list of dictionaries as a parameter. Returns a list of dictionaries as a JSON object. 
    """
    return jsonify(sorted(item_dict, reverse=True, key=lambda item: item['recipe']))


@app.route('/sort', methods=['POST'])
def sort():
    """
    Checks the query parameter in the URL to determine sort method, then calls the appropriate function to sort.
    Receives no parameters. Returns JSON object with a list of dictionaries containing a name as the key and rating as the value, sorted
    per the query parameter.
    """
    data = request.get_json()
    sort_method = request.args.get('sort_method')
    if sort_method == 'high-low':
        return high_low_sort(data)
    elif sort_method == 'low-high':
        return low_high_sort(data)
    elif sort_method =='name-ascending':
        return name_asc_sort(data)
    elif sort_method == 'name-descending':
        return name_des_sort(data)
    else:
        return 'Error: Invalid sort method.'
        
if __name__ == '__main__':
    app.run(port=5002, debug=True)
        
