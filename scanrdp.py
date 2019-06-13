from shodan import Shodan
import pymysql


# API_KEY = 17VYuBdMTySxjVzyJtgsOjDtxH8WM0pD

class get_results():
    def __init__(self, results):
        self.matches = results['matches']

    def get_result(self):
        FINAL = []
        for result in self.matches:
            f = {}
            f['os'] = result['os']
            f['isp'] = result['isp']
            f['port'] = result['port']
            f['city'] = result['location']['city']
            f['longitude'] = result['location']['longitude']
            f['country'] = result['location']['country_name']
            f['latitude'] = result['location']['latitude']
            f['timestamp'] = result['timestamp']
            f['org'] = result['org']
            f['data'] = result['data']
            f['transport'] = result['transport']
            f['ip'] = result['ip_str']
            if f['data'][0:14] == 'Remote Desktop':
                FINAL.append(f)
        return FINAL


class db_action():
    def __init__(self, data):
        self.db = pymysql.connect("localhost", "root", "951640", 'result')
        self.cursor = self.db.cursor()
        self.data = data
        self.cursor.execute('truncate result')

    def post_data(self):
        id = 0
        for F in self.data:
            id = id + 1
            sql = """
            INSERT INTO result(id,os,isp,port,city,country,longitude,latitude,ip,org,data,transport)
            VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
            """.format(id, F['os'], F['isp'], F['port'], F['city'], F['country'], F['longitude'], F['latitude'],
                       F['ip'], F['org'], F['data'], F['transport'])
            try:
                self.cursor.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
        self.db.close()


API_KEY = "17VYuBdMTySxjVzyJtgsOjDtxH8WM0pD"
api = Shodan(API_KEY)
results = api.search("port:3389 os:windows", limit=None, page=10)
print(len(results['matches']))
print("共有：{}个结果".format(results['total']))
FINAL = get_results(results).get_result()
db_action(FINAL).post_data()
