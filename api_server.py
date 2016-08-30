import argparse
import cherrypy

import mongo_utils

from json_handler import json_handler

class ApiServer(object):
    def __init__(self):
        self.db = mongo_utils.get_db()
        pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def search(self, keywords, article_format='html', limit=10):
        projection_dict = {"_id": 0}
        if article_format == "html":
            projection_dict.update({'text_summary': 0})
        elif article_format == "text":
            projection_dict.update({'html_summary': 0})
        else:
            raise cherrypy.HTTPError(400, "Invalid article format")
        return list(self.db.news_articles.find({"$text": {"$search": keywords}}, projection_dict).limit(int(limit)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default='8080',
                       help='port the server runs on')
    parser.add_argument('--production', action="store_true",
                        help="specify whether the server runs in production environment or not")
    args = parser.parse_args()
    server_config = {
        'server.socket_port': args.port,
    }
    if args.production:
        server_config['environment'] = 'production'
    else:
        # only use 1 thread for not production environment
        server_config['server.thread_pool'] = 1
    cherrypy.config['tools.json_out.handler'] = json_handler
    cherrypy.config.update(server_config)
    cherrypy.quickstart(ApiServer())