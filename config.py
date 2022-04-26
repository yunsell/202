import configparser

config = configparser.ConfigParser()

config['MYSQL_CONFIG'] = {}
config['MYSQL_CONFIG']['db_connection'] = 'mysql+pymysql://drsong:drsong@192.168.0.97/ssda'
config['MYSQL_CONFIG']['sql_host'] = '192.168.0.97'
config['MYSQL_CONFIG']['user'] = 'root'
config['MYSQL_CONFIG']['password'] ='dr12#'
config['MYSQL_CONFIG']['db'] = 'ssda'
config['MYSQL_CONFIG']['charset'] = 'utf8mb4'

with open('./config.ini', 'w', encoding='utf-8') as configfile:
    config.write(configfile)
