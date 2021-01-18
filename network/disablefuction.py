# -*- coding: utf-8 -*-
"""
Created on 2020/12/24
"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import json
import pymysql
import flask
from networkx.readwrite import json_graph

#函数功能说明

# WR_degreedisable() 度失效当前数据库jsondata最大generation图，清除jsondata之前的数据，并写入新的失效数据
# WR_betweenessdisable 中介中心性失效当前数据库jsondata最大generation图，清除jsondata之前的数据，并写入新的失效数据
# WR_closenessdisable() 接近中心性失效当前数据库jsondata最大generation图，清除jsondata之前的数据，并写入新的失效数据
# WR_eigenvectordisable() 特征向量中心性失效当前数据库jsondata最大generation图，清除jsondata之前的数据，并写入新的失效数据
# WR_katzdisable() katz中心性失效当前数据库jsondata最大generation图，清除jsondata之前的数据，并写入新的失效数据

def WR_degreedisable(last_jsondata):
    def GraphWRMysql(G):
        d = json_graph.node_link_data(G)  # node-link format to serialize
        d_json = json.dumps(d)
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
        cur = conn.cursor()
        tsql  =  "insert into jsondata(json_data) values('{json}')"
        sql = tsql.format(json=pymysql.escape_string(d_json))
        cur.execute(sql)

        cur.execute('select * from jsondata order by id desc limit 1')
        iddata = cur.fetchall()
        iddata = iddata[0][0]
        #print(iddata) 
        tsql2 = "update jsondata set generation=%d where id=%d" %(gene,iddata)
        cur.execute(tsql2)

        conn.commit()

    def MoveMaxDegreeEdge(G):
        NETWORK_SIZE=G.number_of_nodes()
        degreeMatrix=np.zeros((NETWORK_SIZE),dtype=int)#初始化度矩阵
        for i in range(NETWORK_SIZE):
            degreeMatrix[i]=G.degree(i)
        maxdegree=0
        maxdegreenode=0
        for i in range(NETWORK_SIZE):
            if degreeMatrix[i]>maxdegree:
                maxdegree=degreeMatrix[i]
                maxdegreenode=i
        print("最大度节点"+str(maxdegreenode))
        neighbor=list(G.neighbors(maxdegreenode))
        neighbor_len=len(neighbor)
        for i in range(neighbor_len):
            G.remove_edge(maxdegreenode,neighbor[i])
        return G

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
    # cur.execute('select * from jsondata order by id desc limit 1')
    # mydata = cur.fetchall()
    mydata=last_jsondata[0][1]
    #mydata = mydata[0][1]
    mydata = json.loads(mydata)

    G = json_graph.node_link_graph(mydata)

    #读取后删除数据
    cur.execute("truncate jsondata")
    cur.execute("truncate  graphcaldata")
    cur.execute("truncate  nodedata")
    conn.commit()


    gene=1

    while(1):
        if G.number_of_edges()==0:
            print("finish")
            break
        else:
            print("还剩余的边数"+str(G.number_of_edges()))
            G=MoveMaxDegreeEdge(G)
            GraphWRMysql(G)
            gene=gene+1



def WR_betweenessdisable(last_jsondata):
    def GraphWRMysql(G):
        d = json_graph.node_link_data(G)  # node-link format to serialize
        d_json = json.dumps(d)
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
        cur = conn.cursor()
        tsql  =  "insert into jsondata(json_data) values('{json}')"
        sql = tsql.format(json=pymysql.escape_string(d_json))
        cur.execute(sql)

        cur.execute('select * from jsondata order by id desc limit 1')
        iddata = cur.fetchall()
        iddata = iddata[0][0]
        #print(iddata) 
        tsql2 = "update jsondata set generation=%d where id=%d" %(gene,iddata)
        cur.execute(tsql2)

        conn.commit()


    def MoveMaxBetweennessEdge(G):
        
        bc=nx.degree_centrality(G)
        bc=sorted(bc.items(), key=lambda k: k[1], reverse=True)

        maxbetweennessnode=bc[0][0]
        print("最大中介中心性节点"+str(maxbetweennessnode))
        neighbor=list(G.neighbors(maxbetweennessnode))
        neighbor_len=len(neighbor)
        for i in range(neighbor_len):
            G.remove_edge(maxbetweennessnode,neighbor[i])
        return G


    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
    # cur.execute('select * from jsondata order by id desc limit 1')
    # mydata = cur.fetchall()
    # mydata = mydata[0][1]
    mydata=last_jsondata[0][1]
    mydata = json.loads(mydata)

    G = json_graph.node_link_graph(mydata)

    #读取后删除数据
    cur.execute("truncate jsondata")
    cur.execute("truncate graphcaldata")
    cur.execute("truncate nodedata")
    conn.commit()


    gene=1

    while(1):
        if G.number_of_edges()==0:
            print("finish")
            break
        else:
            print("还剩余的边数"+str(G.number_of_edges()))
            G=MoveMaxBetweennessEdge(G)
            GraphWRMysql(G)
            gene=gene+1



def WR_closenessdisable(last_jsondata):
    def GraphWRMysql(G):
        d = json_graph.node_link_data(G)  # node-link format to serialize
        d_json = json.dumps(d)
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
        cur = conn.cursor()
        tsql  =  "insert into jsondata(json_data) values('{json}')"
        sql = tsql.format(json=pymysql.escape_string(d_json))
        cur.execute(sql)

        cur.execute('select * from jsondata order by id desc limit 1')
        iddata = cur.fetchall()
        iddata = iddata[0][0]
        #print(iddata) 
        tsql2 = "update jsondata set generation=%d where id=%d" %(gene,iddata)
        cur.execute(tsql2)

        conn.commit()


    def MoveMaxClosenessEdge(G):
        
        bc=nx.closeness_centrality(G)
        bc=sorted(bc.items(), key=lambda k: k[1], reverse=True)

        maxclosenessnode=bc[0][0]
        print("最大紧密中心性节点"+str(maxclosenessnode))
        neighbor=list(G.neighbors(maxclosenessnode))
        neighbor_len=len(neighbor)
        for i in range(neighbor_len):
            G.remove_edge(maxclosenessnode,neighbor[i])
        return G


    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
    # cur.execute('select * from jsondata order by id desc limit 1')
    # mydata = cur.fetchall()
    # mydata = mydata[0][1]
    mydata=last_jsondata[0][1]
    mydata = json.loads(mydata)

    G = json_graph.node_link_graph(mydata)

    #读取后删除数据
    cur.execute("truncate jsondata")
    cur.execute("truncate graphcaldata")
    cur.execute("truncate nodedata")
    conn.commit()


    gene=1

    while(1):
        if G.number_of_edges()==0:
            print("finish")
            break
        else:
            print("还剩余的边数"+str(G.number_of_edges()))
            G=MoveMaxClosenessEdge(G)
            GraphWRMysql(G)
            gene=gene+1


def WR_eigenvectordisable(last_jsondata):
    def GraphWRMysql(G):
        d = json_graph.node_link_data(G)  # node-link format to serialize
        d_json = json.dumps(d)
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
        cur = conn.cursor()
        tsql  =  "insert into jsondata(json_data) values('{json}')"
        sql = tsql.format(json=pymysql.escape_string(d_json))
        cur.execute(sql)

        cur.execute('select * from jsondata order by id desc limit 1')
        iddata = cur.fetchall()
        iddata = iddata[0][0]
        #print(iddata) 
        tsql2 = "update jsondata set generation=%d where id=%d" %(gene,iddata)
        cur.execute(tsql2)

        conn.commit()


    def MoveMaxEigenvectorEdge(G):
        
        #bc=nx.eigenvector_centrality(G)

        try:
            bc=nx.eigenvector_centrality(G,max_iter=1000)
        except:
            bc={}
            for i in range(num_node):
                ec[i]=0
            print('bbbbbug')

        bc=sorted(bc.items(), key=lambda k: k[1], reverse=True)

        maxeigenvectornode=bc[0][0]
        print("最大特征向量中心性节点"+str(maxeigenvectornode))
        neighbor=list(G.neighbors(maxeigenvectornode))
        neighbor_len=len(neighbor)
        for i in range(neighbor_len):
            G.remove_edge(maxeigenvectornode,neighbor[i])
        return G


    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
    # cur.execute('select * from jsondata order by id desc limit 1')
    # mydata = cur.fetchall()
    # mydata = mydata[0][1]
    mydata=last_jsondata[0][1]
    mydata = json.loads(mydata)

    G = json_graph.node_link_graph(mydata)

    #读取后删除数据
    cur.execute("truncate jsondata")
    cur.execute("truncate graphcaldata")
    cur.execute("truncate nodedata")
    conn.commit()


    gene=1

    while(1):
        if G.number_of_edges()==0:
            print("finish")
            break
        else:
            print("还剩余的边数"+str(G.number_of_edges()))
            G=MoveMaxEigenvectorEdge(G)
            GraphWRMysql(G)
            gene=gene+1


def WR_katzdisable(last_jsondata):
    def GraphWRMysql(G):
        d = json_graph.node_link_data(G)  # node-link format to serialize
        d_json = json.dumps(d)
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
        cur = conn.cursor()
        tsql  =  "insert into jsondata(json_data) values('{json}')"
        sql = tsql.format(json=pymysql.escape_string(d_json))
        cur.execute(sql)

        cur.execute('select * from jsondata order by id desc limit 1')
        iddata = cur.fetchall()
        iddata = iddata[0][0]
        #print(iddata) 
        tsql2 = "update jsondata set generation=%d where id=%d" %(gene,iddata)
        cur.execute(tsql2)

        conn.commit()


    def MoveMaxKatzEdge(G):
        
        bc=nx.katz_centrality(G)
        bc=sorted(bc.items(), key=lambda k: k[1], reverse=True)

        maxkatznode=bc[0][0]
        print("最大katz中心性节点"+str(maxkatznode))
        neighbor=list(G.neighbors(maxkatznode))
        neighbor_len=len(neighbor)
        for i in range(neighbor_len):
            G.remove_edge(maxkatznode,neighbor[i])
        return G


    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
    # cur.execute('select * from jsondata order by id desc limit 1')
    # mydata = cur.fetchall()
    # mydata = mydata[0][1]
    mydata=last_jsondata[0][1]
    mydata = json.loads(mydata)

    G = json_graph.node_link_graph(mydata)

    #读取后删除数据
    cur.execute("truncate jsondata")
    cur.execute("truncate graphcaldata")
    cur.execute("truncate nodedata")
    conn.commit()


    gene=1

    while(1):
        if G.number_of_edges()==0:
            print("finish")
            break
        else:
            print("还剩余的边数"+str(G.number_of_edges()))
            G=MoveMaxKatzEdge(G)
            GraphWRMysql(G)
            gene=gene+1


