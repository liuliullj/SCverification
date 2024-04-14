from dbutils.pooled_db import PooledDB, SharedDBConnection
import pymysql


# pip install DBUtils

class Config(object):
    SALT = b"sdf1123df"  # 加盐
    SECRET_KEY = 'asdf123sdfsdfsdf'  # 用session 必须加这个，内容无所谓
    MAX_CONTENT_LENGTH = 1024 * 1024 * 7  # 蛇者文件大小
    #   连接池
    POOL = PooledDB(
        creator=pymysql,  # 使用链接数据库的模块
        maxconnections=20,  # 连接池允许的最大连接数，0和None表示不限制连接数
        mincached=10,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        maxcached=10,  # 链接池中最多闲置的链接，0和None不限制
        maxshared=3,
        # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
        blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
        setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
        ping=0,
        # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
        host='127.0.0.1',
        port=3306,
        user='root',
        password='1999511510',
        database='database_learn',
        charset='utf8'
    )