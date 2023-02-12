import csv
from datetime import datetime

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
                
if __name__ == '__main__':
    #find_timed_out_ip("./log.csv")
    find_timed_out_ip_N("./log.csv", 1)