import unittest
import json
import SimpleHTTPServer
import SocketServer
import webbrowser
from pandablog.core import Util
import shutil
import os
from jinja2 import FileSystemLoader, Environment, PackageLoader
import codecs

serve_py = """import SimpleHTTPServer
import SocketServer
PORT = 80
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)
try:
	print 'serving at port', PORT
	httpd.serve_forever()
except KeyboardInterrupt:
	print 'exit'
	httpd.socket.close())
"""

sample_author = {
    'url' : 'http://localhost/sample-auothor-archive/',
    'image' : 'http://localhost/assets/twistoy-logo.png',
    'name' : 'TwIStOy',
    'location' : 'Mars',
    'bio' : 'An AC a day, keeps doctor away',
    'website' : 'http://twistoy.com'
}

sample_posts = [
    {
        'content': 'This is a sample content for hello world',
        'title' : 'Hello World',
        'author' : sample_author,
        'next_url' : '#',
        'previous_url' : '#',
        'tags' : [
            {'name' : 'hello', 'url' : 'url-for-hello'},
            {'name' : 'foobar', 'url' : 'url-for-foobar'}
        ],
        'datetime' : 'September 8 2015',
        'url' : 'http://localhost/url-for-this-post/',
        'datetime_url' : 'http://localhost/datetime-archive-for-sep-8-2015',
        'excerpt' : 'This is a brief excerpt'
    },
    {
        'content': 'This is a sample content for hello world',
        'title' : 'Hello World',
        'author' : sample_author,
        'url' : 'http://localhost/url-for-this-post/',
        'next_url' : '#',
        'previous_url' : '#',
        'tags' : [
            {'name' : 'hello', 'url' : 'url-for-hello'},
            {'name' : 'foobar', 'url' : 'url-for-foobar'}
        ],
        'datetime' : 'September 8 2015',
        'datetime_url' : 'http://localhost/datetime-archive-for-sep-8-2015',
        'excerpt' : 'This is a brief excerpt'
    },
    {
        'content': 'This is a sample content for hello world',
        'title' : 'Hello World',
        'url' : 'http://localhost/url-for-this-post/',
        'author' : sample_author,
        'next_url' : '#',
        'previous_url' : '#',
        'tags' : [
            {'name' : 'hello', 'url' : 'url-for-hello'},
            {'name' : 'foobar', 'url' : 'url-for-foobar'}
        ],
        'datetime' : 'September 8 2015',
        'datetime_url' : 'http://localhost/datetime-archive-for-sep-8-2015',
        'excerpt' : 'This is a brief excerpt'
    }
]

parameters = {
    'common' : {
        'site_url' : 'http://localhost/',
        'site_title' : 'Foobar Banzai',
        'asset_path' : 'http://localhost/assets',
        'template_path' : 'http://localhost/template',
        'year' : '2015',
        'image' : '',    # image that display in the header optional
        'title' : '{{Default Title}}',
        'description' : '{{Default Description}}'   # description goes on the header optinoal
    },
    'index' : {
        'site_logo' : '',
        'site_description' : 'Just a foobar blog',
        'posts' : sample_posts
    },
    'post' : sample_posts[0],
    'page' : {
        'content' : 'This is a sample page Content',
        'title' : 'Title for sample page'
    },
    'archive' : {
        'posts' : sample_posts,
        'title' : 'Title for archive',
        'description' : 'The description for the archive'
    }
}

class TestTemplate(unittest.TestCase):

    def setUp(self):
        if not os.path.exists('C:\\output'):
            Util.create_dir('C:\\output')
        if not os.path.exists('C:\\output\\serve.py'):
            with open('C:\\output\serve.py', 'w') as fp:
                fp.write(serve_py)

    def tearDown(self):
        pass

    def _testComponent(self, component):
        env = Environment(loader=PackageLoader('pandablog', 'theme/casper'))
        template = env.get_template(component + '.html')
        arg = dict(parameters['common'].items() + parameters[component].items())
        output = template.render(**arg)
        with codecs.open('C:\\output\\' + component + '.html', "w", encoding='utf-8') as fp:
            fp.write(output)

    def test_all(self):
        for component in ['index', 'post', 'page', 'archive']:
            self._testComponent(component)


if __name__ == '__main__':
    unittest.main()