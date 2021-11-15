import json
import os

configs = ['config_prod.json', 'config_dev.json', 'config.json']

for conf in configs:
    if(os.path.exists(conf)):
        with open(conf, 'r') as f:
            config = json.load(f)
            break
    