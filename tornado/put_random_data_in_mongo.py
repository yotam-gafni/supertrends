from pymongo import MongoClient
from consts import DBURI
data = [ {'day_date' : '13', 'price_data': 5},
	 {'day_date' : '14', 'price_data': 6},
	 {'day_date' : '15', 'price_data': 3},
	 {'day_date' : '16', 'price_data': 2}]


if __name__ == "__main__":
        client = MongoClient(DBURI) 
	for data_unit in data:
		client.supertrends.supertrends.insert(data_unit)
