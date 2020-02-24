from flask import request

from client.util.HTMLUtil import HTMLUtil
from experiments.michael.nlu_report import generate_report
from experiments.michael.nly_time_sensitive_report import generate_report as gen_nly_report
from experiments.himesh.historic_sensitivity_report import generate_report as gen_his_sen


def report_routes(app):
    @app.route('/report', methods=['GET'])
    def report():
        report_file = request.args.get('name', default='NOT_FOUND', type=str)
        return HTMLUtil.get_report(report_file)

    @app.route('/report', methods=['POST'])
    def create_new_report():
        report_type = request.json.get('report_type')
        if report_type is None:
            return 'Error, invalid report type', 500

        if report_type == 'NLU':
            title = generate_report()
            return '{"report_title": "/report?name=%s"}' % (title + '.html',)
        elif report_type == 'NLU_Timing':
            title = gen_nly_report()
            return '{"report_title": "/report?name=%s"}' % (title + '.html',)
        elif report_type == 'Historic_Sensitivity':
            title = gen_his_sen()
            return '{"report_title": "/report?name=%s"}' % (title + '.html',)

        return 'Error, invalid report type', 500
