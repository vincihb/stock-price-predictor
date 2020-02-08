from flask import request

from client.util.HTMLUtil import HTMLUtil


def report_routes(app):
    @app.route('/report')
    def report():
        report_file = request.args.get('name', default='NOT_FOUND', type=str)
        return HTMLUtil.get_report(report_file)
