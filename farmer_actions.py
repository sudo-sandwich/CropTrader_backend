from datetime import datetime, timedelta, timezone

import constants
import player_exceptions
import sb_client

supabase = sb_client.create_supabase_client()

# births a new farmer into this world. in other words, creates a new player account.
def create_farmer():
    ''''''

# plants any number of seeds to an empty plot.
def plant(player_uuid: str, plot_id: int, num_seeds: int, seed_id: int) -> {}:
    response = supabase.table('player_data').select('plot_size', 'seeds', f'plot_{plot_id}_num', f'plot_{plot_id}_end').eq('id', player_uuid).execute()

    if num_seeds > response.data[0]['plot_size']:
        raise player_exceptions.PlotNotLargeEnoughException(f'Plot is not large enough. Max size: {response.data[0]['plot_size']}')
    elif response.data[0]['seeds'][seed_id] < num_seeds:
        raise player_exceptions.NotEnoughSeedsException(f"Player does not have enough seeds. id: {seed_id}")
    elif response.data[0][f'plot_{plot_id}_num'] != 0:
        raise player_exceptions.PlotNotEmptyException(f'Plot {plot_id} is not empty.')
    
    new_seed_count = response.data[0]['seeds']
    new_seed_count[seed_id] -= num_seeds
    end_time = datetime.now(timezone.utc) + timedelta(seconds=constants.SEED_CONSTANTS[seed_id]['grow_time_sec'])
    end_time_iso = end_time.isoformat()
    response = supabase.table('player_data').update({
        'seeds': new_seed_count,
        f'plot_{plot_id}_type': seed_id, 
        f'plot_{plot_id}_num': num_seeds, 
        f'plot_{plot_id}_end': end_time_iso
        }).eq('id', player_uuid).execute()

# harvests a complete plot and adds products/seeds to a player's inventory.
def harvest(player_uuid: str, plot_id: int) -> {}:
    response = supabase.table('player_data').select('seeds', 'products', f'plot_{plot_id}_type', f'plot_{plot_id}_num', f'plot_{plot_id}_end').execute()

    if response.data[0][f'plot_{plot_id}_num'] == 0:
        raise player_exceptions.PlotNotEmptyException(f'Plot {plot_id} is empty.')
    elif response.data[0][f'plot_{plot_id}_end'] > datetime.now(timezone.utc).isoformat():
        raise player_exceptions.PlotNotReadyException(f'Plot {plot_id} is not ready.')

    new_seed_count = response.data[0]['seeds']
    # TODO: add an actual multiplier here instead of just x2.
    new_seed_count[response.data[0][f'plot_{plot_id}_type']] += response.data[0][f'plot_{plot_id}_num'] * 2
    new_product_count = response.data[0]['products']
    new_product_count[response.data[0][f'plot_{plot_id}_type']] += response.data[0][f'plot_{plot_id}_num']

    response = supabase.table('player_data').update({
        'seeds': new_seed_count,
        'products': new_product_count,
        f'plot_{plot_id}_num': 0
        }).eq('id', player_uuid).execute()

# sells a single product.
def sell(player_uuid: str, product_id: int):
    response = supabase.table('player_data').select('products', 'product_value', 'money').eq('id', player_uuid).execute()

    if response.data[0]['products'][product_id] == 0:
        raise player_exceptions.NotEnoughProductsException(f'Player does not have enough products. id: {product_id}')

    new_product_count = response.data[0]['products']
    new_product_count[product_id] -= 1
    new_money_count = response.data[0]['money'] + constants.PRODUCT_CONSTANTS[product_id]['value'] * response.data[0]['product_value'][product_id]
    new_product_value = response.data[0]['product_value']
    for i in range(len(response.data[0]['product_value'])):
        if i == product_id:
            new_product_value[i] -= 0.05
        else:
            new_product_value[i] += 0.01
        new_product_value[i] = max(0, min(1, new_product_value[i]))

    response = supabase.table('player_data').update({
        'products': new_product_count,
        'product_value': new_product_value,
        'money': new_money_count
        }).eq('id', player_uuid).execute()

# buys a single mystery seed.
def buy_mystery_seed(player_uuid: str):
    response = supabase.table('player_data').select('money', 'seeds').eq('id', player_uuid).execute()

    if response.data[0]['money'] < constants.MYSTERY_SEED_COST:
        raise player_exceptions.NotEnoughMoneyException(f'Player does not have enough money. Cost: {constants.MYSTERY_SEED_COST}')

# upgrades all plots to a larger size.
def upgrade_plot(player_uuid: str):
    ''''''

# trades seeds with another player.
def trade(player1_uuid: str, player2_uuid: str, seeds1: [], seeds2: []):
    ''''''