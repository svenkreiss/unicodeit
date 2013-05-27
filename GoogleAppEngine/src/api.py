# author: Sven Kreiss <sk@svenkreiss.com>

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import unicodeit
import urllib

class Convert(webapp.RequestHandler):
    def get(self, latex):
        latex = urllib.unquote_plus(latex) 
        result = unicodeit.replace([latex])
        self.response.out.write(result[0])


application = webapp.WSGIApplication([
    ('/api/unicodeit/(?P<latex>.*)', Convert)
], debug=True)



def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
