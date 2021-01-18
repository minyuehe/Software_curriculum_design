
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

# WR_erdos_renyi_graph(n,p) 生成ER图，清除jsondata之前的数据，并写入新的生成数据
# n:ER网络的顶点个数     p:连边概率

# WR_watts_strogatz_graph(n, k, p) 生成WS图，清除jsondata之前的数据，并写入新的生成数据
# n:WS网络的顶点个数   k:WS网络每个顶点邻居个数   p:重连边概率    

# WR_barabasi_albert_graph(n, m) 生成BA图，清除jsondata之前的数据，并写入新的生成数据
# n:BA网络的顶点个数   m:BA网络每次加入边个数


def WR_erdos_renyi_graph(NETWORK_SIZE,PROBABILITY_OF_EAGE):

    adjacentMatrix=np.zeros((NETWORK_SIZE,NETWORK_SIZE),dtype=int)#初始化邻接矩阵
    random.seed(time.time())#'random.random()#生成[0,1)之间的随机数

    #生成ER网络矩阵
    count=0
    probability=0.0
    for i in range(NETWORK_SIZE):
        for j in range(i+1,NETWORK_SIZE):
            probability=random.random()
            if probability<PROBABILITY_OF_EAGE:
                count =count+1
                adjacentMatrix[i][j]=adjacentMatrix[j][i]=1
    print('您所构造的ER网络边数为：'+str(count))

    #产生json数据并写入数据库
    G = nx.random_graphs.random_regular_graph(0,NETWORK_SIZE)  #生成包含NETWORK_SIZE个节点规则图G
    # so add a name to each node
    for n in G:
        G.nodes[n]["name"] = n
    #图的初始状态
    d = json_graph.node_link_data(G)  # node-link format to serialize
    d_json = json.dumps(d)
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()

    #将之前的数据删除
    cur.execute("truncate jsondata")
    cur.execute("truncate graphcaldata")
    cur.execute("truncate nodedata")
    conn.commit()

    gene=1
    tsql  =  "insert into jsondata(json_data) values('{json}')"
    sql = tsql.format(json=pymysql.escape_string(d_json))
    cur.execute(sql) 

    cur.execute('select * from jsondata order by id desc limit 1')
    iddata = cur.fetchall()
    iddata = iddata[0][0]
    #print(iddata) 
    gene=1
    tsql2 = "update jsondata set generation=%d where id=%d" %(gene,iddata)
    cur.execute(tsql2)
    conn.commit()

    #开始连接
    for i in range(len(adjacentMatrix)):
        for j in range(i+1,len(adjacentMatrix)):
            if adjacentMatrix[i][j]==1:#如果不加这句将生成完全图，ER网络的邻接矩阵将不其作用
                G.add_edge(i,j)
                d = json_graph.node_link_data(G)  # node-link format to serialize
                d_json = json.dumps(d)
                #conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123', db='networkxdata')
                #cur = conn.cursor()
                #tsql  =  "insert into jsondata(data) values('{json}')"
                sql = tsql.format(json=pymysql.escape_string(d_json))
                cur.execute(sql)

                cur.execute('select * from jsondata order by id desc limit 1')
                iddata = cur.fetchall()
                iddata = iddata[0][0]
                #print(iddata) 
                gene=gene+1
                tsql2 = "update jsondata set generation=%d where id=%d" %(gene,iddata)
                cur.execute(tsql2)

                conn.commit()  
    
    #conn.commit()
    conn.close()



