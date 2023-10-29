import farmer_actions
import player_exceptions

try:
    farmer_actions.plant("86a40223-53e6-44d4-969f-f102a89b81d0", 0, 3, 0)
except player_exceptions.PlayerException as e:
    print(e)