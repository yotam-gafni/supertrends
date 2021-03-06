import tornado.httpserver
import tornado.ioloop
import tornado.log
import tornado.web
from pymongo import MongoClient
import datetime
from time import gmtime, strftime
# NOTICE we prefer local_settings over consts
from consts import DBURI
import json


class MainHandler(tornado.web.RequestHandler):
    def get(self, ItemCode):
    	graph_data = []
        client = MongoClient(DBURI) 
        product_name = ""
        coll_data = client.supertrends.supertrends.find({'ItemCode': int(ItemCode)})
        for data_dict in coll_data:
            graph_data.append([data_dict['Time'], data_dict['ItemPrice']])	
            product_name = data_dict['ItemName']
        print graph_data
        self.render("dataOverTime.html", title = "Whatever", graph_data = graph_data, product_name = product_name)

def check_updates():
	pass

if __name__ == "__main__":
    application = tornado.web.Application([
    (r"/(.*)", MainHandler),
    ])
    application.listen(8888)

    task = tornado.ioloop.PeriodicCallback(check_updates, 60 * 60 * 1000)
    task.start()
    tornado.ioloop.IOLoop.instance().start()
