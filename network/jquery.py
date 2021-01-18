# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request
import json
import time
import random
import networkx as nx
from networkx.readwrite import json_graph
import pymysql
import numpy as np
import cal
from disablefuction import *
from netcreatefuction import *

#client = MongoClient()
#db = client['test-database']




disablecurrent_gen=0
current_gen=0
last_jsondata=0
last_graphdata=0
last_nodedata=0

app = Flask(__name__)

@app.route("/")
def index():
# 主页面
    return render_template("index.html")


@app.route("/er.html")
def er_index():
    return render_template('er.html')

@app.route("/ws.html")
def ws_index():
    return render_template('ws.html')

@app.route("/ba.html")
def ba_index():
    return render_template('ba.html')

@app.route("/file.html")
def file_index():
    return render_template('file.html')

   

@app.route("/readFile")
def readFile():
    jsonFile = request.args.get('a')
    #jsonFile = json.dumps(jsonFile)
    #jsonFile = str(jsonFile)
    print(type(jsonFile))

    strtojson = json.loads(jsonFile)

    G = json_graph.node_link_graph(strtojson)
    histogram=cal.calhistogram(G)
    avgdegree = cal.calavgdegree(G)
    avgpath = cal.calavgpath(G)
    avgcluster = cal.calavgcluster(G)

    #strtojson = json.loads(jsonFile)
    jsonFile = '{"series":[{"type":"graph","layout":"force","roam":true,"force":{"repulsion":200},"draggable":true,"focusNodeAdjacency":true,"lineStyle":{"width":3,"color":"#000"},'+jsonFile[1:]
    jsonFile = jsonFile+']}'
 
    strtojson = json.loads(jsonFile)




    num_node=G.number_of_nodes()
    
    bc=nx.betweenness_centrality(G)
    cc=nx.closeness_centrality(G)
    try:
        ec=nx.eigenvector_centrality(G,max_iter=1000)
    except:
        ec={}
        for i in range(num_node):
            ec[i]=0
        print('bbbbbug')
        print(gene)
        
    kc=nx.katz_centrality(G)

    
    for n in range(G.number_of_nodes()):
        node_id=n
        id_degree=G.degree(n)
        id_betweeness=bc[n]
        id_closeness=cc[n]
        id_eigenvector=ec[n]
        id_katz=kc[n]

        id_cluster= nx.clustering(G,n)
        id_triangle= nx.triangles(G,n)


        fuck1={}
        fuck2={}
        fuck1['formatter']='id: %d\n------------------------\ndegreee: %d\nbetweeness: %f\ncloseness: %f\neigenvector: %f\nkatz: %f\ncluster: %f\ntriangle: %d'%(n,id_degree,id_betweeness,id_closeness,id_eigenvector,id_katz,id_cluster,id_triangle)
        fuck1['align']='left'
        fuck1['position']='right'
        fuck1['color']= "rgba(255, 255, 255, 1)"
        fuck1['backgroundColor']= "rgba(0, 0, 0, 0.7)"
        fuck1['fontSize']= "14"
        fuck1['padding']= 5
        fuck1['borderRadius']= 10
        fuck2['label']=fuck1
        strtojson['series'][0]['nodes'][n]['emphasis']=fuck2









    return jsonify(avg_degree=avgdegree,avg_path=avgpath,avg_cluster=avgcluster,json_str=strtojson,histogramtostr=histogram)



@app.route('/er_submit')
def er_submit():
    global current_gen
    global disablecurrent_gen
    current_gen =0
    disablecurrent_gen=0


    NETWORK_SIZE = request.args.get('a', 0, type=int)
    PROBABILITY_OF_EAGE = request.args.get('b', 0, type=float)
    
    WR_erdos_renyi_graph(NETWORK_SIZE,PROBABILITY_OF_EAGE)
    

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
    cur.execute('select * from jsondata order by id desc limit 1')
    mydata = cur.fetchall()
    maxgene = mydata[0][2]

    i=1
    while(i<=maxgene):
        cal.avggene(i)
        cal.WRnode(i)
        i=i+1


    # conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    # cur = conn.cursor()
    
    # cur.execute('select * from jsondata order by id desc limit 1')
    # data1 = cur.fetchall()
    # maxgen = data1[0][2]
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
    
    cur.execute('select * from graphcaldata order by generation desc limit 1')
    graphdata = cur.fetchall()

    cur.execute('select * from nodedata where generation=%d'%maxgene)
    nodedata = cur.fetchall()


    global last_jsondata
    last_jsondata=mydata
    global last_graphdata
    last_graphdata=graphdata
   
    global last_nodedata
    last_nodedata=nodedata

    return jsonify('submit success !')







