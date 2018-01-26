# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 12:15:29 2017

"""

from flask import Flask
import argparse
import logging
import os
import json

import controllers.pessoal as con

app = Flask(__name__)
app.register_blueprint(con.pessoal_controllers)

def load_db_config(config_file):
    filename = config_file
    if not os.path.dirname(os.path.dirname(config_file)):
        filename = os.path.dirname(__file__) + "/" + config_file

    if not os.path.isfile(filename):
        logging.error("Database config file is missing")
        # TODO raise exception

    configuration = json.load(open(filename))
    return configuration['servername'], configuration['database'], configuration['username'], configuration['password']

if __name__ == '__main__':
    # configuring the parameters parser and storing parameters in global vars
    parser = argparse.ArgumentParser(description='"API Servidor" to provide/handle employee\'s data.')

    parser.add_argument("-s", "--servername", metavar='server_name', 
                        help='Name of the database host server')
    parser.add_argument("-d", "--database", 
                        help="Name of the database", metavar="database_name")
    parser.add_argument("-u", "--username", 
                        help="Username to access the database", metavar="username")
    parser.add_argument("-w", "--password", 
                        help="User's password to acess the database", metavar="user_password")
    parser.add_argument("-c", "--config_file", 
                        help="Database config file path", metavar="config_file")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("-p", "--port", type=int, default=8000,
                        help="Port the program will try to use to serve de API", metavar="api_port")
    args = parser.parse_args()

    if args.config_file:
        args.servername, args.database, args.username, args.password = load_db_config(args.config_file)
    con.configure_params(args.servername, args.database, args.username, args.password)

    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(filename='python-api.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)-3d - %(name)-12s - %(levelname)-8s => %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=log_level)
    logging.info("API Employee started")

    # starting the web server
    app.run(debug=args.debug, host='0.0.0.0', port=args.port)