def WR_watts_strogatz_graph(n, k, p):

    G = nx.Graph()
    nodes = list(range(n))  # nodes are labeled 0 to n-1
    # connect each node to k/2 neighbors
    for j in range(1, k // 2 + 1):
        targets = nodes[j:] + nodes[0:j]  # first j nodes are now last in list
        G.add_edges_from(zip(nodes, targets))
    # rewire edges from each node
    # loop over all nodes in order (label) and neighbors in order (distance)
    # no self loops or multiple edges allowed

    random.seed(time.time())#'random.random()#生成[0,1)之间的随机数
    


    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
   
    #将之前的数据删除
    cur.execute("truncate jsondata")
    cur.execute("truncate graphcaldata")
    cur.execute("truncate nodedata")
    conn.commit()

    # so add a name to each node
    for n in G:
        G.nodes[n]["name"] = n
    #图的初始状态
    #写初始数据库json_data
    d = json_graph.node_link_data(G)  # node-link format to serialize
    d_json = json.dumps(d)
    tsql  =  "insert into jsondata(json_data) values('{json}')"
    sql = tsql.format(json=pymysql.escape_string(d_json))
    cur.execute(sql) 
    
    #写初始数据库generation
    cur.execute('select * from jsondata order by id desc limit 1')
    iddata = cur.fetchall()
    iddata = iddata[0][0] 
    gene=1
    tsql2 = "update jsondata set generation=%d where id=%d" %(gene,iddata)
    cur.execute(tsql2)

    conn.commit()


    for j in range(1, k // 2 + 1):  # outer loop is neighbors
        targets = nodes[j:] + nodes[0:j]  # first j nodes are now last in list
        # inner loop in node order
        for u, v in zip(nodes, targets):
            if random.random() < p:
                w = random.choice(nodes)
                # Enforce no self-loops or multiple edges
                while w == u or G.has_edge(u, w):
                    w = random.choice(nodes)
                    if G.degree(u) >= n - 1:
                        break  # skip this rewiring
                else:
                    #remove
                    G.remove_edge(u, v)
                    
                    #写数据库json_data
                    d = json_graph.node_link_data(G)  # node-link format to serialize
                    d_json = json.dumps(d)
                    tsql  =  "insert into jsondata(json_data) values('{json}')"
                    sql = tsql.format(json=pymysql.escape_string(d_json))
                    cur.execute(sql)

                    #写数据库generation
                    cur.execute('select * from jsondata order by id desc limit 1')
                    iddata = cur.fetchall()
                    iddata = iddata[0][0] 
                    gene=gene+1
                    tsql2 = "update jsondata set generation=%d where id=%d" %(gene,iddata)
                    cur.execute(tsql2)

                    conn.commit()
                    
                    print("remove(%d,%d)"%(u,v))


                    #add
                    G.add_edge(u, w)
                    d = json_graph.node_link_data(G)  # node-link format to serialize
                    d_json = json.dumps(d)
                    tsql  =  "insert into jsondata(json_data) values('{json}')"
                    sql = tsql.format(json=pymysql.escape_string(d_json))
                    cur.execute(sql)

                    #写数据库generation
                    cur.execute('select * from jsondata order by id desc limit 1')
                    iddata = cur.fetchall()
                    iddata = iddata[0][0] 
                    gene=gene+1
                    tsql2 = "update jsondata set generation=%d where id=%d" %(gene,iddata)
                    cur.execute(tsql2)

                    conn.commit()
                    print("add(%d,%d)"%(u,w))
    print("finish")





def WR_barabasi_albert_graph(n, m):

    random.seed(time.time())#'random.random()#生成[0,1)之间的随机数
    seed=random

    def _random_subset(seq, m, rng):
        """ Return m unique elements from seq.

        This differs from random.sample which can return repeated
        elements if seq holds repeated elements.

        Note: rng is a random.Random or numpy.random.RandomState instance.
        """
        targets = set()
        while len(targets) < m:
            x = rng.choice(seq)
            targets.add(x)
        return targets
    # Add m initial nodes (m0 in barabasi-speak)
    G = nx.random_graphs.random_regular_graph(0,m)
    #G = empty_graph(m)
    # so add a name to each node
    for i in G:
        G.nodes[i]["name"] = i
    # Target nodes for new edges
    targets = list(range(m))
    # List of existing nodes, with nodes repeated once for each adjacent edge
    repeated_nodes = []
    # Start adding the other n-m nodes. The first node is m.
    source = m

    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='networkxdata')
    cur = conn.cursor()
   
    #将之前的数据删除
    cur.execute("truncate jsondata")
    cur.execute("truncate graphcaldata")
    cur.execute("truncate nodedata")
    conn.commit()


    #图的初始状态
    #写初始数据库json_data
    d = json_graph.node_link_data(G)  # node-link format to serialize
    d_json = json.dumps(d)
    tsql  =  "insert into jsondata(json_data) values('{json}')"
    sql = tsql.format(json=pymysql.escape_string(d_json))
    cur.execute(sql) 
    
    #写初始数据库generation
    cur.execute('select * from jsondata order by id desc limit 1')
    iddata = cur.fetchall()
    iddata = iddata[0][0] 
    gene=1
    tsql2 = "update jsondata set generation=%d where id=%d" %(gene,iddata)
    cur.execute(tsql2)

    conn.commit()

    while source < n:
        # Add edges to m nodes from the source.
        G.add_edges_from(zip([source] * m, targets))
        # Add one node to the list for each new edge just created.
        repeated_nodes.extend(targets)

        # And the new node "source" has m edges to add to the list.
        repeated_nodes.extend([source] * m)
        # Now choose m unique nodes from the existing nodes
        # Pick uniformly from repeated_nodes (preferential attachment)
        targets = _random_subset(repeated_nodes, m, seed)
        source += 1
        
        for i in G:
            G.nodes[i]["name"] = i

        #写数据库json_data
        d = json_graph.node_link_data(G)  # node-link format to serialize
        d_json = json.dumps(d)
        tsql  =  "insert into jsondata(json_data) values('{json}')"
        sql = tsql.format(json=pymysql.escape_string(d_json))
        cur.execute(sql)

        #写数据库generation
        cur.execute('select * from jsondata order by id desc limit 1')
        iddata = cur.fetchall()
        iddata = iddata[0][0] 
        gene=gene+1
        tsql2 = "update jsondata set generation=%d where id=%d" %(gene,iddata)
        cur.execute(tsql2)

        conn.commit()



                             