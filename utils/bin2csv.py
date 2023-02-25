import pymavlink.mavutil
import argparse
import csv, os

# Create a mavlink object
parser = argparse.ArgumentParser(description='Convert ULog to CSV')
parser.add_argument('filepath', metavar='file.ulg', help='ULog input file')
args = parser.parse_args()

#filepath = '/home/tayyab/Downloads/4 1-1-1980 5-00-00 AM.bin'
try:
    mlog = pymavlink.mavutil.mavlink_connection(args.filepath)
    print("Successfully loaded log file.")
except FileNotFoundError:
    print("Specified file does not exist. Specify the correct filename and filepath. ")

req_messages = ['IMU', 'GPS', 'ATT', 'BARO', 'MAG']
msg_data = {m: {} for m in req_messages}
first_flags = {m: False for m in req_messages}
print(f"Converting {len(req_messages)} messages...")

# Iterate over all the messages in the log file
while True:
    msg = mlog.recv_msg()

    if not msg:
        break
    msg_type = msg.get_type()
    if msg_type in req_messages:
        if not first_flags[msg_type]:
            for msg_key, msg_value in msg.to_dict().items():
                if msg_key != 'mavpackettype':
                    msg_data[msg_type].setdefault(msg_key, []).append(msg_value)

            first_flags[msg_type] = True
        else:
            for msg_key, msg_value in msg.to_dict().items():
                if msg_key != 'mavpackettype':
                    msg_data[msg_type][msg_key].append(msg_value)

print("Loaded data from log file.")
msg_data_new = {}
for m in req_messages:
    unique_i = []

    if 'I' in msg_data[m].keys():
        unique_i = list(set(msg_data[m]['I'][:6]))
        
        if len(unique_i) == 1:
            msg_data_new[m] = msg_data[m]
        else:
            for k in range(len(unique_i)):
                msg_data_new[m + str(k)] = {}
                indices = [i for i, x in enumerate(msg_data[m]['I']) if x == k]
                for key in msg_data[m].keys():
                    msg_data_new[m + str(k)][key] = []
                    for ind in indices:
                        msg_data_new[m + str(k)][key].append(msg_data[m][key][ind]) 
    else:
        msg_data_new[m] = msg_data[m]
        continue
    #print(msg_data_new)

print("Writing CSV files...")
for m in msg_data_new.keys():
    with open(m + os.path.basename(args.filepath)[:-4] + '.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(msg_data_new[m].keys())
            for i in range(len(list(msg_data_new[m].values())[0])):
                row = [list(msg_data_new[m].values())[j][i] for j in range(len(msg_data_new[m]))]
                writer.writerow(row)
print(f"Wrote {len(msg_data_new)} CSV files.")