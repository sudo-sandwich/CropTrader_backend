from flask import Flask, request, jsonify
import uuid

import farmer_actions
import getters
import player_exceptions

app = Flask(__name__)

def is_valid_uuid(uuid_str: str):
    try:
        uuid_obj = uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False

@app.route('/get_username', methods=['GET'])
def flask_get_username():
    if request.method != 'GET':
        return jsonify({'error': 'Invalid request method'})

    player_uuid = request.args.get('player_uuid')

    if player_uuid is None:
        return jsonify({'error': 'player_uuid not provided'})
    elif not is_valid_uuid(player_uuid):
        return jsonify({'error': 'player_uuid is not valid'})

    try:
        username = getters.get_username(player_uuid)
    except getters.UUIDNotFoundException as e:
        return jsonify({'error': str(e)})

    return jsonify({'username': username})

@app.route('/get_plot_size', methods=['GET'])
def flask_get_plot_size():
    if request.method != 'GET':
        return jsonify({'error': 'Invalid request method'})
    
    player_uuid = request.args.get('player_uuid')

    if player_uuid is None:
        return jsonify({'error': 'player_uuid not provided'})
    elif not is_valid_uuid(player_uuid):
        return jsonify({'error': 'player_uuid is not valid'})
    
    try:
        plot_size = getters.get_plot_size(player_uuid)
    except getters.UUIDNotFoundException as e:
        return jsonify({'error': str(e)})
    
    return jsonify({'plot_size': plot_size})

@app.route('/get_plots', methods=['GET'])
def flask_get_plots():
    if request.method != 'GET':
        return jsonify({'error': 'Invalid request method'})
    
    player_uuid = request.args.get('player_uuid')

    if player_uuid is None:
        return jsonify({'error': 'player_uuid not provided'})
    elif not is_valid_uuid(player_uuid):
        return jsonify({'error': 'player_uuid is not valid'})
    
    try:
        plots = getters.get_plots(player_uuid)
    except getters.UUIDNotFoundException as e:
        return jsonify({'error': str(e)})
    
    return jsonify({'plots': plots})

@app.route('/get_money', methods=['GET'])
def flask_get_money():
    if request.method != 'GET':
        return jsonify({'error': 'Invalid request method'})
    
    player_uuid = request.args.get('player_uuid')

    if player_uuid is None:
        return jsonify({'error': 'player_uuid not provided'})
    elif not is_valid_uuid(player_uuid):
        return jsonify({'error': 'player_uuid is not valid'})
    
    try:
        money = getters.get_money(player_uuid)
    except getters.UUIDNotFoundException as e:
        return jsonify({'error': str(e)})
    
    return jsonify({'money': money})

@app.route('/get_seeds', methods=['GET'])
def flask_get_seeds():
    if request.method != 'GET':
        return jsonify({'error': 'Invalid request method'})
    
    player_uuid = request.args.get('player_uuid')

    if player_uuid is None:
        return jsonify({'error': 'player_uuid not provided'})
    elif not is_valid_uuid(player_uuid):
        return jsonify({'error': 'player_uuid is not valid'})
    
    try:
        seeds = getters.get_seeds(player_uuid)
    except getters.UUIDNotFoundException as e:
        return jsonify({'error': str(e)})
    
    return jsonify({'seeds': seeds})

@app.route('/get_products', methods=['GET'])
def flask_get_products():
    if request.method != 'GET':
        return jsonify({'error': 'Invalid request method'})
    
    player_uuid = request.args.get('player_uuid')

    if player_uuid is None:
        return jsonify({'error': 'player_uuid not provided'})
    elif not is_valid_uuid(player_uuid):
        return jsonify({'error': 'player_uuid is not valid'})
    
    try:
        products = getters.get_products(player_uuid)
    except getters.UUIDNotFoundException as e:
        return jsonify({'error': str(e)})
    
    return jsonify({'products': products})

@app.route('/get_product_value', methods=['GET'])
def flask_get_product_value():
    if request.method != 'GET':
        return jsonify({'error': 'Invalid request method'})
    
    player_uuid = request.args.get('player_uuid')

    if player_uuid is None:
        return jsonify({'error': 'player_uuid not provided'})
    elif not is_valid_uuid(player_uuid):
        return jsonify({'error': 'player_uuid is not valid'})
    
    try:
        product_value = getters.get_product_value(player_uuid)
    except getters.UUIDNotFoundException as e:
        return jsonify({'error': str(e)})
    
    return jsonify({'product_value': product_value})

@app.route('/get_net_worth', methods=['GET'])
def flask_get_net_worth():
    if request.method != 'GET':
        return jsonify({'error': 'Invalid request method'})
    
    player_uuid = request.args.get('player_uuid')

    if player_uuid is None:
        return jsonify({'error': 'player_uuid not provided'})
    elif not is_valid_uuid(player_uuid):
        return jsonify({'error': 'player_uuid is not valid'})
    
    try:
        net_worth = getters.get_net_worth(player_uuid)
    except getters.UUIDNotFoundException as e:
        return jsonify({'error': str(e)})
    
    return jsonify({'net_worth': net_worth})

@app.route('/create_farmer', methods=['POST'])
def flask_create_farmer():
    if request.method != 'POST':
        return jsonify({'error': 'Invalid request method'})
    
    username = request.form.get('username')
    password = request.form.get('password')

    if username is None:
        return jsonify({'error': 'username not provided'})
    elif password is None:
        return jsonify({'error': 'password not provided'})
    
    try:
        farmer_actions.create_farmer(username, password)
    except farmer_actions.UsernameNotFoundException:
        return jsonify({'success': False, 'error': 'username already exists'})
    
    return jsonify({'success': True})

