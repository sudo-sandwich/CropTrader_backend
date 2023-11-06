from datetime import datetime, timedelta, timezone
import random

import encryption
import constants
import player_exceptions
import sb_client

class UsernameAlreadyExistsException(Exception):
    ''''''
class UUIDNotFoundException(Exception):
    ''''''

# births a new farmer into this world. in other words, creates a new player account.
def create_farmer(username: str, password: str):
    response = sb_client.supabase.table('player_data').select('username').eq('username', username).execute()
    if response.data:
        raise UsernameAlreadyExistsException(f'Username {username} already exists.')

    hashed_password, salt = encryption.register(password)
    
    random_selection = random.random() * constants.ADVANCED_SEED_TOTAL_WEIGHT
    start_advanced_seed_id = constants.NUM_BASIC_SEEDS
    while random_selection > constants.SEED_CONSTANTS[start_advanced_seed_id]['weight']:
        random_selection -= constants.SEED_CONSTANTS[start_advanced_seed_id]['weight']
        start_advanced_seed_id += 1
    
    start_seed_count = [5,5,5,0,0,0,0,0,0,0]
    start_seed_count[start_advanced_seed_id] = 1

    string_data = salt.decode('utf-8')

    response = sb_client.supabase.table('player_data').insert({
        'username': username,
        'password': hashed_password,
        'seeds': start_seed_count,
        'salt': string_data
    }).execute()

# plants any number of seeds to an empty plot.
def plant(player_uuid: str, plot_id: int, num_seeds: int, seed_id: int) -> {}:
    response = sb_client.supabase.table('player_data').select('plot_size', 'seeds', f'plot_{plot_id}_num', f'plot_{plot_id}_end').eq('id', player_uuid).execute()

    if not response.data:
        raise UUIDNotFoundException(f'UUID {player_uuid} not found in database.')
    elif num_seeds > response.data[0]['plot_size']:
        raise player_exceptions.PlotNotLargeEnoughException(f'Plot is not large enough. Max size: {response.data[0]['plot_size']}')
    elif response.data[0]['seeds'][seed_id] < num_seeds:
        raise player_exceptions.NotEnoughSeedsException(f"Player does not have enough seeds. id: {seed_id}")
    elif response.data[0][f'plot_{plot_id}_num'] != 0:
        raise player_exceptions.PlotNotEmptyException(f'Plot {plot_id} is not empty.')
    
    new_seed_count = response.data[0]['seeds']
    new_seed_count[seed_id] -= num_seeds
    end_time = datetime.now(timezone.utc) + timedelta(seconds=constants.SEED_CONSTANTS[seed_id]['grow_time_sec'])
    end_time_iso = end_time.isoformat()
    response = sb_client.supabase.table('player_data').update({
        'seeds': new_seed_count,
        f'plot_{plot_id}_type': seed_id, 
        f'plot_{plot_id}_num': num_seeds, 
        f'plot_{plot_id}_end': end_time_iso
    }).eq('id', player_uuid).execute()

# harvests a complete plot and adds products/seeds to a player's inventory.
def harvest(player_uuid: str, plot_id: int):
    response = sb_client.supabase.table('player_data').select('seeds', 'products', f'plot_{plot_id}_type', f'plot_{plot_id}_num', f'plot_{plot_id}_end').execute()

    if not response.data:
        raise UUIDNotFoundException(f'UUID {player_uuid} not found in database.')
    elif response.data[0][f'plot_{plot_id}_num'] == 0:
        raise player_exceptions.PlotNotEmptyException(f'Plot {plot_id} is empty.')
    elif response.data[0][f'plot_{plot_id}_end'] > datetime.now(timezone.utc).isoformat():
        raise player_exceptions.PlotNotReadyException(f'Plot {plot_id} is not ready.')

    new_seed_count = response.data[0]['seeds']
    # TODO: add an actual multiplier here instead of just x2.
    new_seed_count[response.data[0][f'plot_{plot_id}_type']] += response.data[0][f'plot_{plot_id}_num'] * 2
    new_product_count = response.data[0]['products']
    new_product_count[response.data[0][f'plot_{plot_id}_type']] += response.data[0][f'plot_{plot_id}_num']

    response = sb_client.supabase.table('player_data').update({
        'seeds': new_seed_count,
        'products': new_product_count,
        f'plot_{plot_id}_num': 0
    }).eq('id', player_uuid).execute()

