import farmer_actions

def get_plot_size(player_uuid: str):
    response = farmer_actions.supabase.table('player_data').select('plot_size').execute()
    return response.data[0]['plot_size']

# def get_plots(player_uuid: str):
#     
#     for i in range (2):
#         response = supabase.table('player_data').select(f'plot_{i}_type', f'plot_{i}_num', f'plot_{i}_end').eq('id', player_uuid).execute()
# 
def get_money(player_uuid: str):
    response = farmer_actions.supabase.table('player_data').select('money').execute()
    return response.data[0]['money']

# def get_seeds(player_uuid: str):
#     
# 
# def get_products(player_uuid: str):
#     ''''''
# 
# def get_product_value(player_uuid: str):
#     ''''''
# 
# def get_net_value(player_uuid: str):
#     ''''''

