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
    cur.execute("select id, nodetext, parentnodes, childnodes from nodes where boardnumber=" + boardnumber)
  nodes = cur.fetchall()

  print "nodes: ", nodes



  #format the node set
  nodeSet = []

  for node in nodes:
    node = str(node[0]) + ";" + str(node[1])
    nodeSet.append(node)

  print "formatted nodes: ", nodeSet





  nodeGraph = []
  for node in nodes:
    print "node : ", node
    if (len(node[3]) > 0): 
      node = str(node[0]) + ";" + str(node[3])
    else: 
      node = "NO CHILDREN"
    nodeGraph.append(node)

  print "formatted nodeGraph: ", nodeGraph




  return render_template('rukaboard.html', boardnumber=boardnumber, nodeSet=nodeSet, nodeGraph=nodeGraph)




