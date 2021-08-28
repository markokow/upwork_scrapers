import os
import googlemaps
import configparser

config = configparser.RawConfigParser()
config.read(filenames= 'twitter.properties')
print(config.sections())

apikey = config.get( 'google')
print(apikey)