About 
-----

The AWeber API Python Library allows you to quickly get up and running with
integrating access to the AWeber API into your Python applications. This
egg requires the python-oauth2 to handle the authentication.

Installation
============

This egg can be installed by checking out the source::

    $ sudo python setup.py install

Or from Pypi::

    $ easy_install -U aweber_api

Usage
=====

To connect the AWeber API Python Libray, you simply include the main class,
AWeberAPI in your application, then create an instace of it with your 
application's consumer key and secret::

    from aweber import AWeberAPI
    aweber = AWeberAPI(consumer_key, consumer_secret)
    account = aweber.get_account(access_token, token_secret)

    for list in account.lists:
        print list.name


Getting request tokens / access tokens
++++++++++++++++++++++++++++++++++++++

You can also use the AWeberAPI object to handle retrieving request tokens::

    from aweber import AWeberAPI
    aweber = AWeberAPI(consumer_key, consumer_secret)
    request_token, request_token_secret = aweber.get_request_token(callback_url)
    print aweber.authorize_url

As well as access tokens::

    from aweber import AWeberAPI
    aweber = AWeberAPI(consumer_key, consumer_secret)
    aweber.user.verifier = verifier
    aweber.user.request_token = request_token
    aweber.user.token_secret = request_token_secret
    access_token, access_token_secret = aweber.get_access_token()


Full Pylons example
+++++++++++++++++++

Here is a simple Pylons example that uses the AWeber API Python Library to get
a request token, have it authorized, and then print some basic stats about the
web forms in that user's first list::

    from pylons import session, request, tmpl_context as c
    from pylons.controllers.util import redirect 

    from awebertest.lib.base import BaseController, render

    from aweber_api import AWeberAPI

    url = 'http://localhost:5000'
    consumer_key = "vjckgsr5y4gfOa3PWnf"
    consumer_secret = "u3sQ7vGGJBfds4q5dfgsTESi685c5x2wm6gZuIj"
    class DemoController(BaseController):

        def __before__(self):
            self.aweber = AWeberAPI(consumer_key, consumer_secret)

        def index(self):
            token, secret = self.aweber.get_request_token(url+'/demo/get_access')
            session['request_token_secret'] = secret
            session.save()
            redirect(self.aweber.authorize_url)

        def get_access(self):
            self.aweber.user.request_token = request.params['oauth_token']
            self.aweber.user.token_secret = session['request_token_secret']
            self.aweber.user.verifier = request.params['oauth_verifier']
            session['token'], session['secret'] = self.aweber.get_access_token()
            session.save()
            redirect(url+'/demo/show')

        def show(self):
            c.account = self.aweber.get_account(session['token'], session['secret'])
            return render('data.mako')


In `data.mako`::

    <!DOCTYPE html>
    <html lang="en">
        <body>
            <h1>Web Forms</h1>
            % for list in c.account.lists:
            <b>List Id:</b> ${list.id}, name: ${list.name}<br />
            <b>Currently has:</b> ${len(list.web_forms)} web forms
            <ul>
            % for form in list.web_forms:
                <li>Form Id: ${form.id}, name: ${form.name}</li>
            % endfor
            </ul>
            % endfor
        </body>
    </html>
