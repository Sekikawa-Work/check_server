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
            
            if response_time == '-':
                recorded_ips[address] = (time, prefix_length)
            #ipアドレス本体とプレフィックス長を確認
            elif address in recorded_ips and recorded_ips[address][1] == prefix_length:
                print(f"{ip},{int((time-recorded_ips[address][0]).total_seconds())}")
                del recorded_ips[address]

find_timed_out_ip("./log.csv")