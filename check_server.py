import csv
from datetime import datetime
import statistics

#設問1
def find_timed_out_ip(filename):
    recorded_ips = {}
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            time = datetime.strptime(row[0], '%Y%m%d%H%M%S')
            ip = row[1]
            response_time = row[2]
             #タイムアウトしたとき
            if response_time == '-':
                if not ip in recorded_ips:
                    recorded_ips[ip] = [time]
            #ipアドレス本体を確認
            elif ip in recorded_ips :
                print(f"{ip},{int((time-recorded_ips[ip][0]).total_seconds())},{recorded_ips[ip][0]},{time}")
                del recorded_ips[ip]

#設問2
def find_timed_out_ip_N(filename, N: int):
    recorded_ips = {}
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            time = datetime.strptime(row[0], '%Y%m%d%H%M%S')
            ip = row[1]
            response_time = row[2]

            #タイムアウトしたとき
            if response_time == '-':
                if ip in recorded_ips:
                    recorded_ips[ip][1] += 1
                else:
                    recorded_ips[ip] = [time, 1]
            #ipアドレス本体を確認
            elif ip in recorded_ips:
                if recorded_ips[ip][1] >= N:
                    print(f"{ip},{int((time-recorded_ips[ip][0]).total_seconds())},{recorded_ips[ip][0]},{time}")
                del recorded_ips[ip]
                
#設問3
def find_overload(filename, m: int, t: int):
    overload_recorded_ips = {}
    overload_timestamp = {}
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            time = datetime.strptime(row[0], '%Y%m%d%H%M%S')
            ip = row[1]
            response_time = row[2]
            #過負荷関連の処理
            if response_time != '-':
                #初めてpingが応答を返すとき
                if not ip in overload_recorded_ips:
                    overload_recorded_ips[ip] = [[time], [int(response_time)]]
                else: 
                    overload_recorded_ips[ip][0].append(time)
                    overload_recorded_ips[ip][1].append(int(response_time))
                #直近m個の応答時間がたまった時
                if len(overload_recorded_ips[ip][1]) >= m:
                    #過負荷状態の場合、直近m回前の時間を記録する
                    if statistics.mean(overload_recorded_ips[ip][1][-m:]) > t:
                        if not ip in overload_timestamp:
                            overload_timestamp[ip] = [overload_recorded_ips[ip][0][-m]]
                    #設問1,2と同様、終わったときに出力する。
                    elif ip in overload_timestamp:
                        print(f"{ip},{int((time-overload_timestamp[ip][0]).total_seconds())},{overload_timestamp[ip][0]},{time}")
                        del overload_timestamp[ip]
                    overload_recorded_ips[ip][0].pop(0)
                    overload_recorded_ips[ip][1].pop(0)
                        
#設問4
def find_timed_out_ip_subnet(filename, N: int):
    recorded_ips = {}
    timeout_ips = {}
    ips = {}
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            time = datetime.strptime(row[0], '%Y%m%d%H%M%S')
            ip = row[1]
            response_time = row[2]
            prefix_length = int(ip.split('/')[1])
            #サブネットごとにIPアドレスの一覧を作る
            if not prefix_length in ips:
                ips[prefix_length] = [ip]
            else:
                if not ip in ips[prefix_length]:
                    ips[prefix_length].append(ip)
            #タイムアウトしたとき
            if response_time == '-':
                if ip in recorded_ips:
                    recorded_ips[ip][1] += 1
                else:
                    recorded_ips[ip] = [time,1]
            #タイムアウトが明けたら故障のログを作成
            elif ip in recorded_ips:
                timeout_exist = True
                if recorded_ips[ip][1] >= N:
                    fault_period = int((time-recorded_ips[ip][0]).total_seconds())
                    if not prefix_length in timeout_ips:
                        timeout_ips[prefix_length] = [[fault_period, time, recorded_ips[ip][0], [ip]]]
                    else:
                        #重複判定 故障期間が同じかつと前後の時刻が1分以内であれば同時刻の故障とみなす。
                        for index, f in enumerate(timeout_ips[prefix_length]):
                            if f[0] == fault_period and abs(int((f[1]-time).total_seconds())) < 60 and abs(int((f[2]-recorded_ips[ip][0]).total_seconds())) < 60:
                                timeout_exist = False
                                timeout_ips[prefix_length][index][3].append(ip)
                                break
                        if timeout_exist:
                            timeout_ips[prefix_length].append([fault_period, time, recorded_ips[ip][0], [ip]])
                del recorded_ips[ip]
        #IPアドレスの一覧と照合して出力
        for key in timeout_ips:
            for result in timeout_ips[key]:
                if len(result[3]) == len(ips[key]):
                    print(f"{key},{result[0]},{result[1]},{result[2]}")

                
if __name__ == '__main__':
    find_timed_out_ip("./log12.csv")
    print("N=1")
    find_timed_out_ip_N("./log12.csv", 1)
    print("N=2")
    find_timed_out_ip_N("./log12.csv", 2)
    print("N=3")
    find_timed_out_ip_N("./log12.csv", 3)
    find_overload("log3.csv", 3, 100)
    find_timed_out_ip_subnet("log4.csv", 3)