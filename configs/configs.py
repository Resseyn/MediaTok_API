import configparser
read_config = configparser.ConfigParser()
read_config.read('settings.ini')

postgres_query = read_config['settings']['postgres_query'] # Query to pqsl