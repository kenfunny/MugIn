import urllib
import webapp2
import jinja2
import os

jinja_environment = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"))

#The front page part
class MainPage(webapp2.RequestHandler):
    # Handler for the MainPage.

    def get(self):
    	template = jinja_environment.get_template('MIHome.html')
    	self.response.out.write(template.render())

#Handler for About page and displaying it.
class AboutPage(webapp2.RequestHandler):

	def get(self):
		template = jinja_environment.get_template('MIAbout.html')
		self.response.out.write(template.render())

class ServicePage(webapp2.RequestHandler):

	def get(self):
		template = jinja_environment.get_template('MIService.html')
		self.response.out.write(template.render())

class ContactPage(webapp2.RequestHandler):

	def get(self):
		template = jinja_environment.get_template('MIContact.html')
		self.response.out.write(template.render())

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/about', AboutPage),
	('/service', ServicePage),
	('/contact', ContactPage),
],debug=True)
