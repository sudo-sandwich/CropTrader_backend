import json

SEED_CONSTANTS = None
SEED_TOTAL_WEIGHT = 0

MYSTERY_SEED_COST = 100000

PLOT_UPGRADE_COSTS = None
PLOT_SIZE_UPGRADE_INCREMENT = 5

with open('seed_constants.json', 'r') as seed_constants_json:
    SEED_CONSTANTS = json.load(seed_constants_json)

for seed_id in range(len(SEED_CONSTANTS)):
    SEED_TOTAL_WEIGHT += SEED_CONSTANTS[seed_id]['weight']

with open('plot_upgrade_costs.json', 'r') as plot_upgrade_costs_json:
    PLOT_UPGRADE_COSTS = json.load(plot_upgrade_costs_json)