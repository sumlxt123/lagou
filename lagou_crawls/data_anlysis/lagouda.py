#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware

"""拉钩网职位数据分析
1、职位分布分析
2、职位要求分析
3、职位薪资分析
4、企业分析
"""

import re
import sys
import pymongo
import pandas as pd
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
format = logging.Formatter("%(asctime)s - %(filename)s [line:%(lineno)d] - %(levelname)s:\
 %(message)s")  # output format
sh = logging.StreamHandler(stream=sys.stdout)    # output to standard output
sh.setFormatter(format)
logger.addHandler(sh)

# class MongoBase:
#     def __init__(self,collection):
#         self.collection=collection
#         self.OpenDB()
#     def OpenDB(self):
#         user='******'
#         passwd='******'
#         host='******'
#         port='******'
#         auth_db='******'
#         uri = "mongodb://"+user+":"+passwd+"@"+host+":"+port+"/"+auth_db+"?authMechanism=SCRAM-SHA-1"
#         self.con = MongoClient(uri, connect=False)
#         self.db=self.con['qq']
#         self.collection=self.db[self.collection]
#
#     def closeDB(self):
#         self.con.close()



class Mongodb(object):
    """
    用于整合 mongodb 的基础操作，增加可复用性
    """
    def __init__(self,host='localhost',port=27017):
        self.host = host
        self.port = port
        pass

    def create_client(self):
        client = pymongo.MongoClient(host=self.host,port=self.port)
        logger.debug('create client : {}'.format(client))
        return client

    def create_db(self,database=None):
        client = self.create_client()
        client_db = client[database]
        logger.debug('create db : {}'.format(client_db))
        return client_db

    def create_collenction(self,database=None,colt=None):
        db = self.create_db(database)
        collen = db[colt]
        logger.debug('create collenction : {}'.format(collen))
        return collen

    def close_client(self):
        """关闭 monogdb client
        目前还不知道自己该怎么关闭计较合理
        client.close()
        """

        pass






class LagouPandas(object):
    """
    实现数据的处理：
    1、数据基础数据的规整和拆分
    2、数据合并
    3、数据统计
    """
    columns = [ 'menu_name', 'job_place', 'jobClass', 'job_id', 'jobName', 'job_payment',\
                'job_experience', 'compansnum', 'jobCompany', 'jobPlace','job_scr']
    skill_col = [ 'menu_name', 'job_place', 'jobClass', 'job_id', 'jobName']

    def __init__(self,jobs=None):
        self.jobs = jobs
        self.data = None
        # logger.debug('__init__ in info value :{}'.format(self.jobs))

    def get_jobs_base_mess(self):
        """统计出基本的职位信息"""
        data = pd.DataFrame(list(self.jobs))
        self.data = data[self.columns]
        logger.debug('get_jobs_base_mess in info value :{}'.format(self.data[:1]))
        return self.data

    def get_jobs_skill_mess(self):
        """获取职业所需的技能信息"""
        data = {'job_id':self.data['job_id']}
        logger.debug('get_jobs_skill_mess in data value :{}'.format(data))
        jobs = pd.DataFrame()
        for job in self.data['job_scr']:
            # 在将行转换为列时，需要关联字段，这个需要在一开始设计存储数据时就解决，要不后期解决成本较高
            logger.debug('get_jobs_skill_mess in job value :{}'.format(job))
            data = {'job_id':job['job_id'][0],'job_scr':job['job_scr']}
            logger.debug('get_jobs_skill_mess in data value :{}'.format(data))
            data = pd.DataFrame(data)
            logger.debug('get_jobs_skill_mess for pandas in data value :{}'.format(data[:1]))
            jobs = pd.concat([jobs,data])
            logger.debug('get_jobs_skill_mess for in jobs value :{}'.format(jobs[:1]))


        return jobs.drop_duplicates()





def main():
    mongodb = Mongodb()
    db = mongodb.create_collenction(database='test',colt='lagoudata2')
    logger.debug("main in db value: {}".format(db))
    jobs = db.find({},{'_id':0}).limit(3)


    lagouinfo = LagouPandas(jobs)
    lagouinfo.get_jobs_base_mess()
    job = lagouinfo.get_jobs_skill_mess()
    print(job)



if __name__ == "__main__":
    # mongodb = Mongodb()
    # db = mongodb.create_collenction(database='test',colt='lagoudata2')
    # print(db)
    # job = db.find_one()
    # print(job)
    main()

