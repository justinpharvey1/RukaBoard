from flask import Flask, url_for, redirect
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




@app.route('/')
def homepage(): 
  with conn.cursor() as cur: 
    cur.execute("select boardname, ID from boards")
    boards = cur.fetchall()
    return render_template("homepage.html", boards=boards)





@app.route('/votes', methods=['POST'])
def votes():
    if request.method == 'POST':

        print "Vote: ", request.form

        nodeID = request.form['nodeID']

        if request.form['voteType'] == 'upvote':
            with conn.cursor() as cur:
              cur.execute("update nodes set upvotes = upvotes + 1 where id=" + str(nodeID))
              conn.commit()
        if request.form['voteType'] == 'downvote':
            with conn.cursor() as cur:
              cur.execute("update nodes set downvotes = downvotes + 1 where id=" + str(nodeID))
              conn.commit()

    return redirect(url_for('boards'))
        




@app.route('/addResponse', methods=['POST'])
def addResponse():
  if request.method == 'POST':

    #insert new post
    print "\n\nResponse: ", request.form
    with conn.cursor() as cur: 
      cur.execute("insert into nodes (nodetitle, nodetext, boardnumber, nodetype) values ('" + str(request.form['responsetitle']) + "','" + str(request.form['responsetext']) + "'," + str(request.form['boardID']) + ",'" + str(request.form['type']) + "')")
      conn.commit()

    #get ID of new post 
    newChild = ""
    with conn.cursor() as cur: 
      cur.execute("select ID from nodes where nodetitle='" + str(request.form['responsetitle']) + "'")
      newChild = "," + str(cur.fetchone()[0])

    #update node graph with new ID
    with conn.cursor() as cur: 
      print "VALUE TEST: ", str(request.form['nodeID'])
      queryStatement = "update nodes set childnodes=CONCAT(childnodes,'" + newChild + "') where id=" + str(request.form['nodeID'])
      print "query statement: ", queryStatement
      cur.execute(queryStatement)
      conn.commit()

    return redirect(url_for('boards'))





@app.route('/boards')
def boards():
  boardnumber = str(request.args.get('boardnumber', ''))
  currentBoard = 0

  if str(request.args.get('currentboard', '')):
    currentBoard = str(request.args.get('currentboard', ''))


  if not (boardnumber):
    boardnumber = 1


  print "BOARD NUMBER: ", boardnumber

  #Board data
  with conn.cursor() as cur:
    cur.execute("select id, nodetitle, parentnodes, childnodes, upvotes, downvotes, nodetext from nodes where boardnumber=" + str(boardnumber))
  nodes = cur.fetchall()
  print "nodes: ", nodes



  #format the node set
  nodeSet = []
  for node in nodes:
    node = str(node[0]) + ";" + str(node[1])
    nodeSet.append(node)
  print "formatted nodes: ", nodeSet



  #format the node graph
  nodeGraph = []
  for node in nodes:
    print "node : ", node
    if (len(node[3]) > 0): 
      node = str(node[0]) + ";" + str(node[3])
    else: 
      node = "NO CHILDREN"
    nodeGraph.append(node)
  print "formatted nodeGraph: ", nodeGraph


  if currentBoard == 0:
    return render_template('rukaboard.html', boardnumber=boardnumber, nodeSet=nodeSet, nodeGraph=nodeGraph, queryResponse=json.dumps(nodes))

  else: 
    return render_template('rukaboard.html', boardnumber=boardnumber, nodeSet=nodeSet, nodeGraph=nodeGraph, queryResponse=json.dumps(nodes), currentBoard=currentBoard)
 



