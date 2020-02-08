from flask import send_from_directory
from os import path as os_path


def static_resource_routes(app):
    _local_dir = os_path.dirname(os_path.abspath(__file__))
    client_path = os_path.join(_local_dir, '..', '..', 'client')

    @app.route('/js/<path:path>')
    def js_route(path):
        return send_from_directory(os_path.join(client_path, 'js'), path)

    @app.route('/css/<path:path>')
    def css_route(path):
        return send_from_directory(os_path.join(client_path,'css'), path)

    @app.route('/assets/<path:path>')
    def asset_route(path):
        return send_from_directory(os_path.join(client_path,'assets'), path)