@app.route('/ws_submit')
def ws_submit():
    global current_gen
    global disablecurrent_gen
    current_gen =0
    disablecurrent_gen=0


    n = request.args.get('a', 0, type=int)
    k = request.args.get('b', 0, type=int)
    p = request.args.get('c', 0, type=float)
    WR_watts_strogatz_graph(n,k,p)


    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
    cur.execute('select * from jsondata order by id desc limit 1')
    mydata = cur.fetchall()
    maxgene = mydata[0][2]

    i=1
    while(i<=maxgene):
        cal.avggene(i)
        cal.WRnode(i)
        i=i+1

    
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()

    cur.execute('select * from graphcaldata order by generation desc limit 1')
    graphdata = cur.fetchall()

    cur.execute('select * from nodedata where generation=%d'%maxgene)
    nodedata = cur.fetchall()


    global last_jsondata
    last_jsondata=mydata
    global last_graphdata
    last_graphdata=graphdata
   
    global last_nodedata
    last_nodedata=nodedata

    return jsonify('submit success !')


    


@app.route('/ba_submit')
def ba_submit():
    global current_gen
    global disablecurrent_gen
    current_gen =0
    disablecurrent_gen=0

   

    n = request.args.get('a', 0, type=int)
    m = request.args.get('b', 0, type=int)
    WR_barabasi_albert_graph(n, m)


    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
    cur.execute('select * from jsondata order by id desc limit 1')
    mydata = cur.fetchall()
    maxgene = mydata[0][2]

    i=1
    while(i<=maxgene):
        cal.avggene(i)
        cal.WRnode(i)
        i=i+1




    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
    cur.execute('select * from graphcaldata order by generation desc limit 1')
    graphdata = cur.fetchall()

    cur.execute('select * from nodedata where generation=%d'%maxgene)
    nodedata = cur.fetchall()

    global last_jsondata
    last_jsondata=mydata
    global last_graphdata
    last_graphdata=graphdata
   
    global last_nodedata
    last_nodedata=nodedata

    
    return jsonify('submit success !')













@app.route('/update')
def update():


    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
    
    cur.execute('select * from jsondata order by id desc limit 1')
    data1 = cur.fetchall()
    maxgen = data1[0][2]
    lastdata = data1[0][1]

    lastdata = '{"series":[{"type":"graph","layout":"force","force":{"repulsion":200},'+lastdata[1:]
    lastdata = lastdata+']}'
    
    cur.execute('select * from graphcaldata order by generation desc limit 1')
    graphdata = cur.fetchall()

    cur.execute('select * from nodedata where generation=%d'%maxgen)
    nodedata = cur.fetchall()
    id_num=len(nodedata)
    
        
   
    last_avgdegree= graphdata[0][0]
    last_avgpath= graphdata[0][1]
    last_avgcluster= graphdata[0][2]
    last_histogram= graphdata[0][4]
    last_strtojson=json.loads(lastdata)

   
    for i in range(id_num):
        fuck1={}
        fuck2={}
        fuck1['formatter']='id: %d\n------------------------\ndegreee: %d\nbetweeness: %f\ncloseness: %f\neigenvector: %f\nkatz: %f\ncluster: %f\ntriangle: %d'%(nodedata[i][1],nodedata[i][2],nodedata[i][3],nodedata[i][4],nodedata[i][5],nodedata[i][6],nodedata[i][7],nodedata[i][8])
        fuck1['align']='left'
        fuck1['position']='right'
        fuck1['color']= "rgba(255, 255, 255, 1)"
        fuck1['backgroundColor']= "rgba(0, 0, 0, 0.7)"
        fuck1['fontSize']= "14"
        fuck1['borderRadius']= 10
        fuck1['padding']= 5
        fuck2['label']=fuck1
        last_strtojson['series'][0]['nodes'][i]['emphasis']=fuck2
        
       
    global current_gen
    current_gen +=1
    
    global last_jsondata
    last_jsondata=data1
    global last_graphdata
    last_graphdata=graphdata
    global last_nodedata
    last_nodedata=nodedata



    if(current_gen<=maxgen):
        
        cur = conn.cursor()
        cur.execute('select * from jsondata where generation=%d'%(current_gen))
        mydata = cur.fetchall()
        mydata = mydata[0][1]
        mydata = '{"series":[{"type":"graph","layout":"circular","roam":true,"focusNodeAdjacency":true,"lineStyle":{"width":3,"color":"#000"},'+mydata[1:]
        mydata = mydata+']}'

        
        cur.execute('select * from graphcaldata where generation=%d'%(current_gen))
        graphdata = cur.fetchall()
        cur.execute('select * from nodedata where generation=%d'%(current_gen))
        nodedata = cur.fetchall()

        id_num2=len(nodedata)
        print(id_num2)

        avgdegree= graphdata[0][0]
        avgpath= graphdata[0][1]
        avgcluster= graphdata[0][2]
        histogram= graphdata[0][4]
        strtojson=json.loads(mydata)

        for i in range(id_num2):
            fuck1={}
            fuck2={}
            fuck1['formatter']='id: %d\n------------------------\ndegreee: %d\nbetweeness: %f\ncloseness: %f\neigenvector: %f\nkatz: %f\ncluster: %f\ntriangle: %d'%(nodedata[i][1],nodedata[i][2],nodedata[i][3],nodedata[i][4],nodedata[i][5],nodedata[i][6],nodedata[i][7],nodedata[i][8])
            fuck1['align']='left'
            fuck1['position']='right'
            fuck1['color']= "rgba(255, 255, 255, 1)"
            fuck1['backgroundColor']= "rgba(0, 0, 0, 0.7)"
            fuck1['fontSize']= "14"
            fuck1['padding']= 5
            fuck1['borderRadius']= 10
            fuck2['label']=fuck1
            strtojson['series'][0]['nodes'][i]['emphasis']=fuck2
            print(i)
      
        

        return jsonify(avg_degree=avgdegree,avg_path=avgpath,avg_cluster=avgcluster,json_str=strtojson,histogramtostr=histogram)
   
        
    else:
        
        return jsonify(avg_degree=last_avgdegree,avg_path=last_avgpath,avg_cluster=last_avgcluster,json_str=last_strtojson,histogramtostr=last_histogram)


