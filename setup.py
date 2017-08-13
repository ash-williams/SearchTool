import sys
import json
from pymongo import MongoClient
import searchtool.settings as sets

def testDB():
    print("Testing connection to database...")

    try:
        path = "./config/config.json"

        with open(path) as config_file:
            config = json.load(config_file)

        client = MongoClient(config['db_url'])
        db = client[config['db_client']]
    except Exception as e:
        print(e.message)
        sys.exit()
    else:
        print("Successfully connected to db, continuing...")
    return db




def load(db):
    print("Loading indicators...")
    
    db.indicators.create_index("name", unique=True)
    db.indicators.create_index("code", unique=True)

    sets.loadIndicators(db, "Topic", "TOP", "./config/Indicators/topic.txt")
    sets.loadIndicators(db, "Reasoning", "RES", "./config/Indicators/reasoning.txt")
    sets.loadIndicators(db, "Blog", "BLG", "./config/Indicators/blog.txt")
    sets.loadIndicators(db, "Experience", "EXP", "./config/Indicators/experience.txt")

    print("Indicator loading complete...")


def loadConfig(db):
    print("Loading default config...")
    

    try:
        db.config.drop()
        path = "./config/config.json"

        with open(path) as config_file:
            config = json.load(config_file)

        config_json = {
            "config_id": 1,
            "api_key": config['api_key'],
            "search_engine_id": config['search_engine_id'],
            "query_mode": 'single',
            "number_of_runs": 1
        }
        
        db.config.insert_one(config_json)
    except Exception as e:
        print(e.message)
        print("ERROR: config not loaded correctly")
    else:
        print("Config loaded successfully...")

####
# Main
####
def main():
    print("Relevance querying setup...")

    # test the database connection
    db = testDB()

    # load the default indicators into the database
    load(db)

    # load the rest of the config
    loadConfig(db)

    print("Setup complete!")
    


if __name__ == "__main__":
    main()


