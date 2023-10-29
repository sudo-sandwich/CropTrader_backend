import sb_client

class UUIDNotFoundException(Exception):
    bleh = 0

def get_plot_size(player_uuid: str) -> int:
    response = sb_client.supabase.table('player_data').select('plot_size').eq('id', player_uuid).execute()
    if not response.data:
        raise UUIDNotFoundException(f'UUID {player_uuid} not found in database.')
    return response.data[0]['plot_size']

def get_plots(player_uuid: str):
    my_list = []

    for i in range(3):
        response = sb_client.supabase.table('player_data').select(f'plot_{i}_type', f'plot_{i}_num', f'plot_{i}_end').eq('id', player_uuid).execute()
        if not response.data:
            raise UUIDNotFoundException(f'UUID {player_uuid} not found in database.')
        my_list.append([response.data[0][f'plot_{i}_type'], response.data[0][f'plot_{i}_num'], response.data[0][f'plot_{i}_end']])
    
    return my_list

def get_money(player_uuid: str) -> int:
    response = sb_client.supabase.table('player_data').select('money').eq('id', player_uuid).execute()
    if not response.data:
        raise UUIDNotFoundException(f'UUID {player_uuid} not found in database.')
    return response.data[0]['money']

def get_seeds(player_uuid: str) -> list:
    response = sb_client.supabase.table('player_data').select('seeds').eq('id', player_uuid).execute()
    if not response.data:
        raise UUIDNotFoundException(f'UUID {player_uuid} not found in database.')
    return response.data[0]['seeds']

def get_products(player_uuid: str) -> list:
    response = sb_client.supabase.table('player_data').select('products').eq('id', player_uuid).execute()
    if not response.data:
        raise UUIDNotFoundException(f'UUID {player_uuid} not found in database.')
    return response.data[0]['products']

def get_product_value(player_uuid: str) -> list:
    response = sb_client.supabase.table('player_data').select('product_value').eq('id', player_uuid).execute()
    if not response.data:
        raise UUIDNotFoundException(f'UUID {player_uuid} not found in database.')
    return response.data[0]['product_value']

def get_net_worth(player_uuid: str) -> int:
    sum = 0
    my_products = get_products(player_uuid)
    for i in range(len(my_products)):
        sum += my_products[i]
    return sum + get_money(player_uuid)