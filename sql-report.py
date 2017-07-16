#!/usr/bin/env python3

import sys
import psycopg2 as ps

# Constants and functions
DBNAME = "news"


def report(q, answer, unit):
	''' This function will connect to database, execute query,
	fetch query result and print out the answer for a question '''

	# Helper functions
	def connect(db_name="news"):
		''' Connect to the database and grab cursor '''
		try:
			db = ps.connect(dbname=db_name)
			c = db.cursor()
			return db,c
		except ps.Error:
			print("Unable to connect to the database")
			sys.exit(1)

	def print_data(data, unit):
		''' Print output from the fetched results '''
		for item in data:
			print("> {} - {} {}".format(item[0], str(item[1]), unit))



	# Connect to database & grab cursor
	db, c = connect()

	# Execute query
	c.execute(q)

	# Fetch data
	data = c.fetchall()

	# Close connection
	db.close()

	# Print answer
	print(answer)
	print_data(data, unit)

if __name__ == "__main__":
	''' The program only runs if it is called directly '''

	# Q1: Number of requests for each article
	q = ''' SELECT articles.title, COUNT(log.path) AS num
			FROM log, articles
			WHERE log.path like '%'||articles.slug||'%'
			GROUP BY articles.title
			ORDER BY num DESC
			LIMIT 3;
		'''
	report(q, "\n3 MOST POPULAR ARTICLES:", "requests")

	# Q2: Number of requests for each author
	q = ''' SELECT authors.name, author_requests.requestnum
			FROM authors LEFT JOIN author_requests
			ON authors.id = author_requests.author
			LIMIT 3
		'''
	report(q, "\n3 MOST POPULAR AUTHORS", "requests")

	# Q3: Days on which more than 1% of requests lead to errors
	q = ''' SELECT TO_CHAR(date::timestamp::date, 'FMMonth DD, YYYY'), ROUND(rate, 1)
			FROM (
				SELECT requests_per_day.date,
				CAST(errors_per_day.count AS NUMERIC)/
				CAST(requests_per_day.count AS NUMERIC)*100
				AS rate
				FROM requests_per_day JOIN errors_per_day
				ON requests_per_day.date = errors_per_day.date
			) AS yo
			WHERE rate > 1;
		'''
	report(q, "\nDAY(S) WITH REQUEST ERROR > 1%:", "%")
