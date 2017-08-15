"""
	SearchTool's main library
"""
import sys
import searchtool.settings as sets
import searchtool.querylib as ql 
import searchtool.menulib as ml

def query(query_string, indicators, start_date, end_date, number_of_results):
	"""
		Query the api
	"""
	if indicators != 'off':
		# convert indicators to a list
		indicators = indicators.split(',')

	try:
		number_of_results = int(number_of_results)
	except:
		# ignore, it will be picked up by validateOptionalArgs
		pass

	# check optional args are valid
	validArgs = ql.validateOptionalArgs(indicators, start_date, end_date, number_of_results)

	if not validArgs:
		print("ERROR: one or more of the optional arguments are invalid, please review the documentation and try again")
		sys.exit()

	# get config
	db = sets.getDB()
	query_mode = sets.getQueryMode()
	number_of_runs = sets.getNumberOfRuns()

	
	# generate queries
	# SINGLE query mode returns a string
	# MULTI query mode returns a list of strings
	generated_query = ql.generateQuery(query_string, indicators, query_mode)

	# query the API
	results = []

	if query_mode == 'single' or indicators == 'off':
		# generated_query is a string
		for i in range(0, number_of_runs):
			results += [ql.queryAPI(generated_query, start_date, end_date, number_of_results)]
	else:
		# generated query is a list
		for i in range(0, number_of_runs):
			for query in generated_query:
				results += [ql.queryAPI(query, start_date, end_date, number_of_results)]

	# store the results in the database
	db.query_results.drop()

	# results is now a nested list of len(number_of_runs)
	# each nested list is a list of json results from 0 to num_of_results

	for result_portion in results:
		for r in result_portion:
			db.query_results.insert_one(r)
			db.query_archive.insert_one(r)

	print("Query complete, exporting db.results...")
	sets.exportResultsCSV()

	print("End of query")



def menu():
	""" 
		Run the main menu
	"""
	print("Welcome to SearchTool")
	print("*********************")

	while(1):
		ml.printMenu()
		option = ml.getValidOption()
		ml.invokeMenuFunction(option)
