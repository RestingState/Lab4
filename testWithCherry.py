import cherrypy

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello world 12"

if __name__ == '__main__':
   cherrypy.quickstart(HelloWorld(), '/api/v1/hello-world-12')