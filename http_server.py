from flask import Flask, request, jsonify

import getters

app = Flask(__name__)

def is_valid_uuid(uuid: str):
    try:
        uuid_obj = uuid.UUID(uuid)
        return True
    except ValueError:
        return False

@app.route('/get_plot_size', methods=['GET'])
def get_plot_size():
    if request.method != 'GET':
        return jsonify({'error': 'invalid request method'})
    
    player_uuid = request.args.get('player_uuid')

    if player_uuid is None:
        return jsonify({'error': 'player_uuid not provided'})
    elif not is_valid_uuid(player_uuid):
        return jsonify({'error': 'player_uuid is not valid'})
    
    return jsonify({'plot_size': getters.get_plot_size(player_uuid)})

@app.route('/get_money', methods=['GET'])
def get_money():
    if request.method != 'GET':
        return jsonify({'error': 'invalid request method'})
    
    player_uuid = request.args.get('player_uuid')

    if player_uuid is None:
        return jsonify({'error': 'player_uuid not provided'})
    elif not is_valid_uuid(player_uuid):
        return jsonify({'error': 'player_uuid is not valid'})
    
    return jsonify({'money': getters.get_money(player_uuid)})

@app.route('/get_seeds', methods=['GET'])
def get_money():
    if request.method != 'GET':
        return jsonify({'error': 'invalid request method'})
    
    player_uuid = request.args.get('player_uuid')

    if player_uuid is None:
        return jsonify({'error': 'player_uuid not provided'})
    elif not is_valid_uuid(player_uuid):
        return jsonify({'error': 'player_uuid is not valid'})
    
    return jsonify({'seeds': getters.get_seeds(player_uuid)})

@app.route('/get_products', methods=['GET'])
def get_products():
    if request.method != 'GET':
        return jsonify({'error': 'invalid request method'})
    
    player_uuid = request.args.get('player_uuid')
    if player_uuid is None:
        return jsonify({'error': 'player_uuid not provided'})
    elif not is_valid_uuid(player_uuid):
        return jsonify({'error': 'player_uuid is not valid'})
    
    return jsonify({'products': getters.get_products(player_uuid)})

@app.route('/get_product_value', methods=['GET'])
def get_product_value():
    if request.method != 'GET':
        return jsonify({'error': 'invalid request method'})
    
    player_uuid = request.args.get('player_uuid')

    if player_uuid is None:
        return jsonify({'error': 'player_uuid not provided'})
    elif not is_valid_uuid(player_uuid):
        return jsonify({'error': 'player_uuid is not valid'})
    
    return jsonify({'product_value': getters.get_product_value(player_uuid)})

@app.route('/get_net_worth', methods=['GET'])
def get_net_worth():
    if request.method != 'GET':
        return jsonify({'error': 'invalid request method'})
    
    player_uuid = request.args.get('player_uuid')

    if player_uuid is None:
        return jsonify({'error': 'player_uuid not provided'})
    elif not is_valid_uuid(player_uuid):
        return jsonify({'error': 'player_uuid is not valid'})
    
    return jsonify({'net_worth': getters.get_net_worth(player_uuid)})

if __name__ == '__main__':
    app.run()