@app.route('/last')
def er_last():
    global last_graphdata
    global last_jsondata
    global last_nodedata
    print(last_graphdata)
    return cal.last_json(last_jsondata,last_graphdata,last_nodedata)








@app.route('/degree')
def er_remove():
    
    global current_gen
    global disablecurrent_gen
    global last_jsondata
    current_gen =0
    disablecurrent_gen=0

    WR_degreedisable(last_jsondata)

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
    cur.execute('select * from jsondata order by id desc limit 1')
    mydata = cur.fetchall()
    maxgene = mydata[0][2]

    i=1
    while(i<=maxgene):
        cal.avggene(i)
        cal.WRnode(i)
        i=i+1

    return jsonify('submit success')




@app.route('/between')
def between():
    global current_gen
    global disablecurrent_gen
    global last_jsondata
    current_gen =0
    disablecurrent_gen=0
    WR_betweenessdisable(last_jsondata)
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
    cur.execute('select * from jsondata order by id desc limit 1')
    mydata = cur.fetchall()
    maxgene = mydata[0][2]

    i=1
    while(i<=maxgene):
        cal.avggene(i)
        cal.WRnode(i)
        i=i+1

    return jsonify('submit success')


@app.route('/close')
def close():
    global current_gen
    global disablecurrent_gen
    global last_jsondata
    current_gen =0
    disablecurrent_gen=0
    WR_closenessdisable(last_jsondata)
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
    cur.execute('select * from jsondata order by id desc limit 1')
    mydata = cur.fetchall()
    maxgene = mydata[0][2]

    i=1
    while(i<=maxgene):
        cal.avggene(i)
        cal.WRnode(i)
        i=i+1

    return jsonify('submit success')

@app.route('/vector')
def vector():
    global current_gen
    global disablecurrent_gen
    global last_jsondata
    current_gen =0
    disablecurrent_gen=0
    WR_eigenvectordisable(last_jsondata)
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
    cur.execute('select * from jsondata order by id desc limit 1')
    mydata = cur.fetchall()
    maxgene = mydata[0][2]

    i=1
    while(i<=maxgene):
        cal.avggene(i)
        cal.WRnode(i)
        i=i+1

    return jsonify('submit success')


@app.route('/katz')
def katz():
    global current_gen
    global disablecurrent_gen
    global last_jsondata
    current_gen =0
    disablecurrent_gen=0
    WR_katzdisable(last_jsondata)
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
    cur.execute('select * from jsondata order by id desc limit 1')
    mydata = cur.fetchall()
    maxgene = mydata[0][2]

    i=1
    while(i<=maxgene):
        cal.avggene(i)
        cal.WRnode(i)
        i=i+1

    return jsonify('submit success')




