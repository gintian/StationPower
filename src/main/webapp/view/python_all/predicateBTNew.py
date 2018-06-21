from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pymysql as db
import numpy as np
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
import pandas as pd
import re
import jieba
import sys

####删除括号######################################
def del_kuohao(str):
    kuohao_list = []
    for i in range(len(str)):
        if str[i] == '(' or str[i] == '（':
            kuohao_list.append(i)
        elif str[i] == ')' or str[i] == '）':
            if len(kuohao_list) != 0:
                index = kuohao_list.pop()
            else:
                index = 0
            str = str.replace(str[index: i + 1], (i + 1 - index) * '*')
    str = str.replace('*', '')
    return str

##命令行参数##############################################################################
print("**************")
print(sys.argv)
# proArgv=sys.argv[1]
proArgv = '安徽'
print(proArgv)
dict={'安徽':'anhui','北京':'beijing','成都':'chengdu','重庆':'chongqing','福建':'fujian','甘肃':'gansu','河北':'hebei','黑龙江':'heilongjang',
      '河南':'henan','湖北':'hubei','湖南':'hunan','江苏':'jiangsu','江西':'jiangxi_before','冀北':'jibei','吉林':'jilin','辽宁':'liaoning','蒙东':'mengdong',
      '宁夏':'ningxia','青海':'qinghai','山东':'shandong','山西':'shanxi','四川':'sicuan','新疆':'xinjiang','西藏':'xizang','浙江':'zhejiang'}
name=dict[proArgv]
print(name)

database =name
province =name

pro6=['anhui','chongqing','gansu','henan','hubei','hunan','jiangsu','liaoning','ningxia','shan1xi','shandong','sicuan','xinjiang']

##################################################################################################################

# jiangxi_before170619
# database = 'xizang'
# province = 'xizang'
path = 'F:/' + province + '_'
if database in pro6:
    conn = db.connect(host='172.16.135.6', user='root', passwd='10086', db=database, port=3306, charset='utf8')
else:
    conn = db.connect(host='172.16.135.8', user='jiangxi', passwd='456123', db=database, port=3306, charset='utf8')
cur = conn.cursor()
cur.execute("select DISTINCT obj_id,name,DISPATCH_LEVEL,A_SITE_ID,Z_SITE_ID,BUZ_TYPE from t_buz WHERE (A_SITE_ID IS NOT NULL AND A_SITE_ID!='')AND(Z_SITE_ID IS NOT NULL AND Z_SITE_ID!='')")
result = cur.fetchall()
data = np.array(result)

########################查询业务对应的通道类型 去t_channel_base找
# data_id = data[:,0]
# cur_type = conn.cursor()
# for i in range(len(data_id)):
#     cur_type.execute("select CHANNEL_TYPE from t_channel_base WHERE OBJ_ID=%s",data_id[i])
# result_type = cur_type.fetchall()
# data_channel_type=np.array(result_type)

########################查询业务对应的起始站点的站点类型 去t_spc_site查
data_A = data[:,3]
data_B = data[:,4]
data_type_A=[]
data_type_B=[]
cur_station_type = conn.cursor()
for i in range(len(data_A)):
    cur_station_type.execute("SELECT STATION_TYPE FROM t_spc_site WHERE OBJ_ID=%s",data_A[i])
    tmp2 = cur_station_type.fetchall()
    result_A = np.array(tmp2)
    # print(result_B.shape)
    if result_A.shape[0] == 0 or result_A.shape[1] == 0 or result_A[0][0] == "":
        data_type_A.append(0)
    else:
        data_type_A.append(np.array(result_A)[0][0])



for i in range(len(data_B)):
    cur_station_type.execute("SELECT STATION_TYPE FROM t_spc_site WHERE OBJ_ID=%s",data_B[i])
    tmp2 = cur_station_type.fetchall()
    result_B = np.array(tmp2)
    # print(result_B.shape)
    if result_B.shape[0] == 0 or result_B.shape[1] == 0 or result_B[0][0] == "":
        data_type_B.append(0)
    else:
        data_type_B.append(np.array(result_B)[0][0])

print(data_type_B[93])

###############为前端页面显示相关通道类型的名字，去提取name
# cur_type = conn.cursor()
cur_name = conn.cursor()
#
# cur_type.execute("select BUZ_TYPE from t_buz WHERE (BUZ_TYPE is not  null AND BUZ_TYPE<>'')")
#
# result_type = cur_type.fetchall()

data_type = data[:, -1]

