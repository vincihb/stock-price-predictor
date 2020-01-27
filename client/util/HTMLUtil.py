class HTMLUtil:
    @staticmethod
    def wrap_in_tag(data, tag, indent=1):
        start_tag = HTMLUtil.get_indent(indent) + '<' + tag + '>'
        end_tag = '</' + tag + '>'

        return start_tag + str(data) + end_tag

    @staticmethod
    def get_indent(level):
        return '\n' + ('\t' * level)
