"""
	querylib - holds functions used for querying
"""
import searchtool.settings as sets
import re
import itertools
from googleapiclient.discovery import build
import datetime
import time
import json

def validateOptionalArgs(indicators, start_date, end_date, number_of_results):
	"""
		returns true if all option arguments are valid
	"""
	if indicators != "off":
				
		# check indicators contains valid codes
		db = sets.getDB()
		db_indicator_types = db.indicators.find()

		db_codes = []
		for ind_type in db_indicator_types:
			db_codes.append(ind_type['code'])

		for code in indicators:
			if code not in db_codes:
				return False

	if start_date != "off":
		# check start date is valid
		isValidStartDate = re.match(r'^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$', start_date)
		
		if not isValidStartDate:
			return False

	if end_date != "off":
		# check start date is valid
		isValidEndDate = re.match(r'^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$', end_date)

		if not isValidEndDate:
			return False

	# check number of results is a valid int
	if type(number_of_results) is not int:
		return False

	# check number of results is multiple of ten
	if number_of_results % 10 != 0:
		return False


	return True


def generateQuery(query_string, indicators, query_mode):
	"""
		Generate query(s) from base string and indicators.
		- SINGLE query mode returns a string
		- MULTI query mode returns a list of strings
	"""
	db = sets.getDB()

	# if indicators off, just return the query
	if indicators == "off":
		return query_string
	
	# indicator list provided
	# handle based on query mode
	if query_mode == 'single':
		# query mode is SINGLE, create a single string

		# get the indicators from the database
		indcator_types = []

		for ind_code in indicators:
			indicator_types.append(db.indicators.find({"code": ind_code}))

		generated_query_string = query_string
		
		for ind_type in indcator_types:
			generated_query_string += " AND ("
			
			ind_words = []
			for iword in ind_type['words']:
				ind_words += iword

			for word in ind_words:
				generated_query_string +=  + "'" + word + "' OR "
			generated_query_string += ")"

		return generated_query_string

	else:
		# query mode is MULTI, create a list of queries

		# get the indicators from the database
		indicator_types = []
		
		for ind_code in indicators:
			db_ind = db.indicators.find_one({"code": ind_code})
			indicator_types.append(db_ind)

		# make ind_words a nested list of indicators by their indicator type
		ind_words = []
		for ind_type in indicator_types:
			ind_words.append(ind_type['words'])

		# get all combinations
		all_combos = list(itertools.product(*ind_words))

		query_list = []

		# have one query that is just the query string
		query_list.append(query_string)

		for combo in all_combos:
			combo = list(combo)

			temp_query = query_string
			for key_phrase in combo:
				temp_query += " AND '" + key_phrase + "'"

			query_list.append(temp_query)

		return query_list

def get_date_string(start_date, end_date):
	"""
		Turns the dates into a string for the API
	"""
	# first convert dates
	start_date = start_date.replace('/', '')
	end_date = end_date.replace('/','')

	if start_date == 'off' and end_date == 'off':
		return ""
	elif start_date == 'off' and end_date != 'off':
		return "date:r::" + end_date
	elif start_date != 'off' and end_date == 'off':
		return "date:r:" + start_date + ":"
	else:
		return "date:r:" + start_date + ":" + end_date

def queryAPI(query, start_date, end_date, number_of_results):
	"""
		Query the API, return the results as a list of JSON object
	"""

	# get config
	api_key = sets.getAPIKey()
	search_engine_id = sets.getSearchEngineID()

	service = build("customsearch", "v1", developerKey=api_key)

	result_list = []

	# make multiple api calls in multiples of 10 to get number of results
	for i in range(0, number_of_results, 10):
		i += 1

		api_call = service.cse().list(
			q=query,
			cx=search_engine_id,
			sort=get_date_string(start_date, end_date),
			start=i
		)

		result = api_call.execute()

		# get the results
		results = []
		total_results = result['queries']['request'][0]['totalResults']
		if int(total_results) > 0:
			for item in result['items']:
				splitMeta = item['snippet'].split(" ")

				if len(splitMeta) > 2:
					if splitMeta[3] == "...":
						date = splitMeta[0] + " " + splitMeta[1] + " " + splitMeta[2]
						meta = " ".join(splitMeta[4:len(splitMeta)])
					else:
						date = "No date available"
						meta = item['snippet']

				results.append({
					'title': item['title'],
					'url': item['link'],
					'date': date,
					'meta': meta
				})


		#build the JSON object
		json_data = {
			"query"				:	str(api_call.__dict__["uri"]),
			"query_string"		:	str(query),
			"search_engine_id"	:	str(search_engine_id),
			"start_date"		:	str(start_date),
			"end_date"			:	str(end_date),
			"query_mode"		:	str(sets.getQueryMode()),
			"number_of_runs"	:	str(sets.getNumberOfRuns()),
			"number_of_results"	:	number_of_results,
			"start_from_result" :	i,
			"total_results"		:	total_results,
			"timestamp"			:	str(datetime.datetime.fromtimestamp(time.time())),
			"results"			:	results
		}

		result_list.append(json_data)
	return result_list

def calculateDuplications():
	"""
	Drops and populates the query_duplications table with calculated duplications
	"""
	db = sets.getDB()

	db.query_duplications.drop()

	# get all results (query history)
	archive_results = db.query_archive.find()

	# init duplication count list
	duplication_count = []


	for res in archive_results:
		query_string = res['query_string'] 
		date = res['timestamp'][0:13] #2017-08-21 16:34:31.622082
		results_list = res['results']
		for r in results_list:
			url = r['url']

			# Ignore query parameters
			url_split = url.split('?')
			base_url = url_split[0]

			flag = False

			for record in duplication_count:
				if base_url == record['url']:
					record['count'] = record['count'] + 1

					if query_string not in record['query_list']:
						record['query_list'].append(query_string)

					if date not in record['date_list']:
						record['date_list'].append(date)
					
					flag = True
					break

			if flag == False:
				duplication_count.append({"url": base_url, "count": 1, "query_list": [query_string], "date_list": [date]})

	for item in duplication_count:
		db.query_duplications.insert({
			"url": item['url'],
			"frequency": item['count'],
			"query_list": item['query_list'],
			"date_list": item['date_list']
		})




	