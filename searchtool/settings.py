"""
	Settings library - a general library of basic functions
"""
import sys
import os
import json
import csv
import time
from pymongo import MongoClient

def getDB():
	""" returns a db object """
	try:
		path = "./config/config.json"

		with open(path) as config_file:
			config = json.load(config_file)

		client = MongoClient(config['db_url'])
		db = client[config['db_client']]
	except Exception as e:
		print(e)
		sys.exit()
	else:
		return db


def setAPIKey(key):
	""" updates the API key in the database with the value of key """
	db = getDB()
	db.config.update(
		{"config_id": 1},
		{ 
			"$set": {"api_key":key}
		}
	)

def getAPIKey():
	""" returns the API key that is stored in the database """
	db = getDB()
	config = db.config.find_one({"config_id": 1})
	return config['api_key']

def setSearchEngineID(id):
	""" updates the search engine ID in the database with the value of id """
	db = getDB()
	db.config.update(
		{"config_id": 1},
		{ 
			"$set": {"search_engine_id":id}
		}
	)

def getSearchEngineID():
	""" returns the search engine ID that is stored in the database """
	db = getDB()
	config = db.config.find_one({"config_id": 1})
	return config['search_engine_id']

def setQueryMode(mode):
	""" updates the query mode in the database with the value of mode. Should be 'multi' or 'single'. """
	if mode == 'single' or mode == 'multi':
		db = getDB()
		db.config.update(
			{"config_id": 1},
			{ 
				"$set": {"query_mode":mode}
			}
		)

def getQueryMode():
	""" returns the current query mode """
	db = getDB()
	config = db.config.find_one({"config_id": 1})
	return config['query_mode']

def setNumberOfRuns(num):
	""" updates the number of runs in the database with the value of num. This setting is for handling stochastic results, see docs """
	db = getDB()
	db.config.update(
		{"config_id": 1},
		{ 
			"$set": {"number_of_runs":num}
		}
	)

def getNumberOfRuns():
	""" returns the current set number of runs """
	db = getDB()
	config = db.config.find_one({"config_id": 1})
	return config['number_of_runs']


def loadIndicators(db, collectionName, code, fileName):
    """ load the indicators into the database """
    try:
        db.indicators.remove({"name": collectionName})

        infile = open(fileName)
        lines = infile.readlines()


        words = []
        for line in lines:
            # line = line.replace(' ', '+')
            line = line.replace('\n','')
            words.append(line)


        json = {
                    "name": collectionName,
                    "words": words,
                    "code": code.upper()
                }

        db.indicators.insert_one(json)
    except Exception as e:
        print(e.message)
        print("ERROR: No indicators loaded for " + collectionName)
    else:
        print(str(len(lines)) + " indicator(s) loaded for " + collectionName)


def exportResultsCSV():
	"""
		Exports results collection to CSV file
	"""
	db = getDB()

	directory = './output'
	filename = str(time.time()) +'_results.csv'
	path = directory + '/' + filename

	if not os.path.exists(directory):
		os.makedirs(directory)

	with open(path, 'w', encoding='utf8') as csvfile:
	    fieldnames = ['query', 'query_string', 'search_engine_id', 'start_date', 'end_date', 'query_mode', 'number_of_runs', 'number_of_results', 'start_from_result', 'total_results', 'timestamp', 'title', 'url', 'date', 'meta']

	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
	    writer.writeheader()

	    for doc in db.query_results.find():
	    	results = doc['results']

	    	for r in results:
	    		writer.writerow({
	    			"query": doc['query'],
	    			"query_string": doc['query_string'],
	    			"search_engine_id": doc['search_engine_id'],
	    			"start_date": doc['start_date'],
	    			"end_date": doc['end_date'],
	    			"query_mode": doc['query_mode'],
	    			"number_of_runs": doc['number_of_runs'],
	    			"number_of_results": doc['number_of_results'],
	    			"start_from_result": doc['start_from_result'],
	    			"total_results": doc['total_results'],
	    			"timestamp": doc['timestamp'],
	    			"title": r['title'],
	    			"url": r['url'],
	    			"date": r['date'],
	    			"meta": r['meta']
	    		})
	csvfile.close()

	print("Exported to CSV at: " + path)
	    		

def exportArchiveCSV():
	"""
		Exports archive collection to CSV file
	"""
	db = getDB()

	directory = './output'
	filename = str(time.time()) +'_archive.csv'
	path = directory + '/' + filename

	if not os.path.exists(directory):
		os.makedirs(directory)

	with open(path, 'w', encoding='utf8') as csvfile:
	    fieldnames = ['query', 'query_string', 'search_engine_id', 'start_date', 'end_date', 'query_mode', 'number_of_runs', 'number_of_results', 'start_from_result', 'total_results', 'timestamp', 'title', 'url', 'date', 'meta']

	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
	    writer.writeheader()

	    for doc in db.query_archive.find():
	    	results = doc['results']

	    	for r in results:
	    		writer.writerow({
	    			"query": doc['query'],
	    			"query_string": doc['query_string'],
	    			"search_engine_id": doc['search_engine_id'],
	    			"start_date": doc['start_date'],
	    			"end_date": doc['end_date'],
	    			"query_mode": doc['query_mode'],
	    			"number_of_runs": doc['number_of_runs'],
	    			"number_of_results": doc['number_of_results'],
	    			"start_from_result": doc['start_from_result'],
	    			"total_results": doc['total_results'],
	    			"timestamp": doc['timestamp'],
	    			"title": r['title'],
	    			"url": r['url'],
	    			"date": r['date'],
	    			"meta": r['meta']
	    		})
	csvfile.close()

	print("Exported to CSV at: " + path)


def exportDuplications():
	"""
		Analyses the archive results collection and returns a csv file formatted like:

		{
			url, 		# the url of the article
			count, 		# the number of times that url appears
			query_list,	# in what queries does this url exist
			date_list	# on what days did this url appear
		}

	"""
	db = getDB()

	
	directory = './output'
	filename = str(time.time()) +'_duplications.csv'
	path = directory + '/' + filename

	if not os.path.exists(directory):
		os.makedirs(directory)

	with open(path, 'w', encoding='utf8') as csvfile:
	    fieldnames = ['url', 'frequency', 'query_list', 'date_list']

	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
	    writer.writeheader()

	    for item in db.query_duplications.find():
	    	writer.writerow({
				"url": item['url'],
				"frequency": item['frequency'],
				"query_list": str(item['query_list']),
				"date_list": str(item['date_list'])
    		})
	
	csvfile.close()

	print("Exported to CSV at: " + path)
	    

