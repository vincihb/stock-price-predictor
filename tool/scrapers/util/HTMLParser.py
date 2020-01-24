from subprocess import run, PIPE

GET_LAST_LINE = 'tail -n 1'
REMOVE_TAGS = 'sed -e "s/<[^>]*>//g"'
PIPE_CHAR = " | "


class HTMLParser:
    @staticmethod
    def grep_for(input_text, search, following=0):
        grep = "grep '$$$$' -A ####".replace('$$$$', search).replace('####', str(following))
        command = grep + PIPE_CHAR + GET_LAST_LINE + PIPE_CHAR + REMOVE_TAGS
        out = run(command, shell=True, input=input_text, stdout=PIPE, encoding='utf-8')
        return out.stdout.strip()
