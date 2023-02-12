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
            prefix_length = int(ip.split('/')[1])
            address = ip.split('/')[0]
             #タイムアウトしたとき
            if response_time == '-':
                if not address in recorded_ips:
                    recorded_ips[address] = [time, prefix_length]
            #ipアドレス本体を確認
            elif address in recorded_ips :
                print(f"{ip},{int((time-recorded_ips[address][0]).total_seconds())}")
                del recorded_ips[address]

#設問2
def find_timed_out_ip_N(filename, N: int):
    recorded_ips = {}
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            time = datetime.strptime(row[0], '%Y%m%d%H%M%S')
            ip = row[1]
            response_time = row[2]
            prefix_length = int(ip.split('/')[1])
            address = ip.split('/')[0]

            #タイムアウトしたとき
            if response_time == '-':
                if address in recorded_ips:
                    recorded_ips[address][2] += 1
                else:
                    recorded_ips[address] = [time, prefix_length, 1]
            #ipアドレス本体を確認
            elif address in recorded_ips:
                if recorded_ips[address][2] >= N:
                    print(f"{ip},{int((time-recorded_ips[address][0]).total_seconds())}")
                del recorded_ips[address]
                
#設問3
def find_overload(filename, N: int, m: int, t: int):
    timeout_recorded_ips = {}
    overload_recorded_ips = {}
    overload_timestamp = {}
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            time = datetime.strptime(row[0], '%Y%m%d%H%M%S')
            ip = row[1]
            response_time = row[2]
            prefix_length = int(ip.split('/')[1])
            address = ip.split('/')[0]

            #タイムアウトしたとき
            if response_time == '-':
                if address in timeout_recorded_ips:
                    timeout_recorded_ips[address][2] += 1
                else:
                    timeout_recorded_ips[address] = [time, prefix_length, 1]
            #ipアドレス本体を確認
            elif address in timeout_recorded_ips:
                if timeout_recorded_ips[address][2] >= N:
                    print(f"{ip},{int((time-timeout_recorded_ips[address][0]).total_seconds())},0")
                del timeout_recorded_ips[address]

            #過負荷関連の処理
            if response_time != '-':
                #初めてpingが応答を返すとき
                if not address in overload_recorded_ips:
                    overload_recorded_ips[address] = [[time], prefix_length, [int(response_time)]]
                else: 
                    overload_recorded_ips[address][0].append(time)
                    overload_recorded_ips[address][2].append(int(response_time))
                #直近m個の応答時間がたまった時
                if len(overload_recorded_ips[address][2]) >= m:
                    #過負荷状態の場合、直近m回前の時間を記録する
                    if statistics.mean(overload_recorded_ips[address][2][-m:]) > t:
                        if not address in overload_timestamp:
                            overload_timestamp[address] = [overload_recorded_ips[address][0][-m]]
                    #設問1,2と同様、終わったときに出力する。最後の数字は区別用、タイムアウトが0で過負荷状態が1
                    elif address in overload_timestamp:
                        print(f"{ip},{int((time-overload_timestamp[address][0]).total_seconds())},1")
                        del overload_timestamp[address]
                    overload_recorded_ips[address][0].pop(0)
                    overload_recorded_ips[address][2].pop(0)
                        

if __name__ == '__main__':
    #find_timed_out_ip("./log12.csv")
    """ print("N=1")
    find_timed_out_ip_N("./log12.csv", 1)
    print("N=2")
    find_timed_out_ip_N("./log12.csv", 2)
    print("N=3")
    find_timed_out_ip_N("./log12.csv", 3) """
    find_overload("log3.csv", 1, 3, 100)