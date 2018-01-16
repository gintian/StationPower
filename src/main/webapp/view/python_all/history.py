import pandas as pd
import pymysql.cursors
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import matplotlib.cm as cm
from EquipFailureBytime import *
from FiberSegFailureBytime import *
from pandas import Series
import sys


config = {
    'host':"172.16.135.19",
    'port':3306,
    'user':'root',
    'password':'hadoop',
    'db':'jiangxi_power',
    'charset':'utf8',
    'cursorclass':pymysql.cursors.DictCursor,
}

connection = pymysql.connect(**config)

myfont = matplotlib.font_manager.FontProperties(fname=r"c:\windows\fonts\simhei.ttf", size=16)


province = 'jiangxi'
graphPath = 'E:/new_graph/'
path = graphPath + 'history/type3/'    #保存图片路径

def resolvebusz(buz_id,buz_lst):
    r = getReliability()
    s = FailureselectByMonth()
    businessid = buz_id  # 业务id
    print("b_id:" + businessid)
    if (len(buz_lst) <= 1):
        return
    index = 0
    G = nx.Graph()
    firstnode = ''
    lastnode = ''
    fiber_dict = {}
    node_dic = {}
    nodes = []
    nodevmax = float(0.0)
    nodevmin = float(1.0)
    paths = []
    fiberLsts = []
    while (index < len(buz_lst)):
        vals = buz_lst[index]
        equips = []
        fibersegs = []
        prevnode = ''
        if (len(vals) > 1):
            for equip in vals:
                if (firstnode == ''):
                    firstnode = equip
                equips.append(equip)
                nodes.append(equip)
                # 获取设备可靠性getEqpAvgRel
                eReliability = getEqpAvgRel(equip)
                er = round(eReliability, 3)
                node_dic[equip] = er
                print(er)
                if (er > nodevmax): nodevmax = er
                if (er < nodevmin): nodevmin = er

                if (prevnode != ''):
                    # 获取光缆ID及平均可靠性
                    fsID, w = r.fiberFailureByType(prevnode, equip)
                    print(fsID)
                    print(w)
                    fiber_dict[fsID] = w
                    fibersegs.append(fsID)
                    G.add_edge(prevnode, equip, weight=w)
                prevnode = equip
                if (lastnode == ''): lastnode = vals[-1]
            paths.append(equips)
            fiberLsts.append(fibersegs)
        index += 1
    print(paths)
    print(fiberLsts)
    if (lastnode != ""):
        fig = plt.figure(figsize=(16, 8))  # 新图 0
        # fig = plt.figure(figsize=(30, 15))
        # fig.suptitle(u'(500kV赣州变～500kV罗坊变)安全自动装置业务' + '\n', fontproperties=myfont, fontsize=60, color='w')
        fig.subplots_adjust(wspace=0.4)
        ax1 = plt.subplot2grid((1, 2), (0, 0))
        pos = nx.spectral_layout(G)  # positions for all nodes
        lables = {}
        m = 1
        for e in G.nodes():
            if e == firstnode:
                lables[e] = r"$S$"
            elif e == lastnode:
                lables[e] = r"$E$"
            else:
                lables[e] = str(m)
                m += 1
        widthlst = [float(d['weight'] * 5) for (u, v, d) in G.edges(data=True)]
        if (nodevmax != nodevmin):
            levels = np.arange(nodevmin, nodevmax, (nodevmax - nodevmin) / 10)
        else:
            nodevmin = 0.0
            nodevmax = 1.0
            levels = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]

        nx.draw_networkx_nodes(G, pos, node_color=list(node_dic[node] for node in G.nodes()), node_size=1000,
                               cmap=cm.jet, vmin=nodevmin, vmax=nodevmax, alpha=0.7, label=None)
        nx.draw_networkx_edges(G, pos, width=widthlst, alpha=0.7)
        nx.draw_networkx_labels(G, pos, lables, font_size=16, font_weight='bold', font_color='w')

        nodecmap = cm.jet
        Z = [[0, 0], [0, 0]]
        bar = plt.contourf(Z, levels, cmap=nodecmap, alpha=0.7)
        ax1=plt.colorbar(bar)
        # ax1.set_ticks([0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00])
        ax1.set_label('equipment average reliability',  color='black')
        # plt.xlabel(str(businessid))
        plt.savefig(path + businessid + ".png", transparent=True, format='png', dpi=80)  # save as png

        G.clear()
        plt.axis('off')
        # 计算业务可靠性
        monthlist = ['2016-01', '2016-02', '2016-03', '2016-04', '2016-05', '2016-06', '2016-07', '2016-08',
                     '2016-09', '2016-10', '2016-11', '2016-12', '2017-01', '2017-02', '2017-03'];
        x = range(15)
        buzreliablelist = []
        for month in monthlist:
            timem = datetime.datetime.strptime(month, '%Y-%m')
            days = calendar.monthrange(int(month.split('-')[0]), int(month.split('-')[1]))[1]
            seconds = days * 24 * 3600
            buzreliable = float(1)
            commonreliable = float(1);
            psreliable_0 = float(1);
            psreliable_1 = float(1);
            if (len(paths) == 1):
                for eq in paths[0]:
                    ereliable = s.failure(eq, month) / seconds
                    buzreliable = buzreliable * (1 - ereliable);
                buzreliablelist.append(buzreliable)
            if (len(paths) == 2):
                for eq in paths[0]:
                    ereliable = s.failure(eq, month) / seconds
                    if (eq in paths[1]):
                        commonreliable = commonreliable * (1 - ereliable);
                    else:
                        psreliable_0 = psreliable_0 * (1 - ereliable)
                for eq in paths[1]:
                    ereliable = s.failure(eq, month) / seconds
                    if (eq in paths[0]):
                        pass
                    else:
                        psreliable_1 = psreliable_1 * (1 - ereliable)

                buzreliable = commonreliable * (1 - (1 - psreliable_0) * (1 - psreliable_1))
                buzreliablelist.append(buzreliable)
        plt.subplot2grid((1, 2), (0, 1))
        plt.plot(x, buzreliablelist, "b--", linewidth=1)
        # plt.axis('off')
        plt.xlabel("month(s)")  # X轴标签
        plt.ylabel("reliable")  # Y轴标签

        # plt.show()
        plt.savefig(path + businessid + ".png")  # save as png
    plt.close('all')  # 关闭图s

