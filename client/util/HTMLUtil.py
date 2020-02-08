from os import path


class HTMLUtil:
    @staticmethod
    def wrap_in_tag(data, tag, indent=1, attributes=None, one_line=True):
        if attributes is None:
            attributes = {}

        start_tag = HTMLUtil.get_indent(indent) + '<' + tag + HTMLUtil._resolve_attrs(attributes) + '>'
        if one_line:
            end_tag = '</' + tag + '>'
        else:
            end_tag = HTMLUtil.get_indent(indent) + '</' + tag + '>'

        return start_tag + str(data) + end_tag

    @staticmethod
    def get_indent(level):
        return '\n' + ('\t' * level)

    @staticmethod
    def _resolve_attrs(attributes):
        attrs = ''
        if attributes is not None:
            for key in attributes:
                attrs += ' ' + str(key) + '="' + str(attributes[key]) + '"'

        return attrs

    @staticmethod
    def get_template(template_name):
        _local_dir = path.dirname(path.abspath(__file__))
        file_path = path.join(_local_dir, '..', 'template', template_name)
        with open(file_path) as template:
            return template.read()

    @staticmethod
    def get_report(report_name):
        _local_dir = path.dirname(path.abspath(__file__))
        file_path = path.join(_local_dir, '..', 'compiled', report_name)
        with open(file_path) as template:
            return template.read()