@app.route('/show_remove')
def er_show_remove():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
    
    cur.execute('select * from jsondata order by id desc limit 1')
    data1 = cur.fetchall()
    maxgen = data1[0][2]
    lastdata = data1[0][1]

    lastdata = '{"series":[{"type":"graph","layout":"circular","roam":true,"focusNodeAdjacency":true,"lineStyle":{"width":3,"color":"#000"},'+lastdata[1:]
    lastdata = lastdata+']}'
    
    cur.execute('select * from graphcaldata order by generation desc limit 1')
    graphdata = cur.fetchall()

    last_avgdegree= graphdata[0][0]
    last_avgpath= graphdata[0][1]
    last_avgcluster= graphdata[0][2]
    last_histogram= graphdata[0][4]
    last_strtojson=json.loads(lastdata)


    cur.execute('select * from nodedata where generation=%d'%(maxgen))
    nodedata = cur.fetchall()
    id_num=len(nodedata)
    for i in range(id_num):
        fuck1={}
        fuck2={}
        fuck1['formatter']='id: %d\n------------------------\ndegreee: %d\nbetweeness: %f\ncloseness: %f\neigenvector: %f\nkatz: %f\ncluster: %f\ntriangle: %d'%(nodedata[i][1],nodedata[i][2],nodedata[i][3],nodedata[i][4],nodedata[i][5],nodedata[i][6],nodedata[i][7],nodedata[i][8])
        fuck1['align']='left'
        fuck1['position']='right'
        fuck1['color']= "rgba(255, 255, 255, 1)"
        fuck1['backgroundColor']= "rgba(0, 0, 0, 0.7)"
        fuck1['fontSize']= "14"
        fuck1['padding']= 5
        fuck1['borderRadius']= 10
        fuck2['label']=fuck1
        last_strtojson['series'][0]['nodes'][i]['emphasis']=fuck2


    #lastdata = json.loads(lastdata)
    global disablecurrent_gen
    disablecurrent_gen +=1
    
    if(disablecurrent_gen<=maxgen):
        
        cur = conn.cursor()
        cur.execute('select * from jsondata where generation=%d'%(disablecurrent_gen))
        mydata = cur.fetchall()
        mydata = mydata[0][1]
        mydata = '{"series":[{"type":"graph","layout":"circular","roam":true,"focusNodeAdjacency":true,"lineStyle":{"width":3,"color":"#000"},'+mydata[1:]
        mydata = mydata+']}'
        
        cur.execute('select * from graphcaldata where generation=%d'%(disablecurrent_gen))
        graphdata = cur.fetchall()

        avgdegree= graphdata[0][0]
        avgpath= graphdata[0][1]
        avgcluster= graphdata[0][2]
        histogram= graphdata[0][4]
        strtojson=json.loads(mydata)


        cur.execute('select * from nodedata where generation=%d'%(disablecurrent_gen))
        nodedata = cur.fetchall()
        id_num=len(nodedata)
        for i in range(id_num):
            fuck1={}
            fuck2={}
            fuck1['formatter']='id: %d\n------------------------\ndegreee: %d\nbetweeness: %f\ncloseness: %f\neigenvector: %f\nkatz: %f\ncluster: %f\ntriangle: %d'%(nodedata[i][1],nodedata[i][2],nodedata[i][3],nodedata[i][4],nodedata[i][5],nodedata[i][6],nodedata[i][7],nodedata[i][8])
            fuck1['align']='left'
            fuck1['position']='right'
            fuck1['color']= "rgba(255, 255, 255, 1)"
            fuck1['backgroundColor']= "rgba(0, 0, 0, 0.7)"
            fuck1['fontSize']= "14"
            fuck1['padding']= 5
            fuck1['borderRadius']= 10
            fuck2['label']=fuck1
            strtojson['series'][0]['nodes'][i]['emphasis']=fuck2



        return jsonify(avg_degree=avgdegree,avg_path=avgpath,avg_cluster=avgcluster,json_str=strtojson,histogramtostr=histogram)
        
    else:
        
        return jsonify(avg_degree=last_avgdegree,avg_path=last_avgpath,avg_cluster=last_avgcluster,json_str=last_strtojson,histogramtostr=last_histogram)













    
if __name__=="__main__":
    app.run(host = "0.0.0.0",port = 5000, debug = True)
