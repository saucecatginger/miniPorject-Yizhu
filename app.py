#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 23:47:06 2020

@author: yizhu
"""

from flask import Flask, request, render_template, jsonify
from cassandra.cluster import Cluster

import json
import requests
import requests_cache

cluster = Cluster(contact_points=['172.17.0.2'],port=9042)
session = cluster.connect()

requests_cache.install_cache('eq_api_cache', backend='sqlite', expire_after=36000)

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name")
    return('<h1>Hello, {}, here to check some earthquake?</h1>'.format(name))

# return all earthquakes and show their ID, latitude, and longitude
@app.route('/earthquake', methods=['GET'])
def profile():
    rows = session.execute("""Select * From useq.stats""")
    result = []
    for r in rows:
        result.append({"id":r.ID,"latitude":r.latitude,"longitude":longitude})
    return jsonify(result)

# return earthquake by its ID
@app.route('/earthquake/<id>', methods=['GET'])
def search(id):
    rows = session.execute( """Select * From useq.stats 
                           where id = '{}'""".format(id))
    for eq in rows:
        return('<h1>{} - latitude: {}, longtitude: {}</h1>'.format(id, eq.latitude, eq.longtitude))
    return('<h1>That earthquake does not exist!</h1>')

# return earthquake by its MMI
@app.route('/eqmmi/<mmi>', methods=['GET'])
def getbymmi(mmi):
    eq_url_template = 'https://api.geonet.org.nz/quake?MMI={mmi}'
    
    my_mmi = mmi

    eq_url = eq_url_template.format(mmi = my_mmi)
    resp = requests.get(eq_url)
    
    if resp.ok:
        return jsonify(resp.json())
    else:
        print(resp.reason)

#return earthquake by its publicID        
@app.route('/eqid/<publicID>', methods=['GET'])
def getbyid(publicID):
    eq_url_template = 'https://api.geonet.org.nz/quake/{publicID}'
    
    my_id = publicID
    
    eq_url = eq_url_template.format(publicID = my_id)
    resp = requests.get(eq_url)
    
    if resp.ok:
        return jsonify(resp.json())
    else:
        print(resp.reason)

# post a new earthquake
@app.route('/eqrecords', methods=['POST'])
def create():
    session.execute("""INSERT INTO useq.stats (id) VALUES ('{}')""".format(request.json['id']))
    return jsonify({'message': 'created: /eqrecords/{}'.format(request.json['id'])}), 201

# update an exisiting earthquake
@app.route('/eqrecords', methods=['PUT'])
def update():
    session.execute("""UPDATE useq.stats SET latitude = {} WHERE id = '{}'""".format(float(request.json['latitude']),request.json['id']))
    return jsonify({'message': 'updated: /eqrecords/{}'.format(request.json['id'])}), 200

# delete an earthquake record
@app.route('/eqrecords', methods=['DELETE'])
def delete():
    session.execute("""DELETE FROM useq.stats WHERE id = '{}'""".format(request.json['id']))
    return jsonify({'message': 'deleted: /eqrecords/{}'.format(request.json['id'])}), 200

if __name__=="__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