# sells a single product.
def sell(player_uuid: str, product_id: int):
    response = sb_client.supabase.table('player_data').select('products', 'product_value', 'money').eq('id', player_uuid).execute()

    if not response.data:
        raise UUIDNotFoundException(f'UUID {player_uuid} not found in database.')
    elif response.data[0]['products'][product_id] == 0:
        raise player_exceptions.NotEnoughProductsException(f'Player does not have enough products. id: {product_id}')

    new_product_count = response.data[0]['products']
    new_product_count[product_id] -= 1
    new_money_count = response.data[0]['money'] + constants.SEED_CONSTANTS[product_id]['value'] * response.data[0]['product_value'][product_id]
    new_product_value = response.data[0]['product_value']
    for i in range(len(response.data[0]['product_value'])):
        if i == product_id:
            new_product_value[i] -= 0.05
        else:
            new_product_value[i] += 0.01
        new_product_value[i] = max(0, min(1, new_product_value[i]))

    response = sb_client.supabase.table('player_data').update({
        'products': new_product_count,
        'product_value': new_product_value,
        'money': new_money_count
    }).eq('id', player_uuid).execute()

# buys a single mystery seed.
def buy_mystery_seed(player_uuid: str):
    response = sb_client.supabase.table('player_data').select('money', 'seeds').eq('id', player_uuid).execute()

    if not response.data:
        raise UUIDNotFoundException(f'UUID {player_uuid} not found in database.')
    elif response.data[0]['money'] < constants.MYSTERY_SEED_COST:
        raise player_exceptions.NotEnoughMoneyException(f'Player does not have enough money. Cost: {constants.MYSTERY_SEED_COST}')
    
    random_selection = random.random() * constants.SEED_TOTAL_WEIGHT
    current_seed_id = 0
    while random_selection > constants.SEED_CONSTANTS[current_seed_id]['weight']:
        random_selection -= constants.SEED_CONSTANTS[current_seed_id]['weight']
        seed_id += 1
    new_seed_count = response.data[0]['seeds']
    new_seed_count[current_seed_id] += 1
    new_money = response.data[0]['money'] - constants.MYSTERY_SEED_COST

    response = sb_client.supabase.table('player_data').update({
        'seeds': new_seed_count,
        'money': new_money
    }).eq('id', player_uuid).execute()

# upgrades all plots to a larger size.
def upgrade_plot(player_uuid: str):
    response = sb_client.supabase.table('player_data').select('money', 'plot_size').eq('id', player_uuid).execute()

    upgrade_index = response.data[0]['plot_size'] / constants.PLOT_SIZE_UPGRADE_INCREMENT - 1

    if not response.data:
        raise UUIDNotFoundException(f'UUID {player_uuid} not found in database.')
    elif upgrade_index >= len(constants.PLOT_UPGRADE_COSTS):
        raise player_exceptions.MaximumPlotSizeException(f'Player plot size is already at maximum. Size: {response.data[0]['plot_size']}')

    upgrade_cost = constants.PLOT_UPGRADE_COSTS[upgrade_index]

    if response.data[0]['money'] < upgrade_cost:
        raise player_exceptions.NotEnoughMoneyException(f'Player does not have enough money. Cost: {upgrade_cost}')

    new_money = response.data[0]['money'] - upgrade_cost
    new_plot_size = response.data[0]['plot_size'] + constants.PLOT_SIZE_UPGRADE_INCREMENT

    response = sb_client.supabase.table('player_data').update({
        'money': new_money,
        'plot_size': new_plot_size
    }).eq('id', player_uuid).execute()

# trades seeds with another player.
def trade(player1_uuid: str, player2_uuid: str, seeds1: [], seeds2: []):
    response1 = sb_client.supabase.table('player_data').select('seeds').eq('id', player1_uuid).execute()
    response2 = sb_client.supabase.table('player_data').select('seeds').eq('id', player2_uuid).execute()

    if not response1.data:
        raise UUIDNotFoundException(f'UUID {player1_uuid} not found in database.')
    elif not response2.data:
        raise UUIDNotFoundException(f'UUID {player2_uuid} not found in database.')

    for i in range(len(seeds1)):
        if seeds1[i] > response1.data[0]['seeds'][i]:
            raise player_exceptions.NotEnoughSeedsException(f'Player 1 does not have enough seeds. id: {i}')
        if seeds2[i] > response2.data[0]['seeds'][i]:
            raise player_exceptions.NotEnoughSeedsException(f'Player 2 does not have enough seeds. id: {i}')
    
    new_seeds1 = response1.data[0]['seeds']
    new_seeds2 = response2.data[0]['seeds']

    for i in range(len(seeds1)):
        new_seeds1[i] -= seeds1[i]
        new_seeds2[i] += seeds1[i]
        new_seeds1[i] += seeds2[i]
        new_seeds2[i] -= seeds2[i]
    
    response1 = sb_client.supabase.table('player_data').update({
        'seeds': new_seeds1
    }).eq('id', player1_uuid).execute()
    response2 = sb_client.supabase.table('player_data').update({
        'seeds': new_seeds2
    }).eq('id', player2_uuid).execute()