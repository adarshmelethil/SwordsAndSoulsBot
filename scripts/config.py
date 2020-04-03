
import yaml

def load():
	with open("config.yaml", 'r') as stream:
		try:
			return yaml.safe_load(stream)
		except yaml.YAMLError as exc:
			print(exc)
			exit(1)

def save(config):
	with open("config.yaml", 'w+') as stream:
		yaml.dump(config, stream)
