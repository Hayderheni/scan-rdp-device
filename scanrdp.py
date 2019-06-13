from shodan import Shodan
import pymysql
import os, datetime
import getpass

class get_results():
    def __init__(self, results):
        self.matches = results['matches']
        self.get_result()

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
        self.post_data()

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


class save_to_file():
    def __init__(self, results):
        self.results = results
        self.ip = self.to_list()
        self.to_file(self.ip)

    def to_list(self):
        ip = []
        for result in self.results:
            ip.append(result['ip'])
        return ip

    def to_file(self, ip_list):
        f = open('result.txt', 'w+')
        for ip in ip_list:
            f.write(ip + '\n')
        f.close()


def main():
    API_KEY = getpass.getpass("输入你的APIKEY:")

    try:
        os.system("clear")
        api = Shodan(API_KEY)
        results = api.search("port:3389 os:windows", limit=None, page=10)
    except:
        os.system('clear')
        print("\nWDNMD,别搞事啊！！")
        exit(0)
    print("共有:{}个结果".format(results['total']))
    FINAL = get_results(results).get_result()
    try:
        id = int(input('1.存入数据库\n2.存入文件\n你的选择:'))
    except:
        os.system('clear')
        print("\nWDNMD,别搞事啊！！")
        exit(0)
    if id ==1:
        db_action(FINAL)
    elif id == 2:
        save_to_file(FINAL)
    else:
        os.system('clear')
        print("\nWDNMD,别搞事啊！！")
        exit(0)

if __name__ == "__main__":
    main()
