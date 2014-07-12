import urllib
import webapp2
import jinja2
import os
import datetime

from google.appengine.ext import ndb
from google.appengine.api import users

jinja_environment = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"),
    extensions = ['jinja2.ext.autoescape'],
    autoescape =True)


DEFAULT_CHAT_NAME = 'admin_book'

def chatbook_key(chatbook_name=DEFAULT_CHAT_NAME):
    return ndb.Key('Chatbook', chatbook_name)

class Greeting(ndb.Model):
    """Models an individual Chatbook entry."""
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

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
                'user_mail': users.get_current_user().nickname(),
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
                'user_mail': users.get_current_user().nickname(),
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
                'user_mail': users.get_current_user().nickname(),
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
                'user_mail': users.get_current_user().nickname(),
                'logout': users.create_logout_url(self.request.host_url),
            }
            template = jinja_environment.get_template('MIContactUser.html')
            self.response.out.write(template.render(template_values))
        else: # if not signed in yet
            template = jinja_environment.get_template('MIContact.html')
            self.response.out.write(template.render())

class Chatlist(webapp2.RequestHandler):
    def get(self):
        chatbook_name = self.request.get('chatbook_name',
                                          DEFAULT_CHAT_NAME)
        greetings_query = Greeting.query(
            ancestor=chatbook_key(chatbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        template_values = {
            'user_mail': users.get_current_user().nickname(),
            'logout': users.create_logout_url(self.request.host_url),
            'greetings': greetings,
            'chatbook_name': urllib.quote_plus(chatbook_name),
            'img_src': '../images/' + chatbook_name + '.jpg',
        }

        template = jinja_environment.get_template('ChatList.html')
        self.response.write(template.render(template_values))

class Chatbook(webapp2.RequestHandler):
    def post(self):
        chatbook_name = self.request.get('chatbook_name',
                                          DEFAULT_CHAT_NAME)
        greeting = Greeting(parent=chatbook_key(chatbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'chatbook_name': chatbook_name}
        self.redirect('/chats?' + urllib.urlencode(query_params))

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/mugin', MainPageUser),
	('/about', AboutPage),
	('/service', ServicePage),
	('/contact', ContactPage),
    ('/chats', Chatlist),
    ('/sign', Chatbook),
],debug=True)