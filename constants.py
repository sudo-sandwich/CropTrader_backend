import json

SEED_CONSTANTS = None
SEED_TOTAL_WEIGHT = 0

MYSTERY_SEED_COST = 100000

with open('seed_constants.json', 'r') as seed_constants_json:
    SEED_CONSTANTS = json.load(seed_constants_json)

for seed_id in range(len(SEED_CONSTANTS)):
    SEED_TOTAL_WEIGHT += SEED_CONSTANTS[seed_id]['weight']