from flask import Flask
from flask import request
from flask import render_template
import requests
import pymysql
import sys
import logging
import json
from urlparse import urlparse
app = Flask(__name__)




#Initialize the database 
#rds settings
rds_host  = "rukadb.c7ypyvkvt80b.us-west-2.rds.amazonaws.com"
name = "masterusername"
password = "masterpassword"
db_name = "RukaDB"




try:
    conn = pymysql.connect(rds_host, user="masterusername", passwd="masterpassword", db="RukaDB", connect_timeout=10)
except:
    print("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()





@app.route('/boards')
def homepage():
  boardnumber = str(request.args.get('boardnumber', ''))

  print "BOARD NUMBER: ", boardnumber

  #Solar data 
  with conn.cursor() as cur:
    cur.execute("select id, nodetext from nodes where boardnumber=" + boardnumber)
  nodes = cur.fetchall()

  print "nodes: ", nodes




  return render_template('rukaboard.html', boardnumber=boardnumber, nodes=json.dumps(nodes))


