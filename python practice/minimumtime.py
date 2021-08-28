time_seen = []*24*60
input = ['23:59','00:00']

for time in input:
    time_split = time.split(':')
    hour = int(time_split[0])
    mins = int(time_split[1])
    time_seen[(hour*60)+mins] = True
    
 