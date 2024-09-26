import json

from src.jcutils.settings import config, config_loader

print(json.dumps(config_loader.config_dict))
print(config.app.name10)
