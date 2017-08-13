"""
	SearchTool.py - the applications start point
"""
import sys
import searchtool.searchtool as st


def main():
	"""
		Start the application

		If there are arguments, run programatically, else run menu
	"""
	if len(sys.argv) > 1:
		# query		 = base query string (required)
		# indicators = (optional/default off)
		# start_date = (optional/default off)
		# end_date   = (optional/default off)
		query_string = ""
		indicators   = "off"
		start_date   = "off"
		end_date     = "off"
		number_of_results = 50
		
		#print(sys.argv) # for debug
		
		# query is required, first handle that
		query = sys.argv[1].split('=')
		if query[0] == 'query':
			query_string = query[1]
		else:
			print("ERROR: argument 'query' is required.")
			sys.exit()

		# now handle the optional args, if they exist
		if len(sys.argv) > 2:
			for i in range(2, len(sys.argv)):
				argument = sys.argv[i].split("=")
				if argument[0] == "indicators":
					indicators = argument[1]
				elif argument[0] == "start_date":
					start_date = argument[1]
				elif argument[0] == "end_date":
					end_date = argument[1]
				elif argument[0] == "number_of_results":
					number_of_results = argument[1]
				else:
					print("ERROR: optional argument not recognised, check spelling")
					sys.exit()

		# Print arguments
		print("Arguments are:")
		print("Query string: " + query_string)
		print("Indicator list: " + indicators)
		print("Start date: " + start_date)
		print("End date: " + end_date)
		print("Number of results: " + str(number_of_results))
		print("Now running query...")

		# Run the query
		st.query(query_string, indicators, start_date, end_date, number_of_results)

	else:
		# No arguments given, run the CLI instead
		st.menu()




if __name__ == '__main__':
	main()