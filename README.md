# Udacity Full Stack Nanodegree Program Project 3 - Log Analysis with Python and PostgreSQL
Create an __internal__ reporting tool for a newspaper site. The tool is written in Python to query a PostgreSQL database of aprroximately 2 million entries and print output to the terminal.
## Table schemas
The relational databse contains 3 tables:
- articles

Columns | Type | Desc
------- | ---- | ----
author | integer | author ID
title | text | article's title
slug | text | article's slug
lead | text | article's lead sentence
body | text | article's body
time | timestamp with time zone | when the article is added to the database
id | integer | article's id number

- authors

Columns | Type | Desc
------- | ---- | ----
name | text | author's full name
bio | text | author's biographical infomation in a sentence
id | integer | author's id number

- log

Columns | Type | Desc
------- | ---- | ----
path | text | the path requested
ip | inet | IP address of the requesting machine
method | text | resquest method
status | text | request status
time | timestamp with time zone | when the request is received
id | integer | request's id number
## Insights to extract
- Articles' popularity (measured by number of requests)
- Authors' popularity (measured by number of requests for their articles)
- Days on which more than 1% of requests lead to errors
## Program's general description
The Python script `sql-report.py` makes use of Python DB-API psycopg2 to query data from PostgreSQL database. To minimise the number of queries used, each insight above is drawn using only one SQL query. The answer is then printed out in plain text to the terminal window that calls the script.
## Installation
1. Follow this [guide](https://goo.gl/Nx5u8L) to install VirtualBox and configure it with Vagrant.
2. Then follow this [guide](https://goo.gl/NPiiyV) to download the data and create the *__news__* database
3. Open a virtual machine shell session by `cd` into the `/vagrant` subdirectory and typing these into your command shell:
`vagrant up`
`vagrant ssh`
4. The `/vagrant` directory is shared between the virtual machine and "your computer" (the system on which the virtual machine is running). Its default __absolute path__ inside the virtual machine is `/vagrant`. Type `cd /vagrant` to locate into this directory.
5. Clone this repository here and `cd` into the git folder
6. Create the required SQL views by typing this into your terminal:
`python3 create-views.py`
or
`python create-views.py` ( _if your default version is Python 3_ )
7. Run the reporting script:
`python3 sql-report.py`
or
`python sql-report.py` ( _if your default version is Python 3_ )

    _**Note:** You can use your favorite text editor to play around with the code outside the virtual machine, as long as all the scripts is kept within the `\vagrant` folder.
## Usage
All Python code is written in Python 3

## SQL Views (for Udacity evaluators)
1. Number of requests for each article title
    ```
    CREATE VIEW article_requests AS
	SELECT articles.title, count(log.path) as requestnum
	FROM log, articles
	WHERE log.path LIKE '%'||articles.slug||'%'
	GROUP BY articles.title
	ORDER BY requestnum DESC;
    ```
2. Number of requests for each author (ID)
    ```
	CREATE VIEW author_requests AS
	SELECT articles.author, count(log.path) AS requestnum
	FROM log, articles
	WHERE log.path LIKE '%'||articles.slug||'%'
	GROUP BY articles.author
	ORDER BY requestnum DESC;
    ```
3. Total number of requests received per day:
    ```
	CREATE VIEW requests_per_day AS
	SELECT DATE_TRUNC('day', time) AS date, count(*)
	FROM log
	GROUP BY date;
    ```
4. Number of erroneous requests per day:
    ```
	CREATE VIEW errors_per_day AS
	SELECT DATE_TRUNC('day', time) AS date, count(*)
	FROM log
	WHERE SUBSTRING(status from 1 for 1) = '4' OR SUBSTRING(status from 1 for 1) = '5'
	GROUP BY date;
    ```

