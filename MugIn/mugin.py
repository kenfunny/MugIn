import urllib
import webapp2
import jinja2
import os

from google.appengine.api import users

jinja_environment = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"))

#The front page part
class MainPage(webapp2.RequestHandler):
    # Handler for users not logged in.

    def get(self):
    	template = jinja_environment.get_template('MIHome.html')
        self.response.out.write(template.render())

class MainPageUser(webapp2.RequestHandler):
    # Front page for those logged in

    def get(self):
        user = users.get_current_user()
        if user:  # signed in already
            template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
            }
            template = jinja_environment.get_template('MIHomeUser.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(self.request.host_url)

#The About page part.
class AboutPage(webapp2.RequestHandler):
    #Handler for both users logged in and not logged in.

    def get(self):
        user = users.get_current_user()
        if user:  # signed in already
            template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
            }
            template = jinja_environment.get_template('MIAboutUser.html')
            self.response.out.write(template.render(template_values))
        else: # if not signed in yet
            template = jinja_environment.get_template('MIAbout.html')
            self.response.out.write(template.render())

#The Services page part
class ServicePage(webapp2.RequestHandler):
    #Handler for both users logged in and not logged in.

    def get(self):
        user = users.get_current_user()
        if user:  # signed in already
            template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
            }
            template = jinja_environment.get_template('MIServiceUser.html')
            self.response.out.write(template.render(template_values))
        else: # if not signed in yet
            template = jinja_environment.get_template('MIService.html')
            self.response.out.write(template.render())

#The Contact page part
class ContactPage(webapp2.RequestHandler):
    #Handler for both users logged in and not logged in.

    def get(self):
        user = users.get_current_user()
        if user:  # signed in already
            template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
            }
            template = jinja_environment.get_template('MIContactUser.html')
            self.response.out.write(template.render(template_values))
        else: # if not signed in yet
            template = jinja_environment.get_template('MIContact.html')
            self.response.out.write(template.render())

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/mugin', MainPageUser),
	('/about', AboutPage),
	('/service', ServicePage),
	('/contact', ContactPage),
],debug=True)