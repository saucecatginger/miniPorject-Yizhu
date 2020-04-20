from flask import Flask, render_template, request, jsonify
import json
import requests
import requests_cache

requests_cache.install_cache('eq_api_cache', backend='sqlite', expire_after=36000)

app = Flask(__name__)

eq_url_template = 'https://apis.is/earthquake/is'


@app.route('/eq', methods=['GET'])
def geteq():
    my_latitude = request.args.get('lat','63.976')
    my_longitude = request.args.get('lng','-21.949')
    my_depth = request.args.get('depth','1.1')
    eq_url = eq_url_template.format(lat = my_latitude, lng = my_longitude, depth = my_depth)
    resp = requests.get(eq_url)
    
    if resp.ok:
        return jsonify(resp.json())
    else:
        print(resp.reason)

if __name__=="__main__":
    app.run(host='0.0.0.0')
