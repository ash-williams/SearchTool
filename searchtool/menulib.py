"""
	menulib - holds functions used for menus
"""
import sys
import searchtool.settings as sets
import searchtool as st

def optionRunSearch():
	"""
		Prompts the user for required variables, validates and runs search
	"""
	print("OPTION 1: Run the search")
	print("######################################")
	print("If you are unsure of any setting, consult the application documentation")
	print()
	print("######################################")
	
	query_string = input("Enter your query string: ")
	indicators = input("Enter your indicators list, seperated by a comma (optional): ")
	start_date = input("Enter a start date in the format dd/mm/yyyy (optional): ")
	end_date = input("Enter a end date in the format dd/mm/yyyy (optional): ")
	number_of_results = input("Enter the number of results to retrieve (default 50): ")

	if indicators == "":
		indicators = "off"

	if start_date == "":
		start_date = "off"

	if end_date == "":
		end_date = "off"

	if number_of_results == "":
		number_of_results = 50
	else:
		number_of_results = int(number_of_results)

	st.searchtool.query(query_string, indicators, start_date, end_date, number_of_results)

def optionExportResults():
	"""
		Export the results to csv
	"""
	print("OPTION 2: Export the results to CSV")
	print("######################################")
	print("If you are unsure of any setting, consult the application documentation")
	print()
	print("######################################")
	print()
	sets.exportResultsCSV()

def optionExportArchive():
	"""
		Export the archive to csv
	"""
	print("OPTION 3: Export the archive to CSV")
	print("######################################")
	print("If you are unsure of any setting, consult the application documentation")
	print()
	print("######################################")
	print()
	sets.exportArchiveCSV()

def optionViewSettings():
	"""
		Prints the users settings
	"""
	print("OPTION 4: View the current settings")
	print("######################################")
	print("If you are unsure of any setting, consult the application documentation")
	print()
	print("######################################")
	print()
	print("API Key: " + sets.getAPIKey())
	print("Search Engine ID: " + sets.getSearchEngineID())
	print("Query mode: " + sets.getQueryMode())
	print("Number of runs: " + sets.getNumberOfRuns())
	print()

def optionUpdateAPIKey():
	"""
		Prompts the user for a API key, updates the db
	"""
	print("OPTION 5: Update the API Key")
	print("######################################")
	print("If you are unsure of any setting, consult the application documentation")
	print()
	print("######################################")
	print()
	api_key = input("Enter the new API key: ")

	if api_key != "":
		sets.setAPIKey(api_key)
	else:
		print("ERROR: Invalid API key, nothing changed")



def optionUpdateSearchEngineID():
	"""
		Prompts the user for a search engine id, updates the db
	"""
	print("OPTION 6: Update the search engine ID")
	print("######################################")
	print("If you are unsure of any setting, consult the application documentation")
	print()
	print("######################################")
	print()
	search_engine_id = input("Enter the new search engine ID: ")

	if search_engine_id != "":
		sets.setSearchEngineID(search_engine_id)
	else:
		print("ERROR: Invalid search engine ID, nothing changed")

def optionChangeQueryMode():
	"""
		Prompts the user for a mode, updates the query mode
	"""
	print("OPTION 7: Change the query mode")
	print("######################################")
	print("If you are unsure of any setting, consult the application documentation")
	print()
	print("######################################")
	print()
	query_mode = input("Enter the new query mode: ")

	if query_mode == "single" or query_mode == 'multi':
		sets.setQueryMode(query_mode)
	else:
		print("ERROR: Invalid query mode, nothing changed")

def optionChangeNumberOfRuns():
	"""
		Prompts the user for an integer, updates the number of runs
	"""
	print("OPTION 8: Change the number of runs")
	print("######################################")
	print("If you are unsure of any setting, consult the application documentation")
	print()
	print("######################################")
	print()
	number_of_runs = input("Enter the number of runs: ")

	if type(number_of_runs) is int and number_of_runs >= 1:
		sets.setNumberOfRuns(number_of_runs)
	else:
		print("ERROR: Invalid number of runs, nothing changed")

def optionUpdateIndicators():
	"""
		Prompts the user to update the indicator files, and then 
		updates database with new indicators.
	"""
	print("OPTION 9: Update the indicators")
	print("######################################")
	print("If you are unsure of any setting, consult the application documentation")
	print()
	print("######################################")
	print()
	print("Indicators will be updated with the values of the indicator files in /config/indicators. Update these files with desired indicators before continuing.")
	input("Hit enter to continue once you have updated the indicator files")

	print("Updating indicators...")
	db = sets.getDB()
	sets.loadIndicators(db, "Topic", "TOP", "./config/Indicators/topic.txt")
	sets.loadIndicators(db, "Reasoning", "RES", "./config/Indicators/reasoning.txt")
	sets.loadIndicators(db, "Blog", "BLG", "./config/Indicators/blog.txt")
	sets.loadIndicators(db, "Experience", "EXP", "./config/Indicators/experience.txt")

	print("Indicators updated")


def printMenu():
	"""
		Prints the menu
	"""
	print()
	print("Main Menu")
	print("*********************")
	print()
	print("Please select an option:")
	print()
	print("1 - Run search")
	print("2 - Export results")
	print("3 - Export result archive")
	print("4 - View all settings")
	print("5 - Update API key")
	print("6 - Update Search Engine ID")
	print("7 - Change query mode")
	print("8 - Change number of runs")
	print("9 - Update indicators")
	print()
	print("*********************")
	print("0 - Exit application")


def getValidOption():
	""" 
		Prompts a user for an option until a valid open is entered
		and then returns
	"""
	while(1):
		try:
			option = int(input("Enter an option: "))
		except:
			print("Please enter an integer")
		else:
			if option >= 0:
				return option
			else:
				print("Option must be an interger of zero or above")

def invokeMenuFunction(option):
	"""
		Calls a menu function based on the option given
	"""
	if option == 0:
		sys.exit()
	elif option == 1:
		optionRunSearch()
	elif option == 2:
		optionExportResults()
	elif option == 3:
		optionExportArchive()
	elif option == 4:
		optionViewSettings()
	elif option == 5:
		optionUpdateAPIKey()
	elif option == 6:
		optionUpdateSearchEngineID()
	elif option == 7:
		optionChangeQueryMode()
	elif option == 8:
		optionChangeNumberOfRuns()
	elif option == 9:
		optionUpdateIndicators()
	else:
		print("Option not recognised")
