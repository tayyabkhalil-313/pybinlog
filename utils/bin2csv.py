import pymavlink.mavutil
import argparse
import csv, os

def main():
    parser = argparse.ArgumentParser(description='Convert bin to CSV')
    parser.add_argument('filepath', metavar='file.bin', help='bin input file')
    parser.add_argument(
        '-m', '--messages', dest='messages',
        help=("Required messages for conversion to csv. Must be a comma-separated list of"
              " names, like 'ATT,IMU'"))
    parser.add_argument(
        '-o', '--output_dir', dest='output_dir',
        help=("Directory for saving the CSV files."))
    args = parser.parse_args()
    convert2csv(args.filepath, args.messages, args.output_dir)

def convert2csv(filepath, req_messages, output_directory):
    try:
        mlog = pymavlink.mavutil.mavlink_connection(filepath)
        print("Successfully loaded log file.")
    except FileNotFoundError:
        print("Specified file does not exist. Specify the correct filename and filepath. ")

    output_directory = os.path.dirname(filepath) if output_directory is None else output_directory

    req_messages = req_messages.replace(" ", "").split(',') if req_messages else mlog.messages.keys()
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

    print("Writing CSV files...")
    count = 0
    for m in msg_data_new.keys():
        if len(list(msg_data_new[m].values())) > 0: 
            #Create CSV file if message is not empty
            output_path = os.path.join(output_directory, m + '-' + os.path.basename(filepath)[:-4] + '.csv')
            with open(output_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(msg_data_new[m].keys())
                    for i in range(len(list(msg_data_new[m].values())[0])):
                        row = [list(msg_data_new[m].values())[j][i] for j in range(len(msg_data_new[m]))]
                        writer.writerow(row)
            count += 1         
    print(f"Wrote {count} CSV files.")