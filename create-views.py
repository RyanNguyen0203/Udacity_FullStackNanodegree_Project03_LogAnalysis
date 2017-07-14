# This script will create custom views in the 'news' database

import psycopg2 as ps

DBNAME = "news"

if __name__ == "__main__":
	db = ps.connect(dbname="news")
	c = db.cursor()

	q1= ''' CREATE VIEW article_requests AS
			SELECT articles.title, count(log.path) as requestnum
			FROM log, articles
			WHERE log.path LIKE '%'||articles.slug||'%'
			GROUP BY articles.title
			ORDER BY requestnum DESC;
		'''
	q2= ''' CREATE VIEW author_requests AS
			SELECT articles.author, count(log.path) AS requestnum
			FROM log, articles
			WHERE log.path LIKE '%'||articles.slug||'%'
			GROUP BY articles.author
			ORDER BY requestnum DESC;
		'''
	q3= ''' CREATE VIEW requests_per_day AS
			SELECT DATE_TRUNC('day', time) AS date, count(*)
			FROM log
			GROUP BY date;
		'''

	q4= ''' CREATE VIEW errors_per_day AS
			SELECT DATE_TRUNC('day', time) AS date, count(*)
			FROM log
			WHERE SUBSTRING(status from 1 for 1) = '4' OR SUBSTRING(status from 1 for 1) = '5'
			GROUP BY date;
		'''
	c.execute(q1)
	c.execute(q2)
	c.execute(q3)
	c.execute(q4)
	db.commit()
	db.close()

	print("VIEWS SUCCESSFULLY CREATED ")