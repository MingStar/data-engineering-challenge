import argparse
import cherrypy

import mongo_utils

from json_handler import json_handler

class ApiServer(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def search(self, keywords, article_format='text', limit=10):
        projection_dict = {"_id": 0}
        if article_format == "html":
            projection_dict.update({'text_summary': 0})
        elif article_format == "text":
            projection_dict.update({'html_summary': 0})
        else:
            raise cherrypy.HTTPError(400, "Invalid article format")
        try:
            limit = int(limit)
        except ValueError:
            raise cherrypy.HTTPError(400, "Invalid value for limit")
        if not (0 < limit <= 100):
            raise cherrypy.HTTPError(400, "Invalid value for limit")
        col = mongo_utils.get_collection()
        cursor = col.find({"$text": {"$search": keywords}}, projection_dict)
        cursor = cursor.limit(limit)
        return list(cursor)

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