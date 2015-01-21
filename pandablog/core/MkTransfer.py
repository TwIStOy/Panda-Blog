# -*- coding:utf-8 -*-
__author__ = 'TwIStOy'

import markdown
import re
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor

class mathjaxSkipBefore(Preprocessor):
    def run(self, lines):
        new_lines = []
        small = re.compile(r'\\\((.*?)\\\)')
        big = re.compile(r'\\\[(.*?)\\\]')
        for line in lines:
            line = small.sub(r'<code class="mathjaxSkipSmall">\1</code>', line)
            line = big.sub(r'<code class="mathjaxSkipBig">\1</code>', line)
            new_lines.append(line)
        return new_lines


class mathjaxSkipAfter(Postprocessor):
    def run(self, text):
        rv = []
        small = re.compile(r'<code class="mathjaxSkipSmall">(.*?)</code>')
        big = re.compile(r'<code class="mathjaxSkipBig">(.*?)</code>')
        for line in text.split('\n'):
            line = small.sub(r'\\(\1\\)', line)
            line = big.sub(r'\\[\1\\]', line)
            rv.append(line)
        return "\n".join(rv)


class codeHighLight(Postprocessor):
    def run(self, text):
        language = re.compile(r'<code>(.*?)\n')
        print re.findall(language, text)
        return language.sub(r'<code class="\1 syntax-highlight">', text)


from markdown.extensions import Extension


class mathjaxExtension(Extension):
    def __init__(self, configs={}):
        self.config = configs

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)

        md.preprocessors.add('mathjax_skip_before', mathjaxSkipBefore(), '<normalize_whitespace')
        md.postprocessors.add('mathjax_skip_after', mathjaxSkipAfter(), '>unescape')
        md.postprocessors.add('codeHighLight', codeHighLight(), '_end')

ext = mathjaxExtension()


def convert(text):
    return markdown.markdown(text, extensions=[ext])


if __name__ == '__main__':
    text = '''# asdfasdf\\(x_i + x_1\\)\n## \\[\sum\\]\n```python\nprint a```'''
    print convert(text)
