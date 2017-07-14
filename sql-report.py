import psycopg2 as ps

# Constants and functions
DBNAME = "news"


def report(q, answer, unit):
    ''' This function will execute query q and print out the answers '''

    def print_data(data, unit):
        ''' Print fetched data '''
        for item in data:
            print("> {} - {} {}".format(item[0], str(item[1]), unit))

    # Execute query
    c.execute(q)

    # Fetch data
    data = c.fetchall()

    # Print answer
    print(answer)
    print_data(data, unit)

if __name__ == "__main__":
    ''' The program only runs if it is called directly '''

    # Connect to the database & set up cursor
    db = ps.connect(dbname="news")
    c = db.cursor()

    # Q1: Number of requests for each article
    q = ''' SELECT articles.title, COUNT(log.path) AS num
            FROM log, articles
            WHERE log.path like '%'||articles.slug||'%'
            GROUP BY articles.title
            ORDER BY num DESC;
        '''
    report(q, "\nARTICLE POPULARITY:", "requests")

    # Q2: Number of requests for each author
    q = ''' SELECT authors.name, author_requests.requestnum
            FROM authors LEFT JOIN author_requests
            ON authors.id = author_requests.author
        '''
    report(q, "\nAUTHOR POPULARITY:", "requests")

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
    report(q, "\nDAY WITH REQUEST ERROR > 1%:", "%")

    # Close connection
    db.close()
