# connect to mysql database
import mysql.connector

class database:
    def __init__(self, ip, port, user, pwd, database) -> None:
        self.conn = mysql.connector.connect(
            host = ip,
            port = port,
            user = user,
            password = pwd,
            database = database
        )
        self.cursor = self.conn.cursor()
    def exec(self, cmd: str):
        self.cursor.execute(cmd)
        result = self.cursor.fetchall()
        self.conn.commit()
        return result



if __name__ == '__main__':
    db = database(
        ip="192.168.134.123",
        port=3306,
        user="node1",
        pwd="mysql114514",
        database="grafana",
    )
    ret = db.exec("SELECT * FROM grafana.`CudaEvent2` ORDER BY time DESC LIMIT 5;")
    print(ret)
#     ret = db.exec(
#     """insert INTO grafana.`CudaEvent2` VALUES
# ('2024-07-19 8:25:00', TRUE, NULL, TRUE)
# ,('2024-07-19 8:36:00', NULL, NULL, NULL);"""
#     )
#     print(ret)
