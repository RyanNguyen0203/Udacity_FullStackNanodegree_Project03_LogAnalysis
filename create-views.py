#!/usr/bin/env python3

# This script will create custom views in the 'news' database

import sys
import psycopg2 as ps

# Constants and Functions
DBNAME = "news"

def create_view(q):

	# Helper functions:
	def connect(db_name="news"):
		''' Connect to the database and grab cursor '''
		try:
			db = ps.connect(dbname=db_name)
			c = db.cursor()
			return db,c
		except ps.Error:
			print("Unable to connect to the database")
			sys.exit(1)

	# Main

	# Connect to database & grab cursor
	db, c = connect()

	# Execute view-creating query
	c.execute(q)

	# Commit
	db.commit()

	# Close the connection
	db.close()

if __name__ == "__main__":

	q1= ''' CREATE VIEW article_requests AS
			SELECT articles.title, count(log.path) as requestnum
			FROM log, articles
			WHERE log.path LIKE '%'||articles.slug||'%'
			GROUP BY articles.title
			ORDER BY requestnum DESC;
		'''
	create_view(q1)


	q2= ''' CREATE VIEW author_requests AS
			SELECT articles.author, count(log.path) AS requestnum
			FROM log, articles
			WHERE log.path LIKE '%'||articles.slug||'%'
			GROUP BY articles.author
			ORDER BY requestnum DESC;
		'''
	create_view(q2)


	q3= ''' CREATE VIEW requests_per_day AS
			SELECT DATE_TRUNC('day', time) AS date, count(*)
			FROM log
			GROUP BY date;
		'''
	create_view(q3)


	q4= ''' CREATE VIEW errors_per_day AS
			SELECT DATE_TRUNC('day', time) AS date, count(*)
			FROM log
			WHERE SUBSTRING(status from 1 for 1) = '4' OR SUBSTRING(status from 1 for 1) = '5'
			GROUP BY date;
		'''
	create_view(q4)

	print("VIEWS SUCCESSFULLY CREATED ")