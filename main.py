#!/usr/bin/env python
import os
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)

defaults = [
    {
        "name": "first_city",
        "image": "../assets/img/01_drzava.jpg",
        "country": "France",
        "capital": "Paris",
        "difficulty": 1
    },
    {
        "name": "second_city",
        "image": "../assets/img/02_drzava.jpg",
        "country": "Ukraina",
        "capital": "Kijev",
    },
    {
        "name": "third_city",
        "image": "../assets/img/03_drzava.jpg",
        "country": "Hungary",
        "capital": "Budapest",
    }
]


class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html", params={"cities": defaults})


class RezultatHandler(BaseHandler):
    def post(self):

        messages = {}
        messages["errors"] = []
        messages["success"] = []

        for city in defaults:
            input = self.request.get(city["name"])
            if (input.lower() == city["capital"].lower()):
                messages["success"].append("You guessed the capital of %s" % city["country"])
            else:
                messages["errors"].append("You did not guess the capital of %s" % city["country"])

        return self.write(messages)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
], debug=True)
