# GoogleSearch
Development Assignment:
· Create a tool that crawls google for user-inputted search terms
· Save the first 20 results returned
· Visit each of the result pages and store any information you think could or would be useful
· Display the information in some way that will be useful for a user
 
Use Python 2.7 (libraries and frameworks are welcome)
Store data in MySQL (or MongoDB)


##Dependecies needed
The following python libraries are needed

* BeautifulSoup4
* requests
* 
yum install MySQL-python

###Installing dependencies
```bash
pip install bs4
pip install requests

#if using Yellowdog Updater, Modified
yum install MySQL-python

#if using Advanced Packaging Tool
apt-get install MySQL-python
```


##Database
The database must be created, in my case I used a local MySQL database
You must import the provided database.sql 
Change the database credentials 
```
host = '127.0.0.1'
user = 'root'
password = 'password'
```

##Running the script
```bash
python main.py
```