#去t_pub_code提取name
data_name = []
for i in range(len(data_type)):
    cur_name.execute("select NAME from t_pub_code WHERE (TYPE='BUSINESS_TYPE' AND CODE=%s)",data_type[i])
    result_name = cur_name.fetchall()
    if (len(result_name) == 0):
        data_name.append('无法查找到名字')
    else:
        data_name.append(np.array(result_name)[0][0])




"""
word_list = ['继电', '保护', '专用', '光纤', 'B套', '安全', '自动', '装置', '调度', '数据', '集控', '采集', 'OPEN300',
             'EMS', '县调', '综合', '信息', '地调', '远动', '通信', 'PCM', '电话', '监控', '其他', 'SCADA', '行政',
             'SAGEM', 'FA16', 'FMX12', '交换', '省调', '以太网', 'ZXJ10', '会议', '电视', 'MIS', '内网', '外网', '视频',
             'OLT', '网管', '通道', '安排', '电量', '图像', '局域网', '安防', '生产', '管理', '质量', '监测', 'OLP',
             '故障', '测距', '网关', '应急', '指挥', '中心', '电能', '覆冰', '南瑞', '光切换', '广域网', '柘林', '财务',
             '五防', '线路', 'OA', '环境', '动力', '稳控', '星子', '微波', '带宽', '提升', '联网', '直流', '在线', '谐波',
             '2B+D', '租用', '电信', '运检班', 'DCN', '波分', '配电', 'NARI', '配网']
"""

# 字符串预处理
x_list = []
for i in range(data.shape[0]):
    """
    index1 = buz_name.find(')')
    index2 = buz_name.find('）')
    if index1 != -1:
        buz_name = buz_name[index1+1:]
    elif index2 != -1:
        buz_name = buz_name[index2+1:]
    """
    buz_name = data[i][1].replace(' ', '')  # 去掉空格
    buz_name = del_kuohao(buz_name)  # 去掉括号中的内容

    buz_name = re.sub('[A-Za-z0-9]*', '', buz_name)  # 去掉数字和字母
    buz_name = buz_name.replace('业务', '')  # 去掉"业务"
    if buz_name != '':
        x_list.append(buz_name)

# 结巴分词
word_list = []
for i in range(len(x_list)):
    seg_list = jieba.cut(x_list[i])
    for j in seg_list:
        word_list.append(j)
new_list = ['继电保护', '安全自动装置', '调度自动化', '调度电话', '行政电话', '综合数据网', '调度数据', '电视电话会议',
            '保护PCM', '通信PCM', '视频', '其他', '专用光纤', '网管', '配电自动化', '频控', 'PCM']

word_list.extend(new_list)
word_list = list(set(word_list))

# 加入其他特征
dptl_list = data[:, 2]  # 调度等级
# 初始化特征
x = np.zeros((data.shape[0], len(word_list)+3), dtype=np.float)
print(x.shape)
# 获得类别
y = data[:, -1]
# 量化
for i in range(x.shape[0]):
    for j in range(x.shape[1]):
        if j<len(word_list)and data[i, 1].find(word_list[j]) >= 0:
            x[i, j] = 1
        if j==len(word_list):
            x[i,j] = dptl_list[i]
        if j==len(word_list)+1:
            x[i,j] = data_type_A[i]
        if j==len(word_list)+2:
            x[i,j] = data_type_B[i]
            # print(i)

# dptl_list = dptl_list.reshape(-1, 1)
# print(x.shape)
# print(dptl_list.shape)
# x = np.concatenate((x, dptl_list), axis=1)
# 交叉验证
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)
# 伯努利朴素贝叶斯分类
clf = BernoulliNB()
# 训练
clf.fit(x_train, y_train)
print(clf.score(x_test, y_test))
# 预测
h = clf.predict(x)