def getEqpAvgRel(equip):
    s = FailureselectByMonth()
    monthlist = ['2016-01', '2016-02', '2016-03', '2016-04', '2016-05', '2016-06', '2016-07', '2016-08',
                 '2016-09', '2016-10', '2016-11', '2016-12', '2017-01', '2017-02', '2017-03']
    efailure = float(0)
    ereliable = float(1)
    for month in monthlist:
        days = calendar.monthrange(int(month.split('-')[0]), int(month.split('-')[1]))[1]
        seconds = days * 24 * 3600
        efailure += (s.failure(equip, month) / seconds)
    ereliable = 1 - efailure / len(monthlist)
    return ereliable


def to_list(str):
    nelist = []
    list1 = str.split("], [")
    # print(list1)
    for i in range(len(list1)):
        if (i == 0):
            list1[i] = list1[i][2:]
        if (i == len(list1) - 1):
            list1[i] = list1[i][0:-2]
        # print(list1[i])
        # print(type(list1[i]))
        str1 = list1[i]
        # print(str1)
        list3 = []
        list2 = str1.split(", ")
        # print(list2)

        for j in range(len(list2)):
            # if (j == 0):
            #     list2[j] = list2[j][1:]
            # if (i == len(list2) - 1):
            #     list2[j] = list2[j][:-1]
            list2[j] = list2[j][1:-1]
            # print(list2[j])

            list3.append(list2[j])

        nelist.append(list3)
    # print(nelist)
    # print(type(nelist))
    return nelist





    # buz_id = sys.argv[1]
    # buz_id = "A7464B0A-B0FB-41C5-951A-FE17E41B7263-00250"


if __name__ == '__main__':

    buz_id = sys.argv[1]
    buz_type = sys.argv[2]
    # buz_id = "A7464B0A-B0FB-41C5-951A-FE17E41B7263-00250"
    sql = "select OBJ_ID,BUZ_TYPE,NE_LIST from jiangxi_t_buz_re WHERE OBJ_ID = '%s' "%buz_id
    results = pd.read_sql(sql, connection)
    lists = []
    nestr = results.ix[0].NE_LIST
    lists = to_list(nestr)
    resolvebusz(buz_id, lists)

    connection.close()

