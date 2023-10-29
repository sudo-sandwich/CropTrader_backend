import farmer_actions
from http_server import app
import player_exceptions
import getters

# try:
#     farmer_actions.plant("59d4024d-2315-403b-b36b-2bc93f614ca3", 0, 3, 0)
# except player_exceptions.PlayerException as e:
#     print(e)

# print(getters.get_plot_size('86a40223-53e6-44d4-969f-f102a89b81d0'))
# print(getters.get_money('86a40223-53e6-44d4-969f-f102a89b81d0'))
# print(getters.get_plots('86a40223-53e6-44d4-969f-f102a89b81d0'))
# print(getters.get_seeds('86a40223-53e6-44d4-969f-f102a89b81d0'))
# print(getters.get_products('86a40223-53e6-44d4-969f-f102a89b81d0'))
# print(getters.get_product_value('86a40223-53e6-44d4-969f-f102a89b81d0'))
# print(getters.get_net_worth('86a40223-53e6-44d4-969f-f102a89b81d0'))

farmer_actions.create_farmer("Joe")
farmer_actions.create_farmer("Bob")
farmer_actions.create_farmer("Lee")
farmer_actions.create_farmer("Moe")
farmer_actions.create_farmer("Cox")
farmer_actions.create_farmer("Ali")
farmer_actions.create_farmer("Poe")

if __name__ == '__main__':
    app.run()
