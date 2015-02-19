from flask import Flask, jsonify, request, abort, make_response, render_template
from datetime import datetime, timedelta
import uuid

# Flask light-weight web server.
server = Flask(__name__)

# In-memory Databases - Dynamic Dictionaries
orders = dict()
products = ['FiOS','SONET', 'VOD']
bad_states = []


##########################
##### REST SERVICES ######
##########################

# Helper function for generating 404 errors
@server.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# Returns the main form. Utilizes the oep.html template
@server.route('/', methods=['GET'])
def get_root():
    return render_template('oep.html', entries=products)


# Get a specific order by calling /ovs/orders/<order_id>
@server.route('/ovs/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    # if the id is on our 'orders' database return it, if not, return 404
    if orders.has_key(str(order_id)):
        return jsonify({'order': orders.get(str(order_id))})
    else:
        abort(404)


# Get all orders by calling /ovs/orders
@server.route('/ovs/orders', methods=['GET'])
def get_all_order():
    # return everything in out 'orders' database
    return jsonify({'orders': orders.values()})



# Order Validation Service
@server.route('/ovs/orders', methods=['POST'])
def post_order():

    # Get the Json order from the request
    if (request.headers['Content-Type'] == 'application/json'): # if already json, parse it as such
        new_order = request.json
    elif (request.headers['Content-Type'] == 'application/x-www-form-urlencoded'): # if post params, parse into json
        new_order = dict()
        new_order['name'] = request.form['name']
        new_order['address'] = request.form['address']
        new_order['city'] = request.form['city']
        new_order['state'] = request.form['state']
        new_order['zipcode'] = request.form['zipcode']
        new_order['dueDate'] = request.form['dueDate']


    # call the order validation function
    valid,error_msg = order_field_validation(new_order)

    # If not valid, return status 400 (bad request) with a json body containing the error message.
    if not valid:
        return jsonify({'error': error_msg}), 400

    # if it is valid, generate ids and store in internal database...
    order_id = uuid.uuid4() # Generate an ID for this order.
    new_order['id'] = str(order_id.hex) # Add the ID to the order json object
    orders[str(order_id.hex)] = new_order # Add the order to the database


    # Return the order created with generated ID
    return jsonify(new_order)




##########################
#### HELPER FUNCTIONS ####
##########################

# Order Validation, returns a tuple, (boolean,string)
# This is doing sequential validation for now...
def order_field_validation(order={}):

    # Check if the request is empty
    valid,error = validate_empty_order(order=order)
    if not valid:
        return valid, error

    # If all validation passes, return true.
    return True, ''


# Helper: Empty request validation.
def validate_empty_order(order={}):
    if not order:
        return False, 'order is empty'
    else:
        return True, ''


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=80, debug=True)