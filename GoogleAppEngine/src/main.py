#!/usr/bin/env python
#
# author: Sven Kreiss <sk@svenkreiss.com>

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
import os


class MainHandler(webapp.RequestHandler):
    def get(self):
        template_values = {}
        
       if self.request.get('expr') is not None:
            template_values['expression'] = self.request.get('expr') 
        
        path = os.path.join(os.path.dirname(__file__), 'templates/base.html')
        self.response.out.write(template.render(path, template_values))



def main():
    application = webapp.WSGIApplication([
        ('/', MainHandler)
    ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

