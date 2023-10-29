import farmer_actions
import player_exceptions

try:
    farmer_actions.plant("59d4024d-2315-403b-b36b-2bc93f614ca3", 0, 3, 0)
except player_exceptions.PlayerException as e:
    print(e)