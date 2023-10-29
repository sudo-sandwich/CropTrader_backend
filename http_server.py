from flask import Flask, request, jsonify

import getters

app = Flask(__name__)

@app.route('/get_plot_size', methods=['GET'])
def get_plot_size():
    if request.method != 'GET':
        return jsonify({'error': 'invalid request method'})
    
    player_uuid = request.args.get('player_uuid')

    if player_uuid is None:
        return jsonify({'error': 'player_uuid not provided'})
    
    return jsonify({'plot_size': getters.get_plot_size(player_uuid)})

if __name__ == '__main__':
    app.run()