import mongoengine
import pymysql

pymysql.install_as_MySQLdb()

# mongoengine指明要连接的数据库
mongoengine.connect('spitdb', host='127.0.0.1', port=27017)