"""
# 字符串预处理
x_list = []
for i in range(data.shape[0]):
    buz_name = data[i][1].replace(' ', '')  # 去掉空格
    buz_name = re.sub('[0-9]*$', '', buz_name)  # 去掉末尾数字
    buz_name = buz_name.replace('业务', '')  # 去掉"业务"
    # 去掉括号中的内容
    index1 = buz_name.find(')')
    index2 = buz_name.find('）')
    if index1 != -1:
        buz_name = buz_name[index1+1:]
    elif index2 != -1:
        buz_name = buz_name[index2+1:]
    x_list.append(buz_name)

print(x_list)
# 结巴分词
word_list = []
for i in range(len(x_list)):
    seg_list = jieba.cut(x_list[i])
    for j in seg_list:
        word_list.append(j)
word_list = list(set(word_list))
print(word_list)
# 特征
count_vec = CountVectorizer(vocabulary=word_list)
x = count_vec.fit_transform(x_list)
# vectorizer = TfidfVectorizer()
# x = vectorizer.fit_transform(x_list)
print(x.shape)
# 类别
y = data[:, -1]
# 交叉验证
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)
# 多项式朴素贝叶斯分类
clf = MultinomialNB()
# 训练
clf.fit(x_train, y_train)
print(clf.score(x_test, y_test))
# 预测
h = clf.predict(x)
"""
# 可能性
probablity = clf.predict_proba(x)
list_pro = []
for i in range(probablity.shape[0]):
    pro = max(list(probablity[i]))
    if abs(pro - 1.0) < 1e-4:
        pro = 0.9985
    pro = ("%.4f" % pro)
    pro = eval(pro)
    list_pro.append(pro)
# 输出结果
result = pd.DataFrame(np.column_stack((data[:, 0:2], data[:, -1], np.array(h).reshape((-1, 1)), np.array(list_pro).reshape((-1, 1)))),
                      columns=['obj_id', 'name', 'buz_type', 'predict', 'probablity'])
#result.to_csv(path+"buz_type_all.csv", index=False, header=True, encoding='gbk')
# 找出错误业务类型,包括错误值和空值
boarr_diff = []
boarr_null = []
for i in range(result.shape[0]):
    boarr_diff.append(result['buz_type'][i] != result['predict'][i] and result['buz_type'][i] != '')
    boarr_null.append(result['buz_type'][i] != result['predict'][i] and result['buz_type'][i] == '')
# 错误值导出
result_diff = result[boarr_diff].sort_values(by='probablity', ascending=False)  # 排序
#result_diff.to_csv(path+"buz_type_diff.csv", index=False, header=True, encoding='gbk')
# 空值导出
result_null = result[boarr_null].sort_values(by='probablity', ascending=False)  # 排序
#result_null.to_csv(path+"buz_type_null.csv", index=False, header=True, encoding='gbk')

#conn = db.connect(host='172.16.135.8', user='jiangxi', passwd='456123', db=database, port=3306, charset='utf8')
#输出到数据库中########################################################################################################
connect=db.connect(host="172.16.135.19",user="root",passwd="hadoop",db="jiangxi_power",port=3306,charset='utf8')
cursor=connect.cursor()
sql="create table if not exists buz_type_diff" \
    "(province varchar(255) DEFAULT NULL,obj_id varchar(255) DEFAULT NULL,buz_type varchar(255) DEFAULT NULL," \
    "predict varchar(255) DEFAULT NULL,probablity varchar(255) DEFAULT NULL,name varchar(255) DEFAULT NULL);"
cursor.execute(sql)

h=np.array(h).reshape((-1, 1))
list_pro=np.array(list_pro).reshape((-1, 1))
data4=[]###############predicate
data5=[]################probablity
values=[]
for i in h:
    data4.append(str(i).replace('[','').replace("]","").replace("'","").replace("'",""))
for j in list_pro:
    data5.append(str(j).replace('[','').replace("]",""))

data1=list(data[:,0])##############odj_id
data2=[]###############province
data3=list(data[:,-1])###########buzType
datan=data_name##########name 这个业务类型的编号代表的名称
data6=data[:,1]##########name_name 这个业务的名称

for i in range(len(data1)):
    data2.append(proArgv)
############异常的值（）diff
for i in range(len(data1)):
    if data3[i]!=data4[i] and data3[i]!='':
        values.append([data2[i],data1[i],data3[i],data4[i],data5[i],datan[i],data6[i]])

# cursor.execute('delete from buztype_diff ')
cursor.execute('delete from buz_type_diff WHERE province=%s',proArgv)
for i in range(len(values)):
    cursor.execute('insert into buz_type_diff VALUES(%s,%s,%s,%s,%s,%s,%s)',values[i])

##空值################3
values=[]
for i in range(len(data1)):
    if data3[i] != data4[i] and data3[i] == '':
        values.append([data2[i],data1[i],data4[i],data5[i],data6[i]])

cursor.execute('delete from buz_type_null WHERE province=%s',proArgv)
for i in range(len(values)):
    cursor.execute('insert into buz_type_null VALUES(%s,%s,%s,%s,%s)', values[i])


connect.commit()
cursor.close()
connect.close()



