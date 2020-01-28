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
