from flask import render_template, jsonify, request
from app import app, return_200_if_HEAD

import re

from app.extras.bx24 import BX24, Event

# !!! ABSOLUTELY NOT MANDATORY !!! #
"""
Much better is to serve both static and API with nginx in different routes
But this way is faster and easier to bootstrap.
"""
@return_200_if_HEAD
@app.route('/', methods=['POST', 'HEAD', 'GET'])
# Bitrix can use different methods depending on "PLACE"(embedding, main app, after install, mobile)
# And it always checks with HEAD if / and /install are existing
def main(): # App entry point
    try:
        # Your App logic if needed
        bx24 = BX24([request.args['DOMAIN'], request.form['AUTH_ID']]) # Bitrix24 API client
        return render_template('index.html') # Vue App render
    except KeyError:
        # Rejecting, if app invoked outside BX24 environment
        return ("App won't work outside the BX24 Portal.", 200)

@return_200_if_HEAD
@app.route('/install/', methods=['POST', 'GET', 'HEAD'])
# Bitrix can use different methods depending on "PLACE"(embedding, main app, after install, mobile)
# And it always checks with HEAD if / and /install are existing
def install():
    try:
        bx24 = BX24([request.args['DOMAIN'], request.form['AUTH_ID']]) # Bitrix24 API client
        
        # Your Install logic
        # Like setting hooks up
        
        """
            By calling install, BX24 awaits your logic to be done
            and to receive a html-page with JS script, which will
            finish install.
                Check this file at:
                    - public/install_finish.html if ui is built
                    - /ui/public/install_finish.html
        """
        return render_template('install_finish.html')
    except:
        return '', 200

# Hook example
@app.route('/hook', methods=['POST', 'GET'])
def hook():
    bx24 = BX24([
        request.form['auth[domain]'],
        request.form['auth[access_token]']
    ]) # As you can see, hooks have different parameters structure

    # Let's say we have one route for add, update and delete Lead
    # 1. Compiling parser
    # event always looks like this ON<scope><instance><method>,
    # e.g. ONCRMLEADUPDATE -> { scope: crm, instance: lead, method: update }
    pattern = re.compile("ONCRMLEAD(?P<method>DELETE|UPDATE|ADD?)")
    # 2. Parsing event
    match = pattern.match(request.form['event'])
    # 3. This case we're capturing only method, so...
    method = match.groups()[0]

    # 4. In this param("data[FIELDS][ID]") instance ID is stored(usually as string)
    invoice_id = int(request.form['data[FIELDS][ID]'])

    if method in ['ADD', 'UPDATE']:
        pass
    elif method == 'DELETE':
        pass
    else:
        # WTF?
        pass
        # It's not an ad

