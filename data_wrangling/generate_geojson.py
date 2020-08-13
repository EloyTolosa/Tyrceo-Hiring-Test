import pymysql as sql
import pandas as pd
import numpy as np
import re
import Levenshtein as lev
from json import dump

# Database credentials
HOST = "35.187.55.190"
USER = "candidate"
PASS = "Fbps9Y7MhKQa4XPxjYo8"
DATABASE = "test"
# Program variables
STARTING_POKEMON = ["Charmander","Bulbasaur","Squirtle"] # List of valid pokemon
SIMILARITY_THRESHOLD = 0.80 # Levenshtein score threshold to ensure a word is similar to another. Can be changed a little bit, but this works fine.
# Debug variables
verbose = False # True to show execution prints. False shows nothing
csv = False # True exports the data to a csv file so we can check if it's correct or not. False does not export a csv file

def is_starting_pokemon(pokemon:str):
    """ This fucnction recieves the string of a pokemon. Returns true if the name is quite similar to Charmander, Bulbasaur or Squirtle
    so we can know if the name has a typo. Returns false otherwise """

    idx = 0
    similar = False
    length = len(STARTING_POKEMON)
    while ( (idx < length) and not similar ):
        similar = lev.ratio(STARTING_POKEMON[idx], pokemon) >= SIMILARITY_THRESHOLD
        idx += 1
        
    return similar



def main():
    ' Main function '

    # Before reading this, we need to take into acount that we could have separated this into 3 different functions (retrieving data, cleaning data, and creating points.geojson),
    # but, to keep this program simple, but still readable, we will keep the code like this, as it's not too dificult to read the code and the modules are easily discernible.-
    # All code is explained, except for basic code/algorithms

    print("Retrieving data from mysql server database...")
    # First of all connect to the database using credentials sent by email
    con = sql.connect(HOST, USER, PASS, DATABASE)
    # Prepare query: we want rows to be like this (latitude, longitude, pokemon, score), and we also want only the rows with score higher or equal than 0.5
    query = """ SELECT latitude, longitude, pokemon, score FROM data_at_coordinate 
    JOIN data ON data_at_coordinate.id_data = data.id
    JOIN coordinates ON data_at_coordinate.id_coordinate = coordinates.id
    WHERE score >= 0.5    
    """
    # Get query, and retrieve rows to see the data
    data = pd.read_sql(query, con)


    print("Cleaning data...")
    # Now that we know how data is arranged, we need to clean the data in order to keep just the pokemons we need.
    # This could have been done in the sql query, but in that case we would miss the typos and we want to keep them
    for idx, row in data.iterrows():
        # First, we want to remove leading and trailing spaces
        data.at[idx, 'pokemon'] = re.sub(r"^\s+|\s+$", "", row['pokemon'])
        # We also want to put the first letter of the pokemon to uppercase so all of them are equal
        data.at[idx, 'pokemon'] = data.at[idx, 'pokemon'].capitalize()
        # Now, we will check how similar the name of the pokemon is to either Bulbasaur, Squirtle or Charmander. If the match to any of the 3 names is higher than
        # let's say 80%, we will consider the name a typo and we will keep the row in the data. Otherwise, if the name does not match any of the 3, we will drop the row
        # as we only need the rows about our three starting pokemon
        # To do this, we will use the function ratio() from the Levenshtein library
        poke = row['pokemon']
        print(f"Pokemon:{poke}") if verbose else ""
        if ( poke not in STARTING_POKEMON and not is_starting_pokemon(poke) ):
            print(f"Pokemon {poke} from row {idx} removed") if verbose else ""
            data.drop(idx, inplace=True)
    # Lastly, we want to remove duplicates, just in case we have some
    data.drop_duplicates(inplace=True)

    
    print("Creating points.geojson...")
    # At this point, we have the data that we want. Now, we want to store it into a geoJSON file. First, we will transform our data to a dictionary, and then
    # dump it into a geojson file
    geojson = dict(type="FeatureCollection", features= [])
    geodata = {}
    # For every pokemon, we insert the data as we have it in the dictionary
    for idx, row in data.iterrows():
        geodata = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    row['longitude'],
                    row['latitude']
                ]
            },
            "properties": {
                "pokemon":row['pokemon'],
                "score":row['score']
            }
        }
        geojson['features'].append(geodata)

    with open("points.geojson", "w") as fd:
        dump(geojson, fd)
    

    print("Finished with success!")
    data.to_csv("data.csv") if csv else None

if __name__ == "__main__":
    main()