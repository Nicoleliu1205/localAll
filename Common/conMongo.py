import logging
import pymongo
import pymysql
import redis
from bson import ObjectId

#mongoDB数据库连接
myclient = pymongo.MongoClient("mongodb://192.168.0.189:27017/")
try:
    print(myclient.server_info())
except Exception:
    print("Unable to connect to the mongoDB server.")

def findsql(dbname, tablename, querystr):
    mydb_account = myclient[dbname]
    mycol = mydb_account[tablename]
    for x in mycol.find(querystr):
        logging.log.info("查询数据库结果为：" + str(x))
        return x

def findSqlSort(dbname, tablename, querystr,sortstr,updown):
    mydb_account = myclient[dbname]
    mycol = mydb_account[tablename]
    results=mycol.find(querystr).sort(sortstr,updown)
    logging.log.info(results)
    for x in results:
        logging.log.info("查询数据库结果为：" + str(x))
        return x


def addsql(dbname, tablename, addstr):
    mydb_account = myclient[dbname]
    mycol = mydb_account[tablename]
    x = mycol.insert_one(addstr)
    logging.log.info("插入数据库完成")
    return x.inserted_id


def delsql(dbname, tablename, delstr):
    mydb_account = myclient[dbname]
    mycol = mydb_account[tablename]
    mycol.delete_one(delstr)
    logging.log.info("删除数据库完成")


def editsql(dbname, tablename, query, newvalues):
    mydb_account = myclient[dbname]
    mycol = mydb_account[tablename]
    mycol.update_one(query, {"$set":newvalues})
    logging.log.info("修改数据库完成")


#MySQL连接-chain
db=pymysql.connect(host='154.91.156.113',
                   user='22c6bd3282c1af51',
                   password='7de7ec1548406fca',
                   database='VII_SCORES')
def findmysql(querystr):
    cursor=db.cursor()
    try:
        cursor.execute(querystr)
        results=cursor.fetchall()
        for row in results:
            print(row)
    except:
        print("find mysql error:")
db.close()


#redis连接
r = redis.Redis(host='192.168.0.189', port=6379, db=7)

if __name__ == "__main__":
    query = {"_id": ObjectId("62a80b668ab8e17276d1245e")}
    newvalues = {"$set": {"photoFrameBindStatus": "UNBOUND"}}
    editsql("owl-account", "photo_frame", query, newvalues)
    findsql("owl-account", "photo_frame", query)
    print("account case runned!")