@app.route('/plant', methods=['POST'])
def flask_plant():
    if request.method != 'POST':
        return jsonify({'error': 'Invalid request method'})
    
    player_uuid = request.form.get('player_uuid')
    plot_id = request.form.get('plot_id')
    num_seeds = request.form.get('num_seeds')
    seed_id = request.form.get('seed_id')

    if player_uuid is None:
        return jsonify({'success': False, 'error': 'player_uuid not provided'})
    elif not is_valid_uuid(player_uuid):
        return jsonify({'success': False, 'error': 'player_uuid is not valid'})
    elif plot_id is None:
        return jsonify({'success': False, 'error': 'plot_id not provided'})
    elif num_seeds is None:
        return jsonify({'success': False, 'error': 'num_seeds not provided'})
    elif seed_id is None:
        return jsonify({'success': False, 'error': 'seed_id not provided'})
    
    try:
        farmer_actions.plant(player_uuid, plot_id, num_seeds, seed_id)
    except (player_exceptions.PlayerException, farmer_actions.UUIDNotFoundException) as e:
        return jsonify({'success': False, 'error': str(e)})
    
    return jsonify({'success': True})

@app.route('/harvest', methods=['POST'])
def flask_harvest():
    if request.method != 'POST':
        return jsonify({'error': 'Invalid request method'})
    
    player_uuid = request.form.get('player_uuid')
    plot_id = request.form.get('plot_id')

    if player_uuid is None:
        return jsonify({'success': False, 'error': 'player_uuid not provided'})
    elif not is_valid_uuid(player_uuid):
        return jsonify({'success': False, 'error': 'player_uuid is not valid'})
    elif plot_id is None:
        return jsonify({'success': False, 'error': 'plot_id not provided'})
    
    try:
        farmer_actions.harvest(player_uuid, plot_id)
    except (player_exceptions.PlayerException, farmer_actions.UUIDNotFoundException) as e:
        return jsonify({'success': False, 'error': str(e)})
    
    return jsonify({'success': True})

@app.route('/sell', methods=['POST'])
def flask_sell():
    if request.method != 'POST':
        return jsonify({'error': 'Invalid request method'})
    
    player_uuid = request.form.get('player_uuid')
    product_id = request.form.get('product_id')

    if player_uuid is None:
        return jsonify({'success': False, 'error': 'player_uuid not provided'})
    elif not is_valid_uuid(player_uuid):
        return jsonify({'success': False, 'error': 'player_uuid is not valid'})
    elif product_id is None:
        return jsonify({'success': False, 'error': 'product_id not provided'})
    
    try:
        farmer_actions.sell(player_uuid, product_id)
    except (player_exceptions.PlayerException, farmer_actions.UUIDNotFoundException) as e:
        return jsonify({'success': False, 'error': str(e)})
    
    return jsonify({'success': True})

@app.route('/buy_mystery_seed', methods=['POST'])
def flask_buy_mystery_seed():
    if request.method != 'POST':
        return jsonify({'error': 'Invalid request method'})
    
    player_uuid = request.form.get('player_uuid')

    if player_uuid is None:
        return jsonify({'success': False, 'error': 'player_uuid not provided'})
    elif not is_valid_uuid(player_uuid):
        return jsonify({'success': False, 'error': 'player_uuid is not valid'})
    
    try:
        farmer_actions.buy_mystery_seed(player_uuid)
    except (player_exceptions.PlayerException, farmer_actions.UUIDNotFoundException) as e:
        return jsonify({'success': False, 'error': str(e)})
    
    return jsonify({'success': True})

@app.route('/upgrade_plot', methods=['POST'])
def flask_upgrade_plot():
    if request.method != 'POST':
        return jsonify({'error': 'Invalid request method'})
    
    player_uuid = request.form.get('player_uuid')

    if player_uuid is None:
        return jsonify({'success': False, 'error': 'player_uuid not provided'})
    elif not is_valid_uuid(player_uuid):
        return jsonify({'success': False, 'error': 'player_uuid is not valid'})
    
    try:
        farmer_actions.upgrade_plot(player_uuid)
    except (player_exceptions.PlayerException, farmer_actions.UUIDNotFoundException) as e:
        return jsonify({'success': False, 'error': str(e)})
    
    return jsonify({'success': True})

@app.route('/trade', methods=['POST'])
def flask_trade():
    if request.method != 'POST':
        return jsonify({'error': 'Invalid request method'})
    
    player1_uuid = request.form.get('player1_uuid')
    player2_uuid = request.form.get('player2_uuid')

    if player1_uuid is None:
        return jsonify({'success': False, 'error': 'player1_uuid not provided'})
    elif not is_valid_uuid(player1_uuid):
        return jsonify({'success': False, 'error': 'player1_uuid is not valid'})
    elif player2_uuid is None:
        return jsonify({'success': False, 'error': 'player2_uuid not provided'})
    elif not is_valid_uuid(player2_uuid):
        return jsonify({'success': False, 'error': 'player2_uuid is not valid'})
    
    try:
        farmer_actions.trade(player1_uuid, player2_uuid)
    except (player_exceptions.PlayerException, farmer_actions.UUIDNotFoundException) as e:
        return jsonify({'success': False, 'error': str(e)})
    
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run('ssl_context=adhoc')