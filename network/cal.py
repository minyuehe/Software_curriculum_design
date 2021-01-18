import json
import time
import random
import networkx as nx
from networkx.readwrite import json_graph
import pymysql
from flask import jsonify,request

def avggene(gene):
    
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
    cur.execute('select * from jsondata where generation=%d' %gene)
    mydata = cur.fetchall()
    mydata = mydata[0][1]
    mydata = json.loads(mydata)
    G = json_graph.node_link_graph(mydata)

    avg_degree=calavgdegree(G)
    avg_path=calavgpath(G)
    avg_cluster=calavgcluster(G)
    histogramtostr=calhistogram(G)

    tsql  =  "insert into graphcaldata(avgdegree,avgpath,avgcluster,generation) values(%f,%f,%f,%d)" %(avg_degree,avg_path,avg_cluster,gene)
    cur.execute(tsql)
    
    tsql2 = "update graphcaldata set histogram='"+histogramtostr+"' where generation=%d" %(gene)
    cur.execute(tsql2)
    conn.commit()


def calhistogram(G):
    degree_list=list(nx.degree_histogram(G))
    histogramtostr= str(degree_list)
    #print(histogramtostr)
    return histogramtostr



def calavgdegree(G):
        
    degree_list=list(nx.degree_histogram(G))
    #print(degree_list)
    avg_degree=0
    for i in range(len(degree_list)):
        avg_degree += i*(degree_list[i])
    avg_degree=avg_degree / G.number_of_nodes()
    return avg_degree


def calavgpath(G):
    degree_list=list(nx.degree_histogram(G))
    if (degree_list[0]==0):
        try:
            avg_path=nx.average_shortest_path_length(G)
        except:
            print('bug')
            avg_path= 999
    else:
        avg_path= 999
    return avg_path


def calavgcluster(G):  
    avg_cluster=nx.average_clustering(G)
    return avg_cluster



def last_json(last_jsondata,last_graphdata,last_nodedata):

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
    
    # cur.execute('select * from jsondata order by id desc limit 1')
    # data1 = cur.fetchall()
    # maxgen = data1[0][2]
    # lastdata = data1[0][1]
    #maxgen =last_jsondata[0][2]
    lastdata =last_jsondata[0][1]

    lastdata = '{"series":[{"type":"graph","layout":"force","roam":true,"force":{"repulsion":200},"draggable":true,'+lastdata[1:]
    lastdata = lastdata+']}'
    
    #cur.execute('select * from graphcaldata order by generation desc limit 1')
    #graphdata = cur.fetchall()
    graphdata=last_graphdata

    last_avgdegree= graphdata[0][0]
    last_avgpath= graphdata[0][1]
    last_avgcluster= graphdata[0][2]
    last_histogram= graphdata[0][4]
    last_strtojson=json.loads(lastdata)


    #cur.execute('select * from nodedata where generation=%d'%(maxgen))
    #nodedata = cur.fetchall()
    nodedata = last_nodedata
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

    return jsonify(avg_degree=last_avgdegree,avg_path=last_avgpath,avg_cluster=last_avgcluster,json_str=last_strtojson,histogramtostr=last_histogram)



def WRnode(gene):
        
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
        cur = conn.cursor()
        cur.execute('select * from jsondata where generation=%d' %gene)
        mydata = cur.fetchall()
        mydata = mydata[0][1]
        mydata = json.loads(mydata)
        G = json_graph.node_link_graph(mydata)

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
            tsql  =  "insert into nodedata(generation,nodeid,degree,betweeness,closeness,eigenvector,katz,cluster,triangle) values(%d,%d,%d,%f,%f,%f,%f,%f,%d)"%(gene,node_id,id_degree,id_betweeness,id_closeness,id_eigenvector,id_katz,id_cluster,id_triangle)
            cur.execute(tsql)

        conn.commit()