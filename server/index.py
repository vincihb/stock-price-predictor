from flask import Flask
from server.routes.static_resources import static_resource_routes
from server.routes.index import index_routes
from server.routes.report import report_routes

app = Flask(__name__)
static_resource_routes(app)
index_routes(app)
report_routes(app)

if __name__ == '__main__':
    app.run(port=5050)
