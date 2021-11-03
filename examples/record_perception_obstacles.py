# ****************************************************************************
# Copyright 2018 The Apollo Authors. All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ****************************************************************************
# -*- coding: utf-8 -*-
"""Module for example of record trans."""

import sys
import os
sys.path.append("/apollo/cyber")
os.chdir("/apollo/cyber")
from cyber_py import cyber
from cyber_py import record
from modules.perception.proto import perception_obstacle_pb2

MSG_TYPE = "apollo.perception.PerceptionObstacles"
CHANNEL_NAME = "/apollo/perception/obstacles"
MSG_TYPE_CHATTER = "apollo.cyber.proto.Chatter"

variable_to_record = ['brake', 'accleration', 'steering_rate', 'steering_target', 'speed', 'throttle']

data_list = list()


def saveList(paraList, path):
    output = open(path, 'wb')
    # Pickle dictionary using protocol 0.
    pickle.dump(paraList, output)
    output.close()

'''
load the pkl files
'''
def loadList(path):
    pkl_file = open(path, 'rb')
    segContent = pickle.load(pkl_file)
    pkl_file.close()
    return segContent

def headers_to_dict(raw_headers):
    d = dict()
    for i in raw_headers.split('\n'):
        if ":" in i:
            k = i.split(":", 1)
            if k[0].strip() in variable_to_record:
                d[k[0].strip()] = k[1].strip()
    return d
    # return dict([k.strip() for k in i.split(":", 1)] for i in raw_headers.split('\n'))


def test_record_trans(reader_path):
    """
    Record trans.
    """
    freader = record.RecordReader(reader_path)
    count = 0
    time_start = 0
    for channel_name, msg, datatype, timestamp in freader.read_messages():
        curr_time = float('%.2f' %((float(timestamp))/1000000000.0))
        if count == 0:
            time_start = curr_time
        time_bias = ((curr_time - time_start)*100)/25
        if channel_name == CHANNEL_NAME and time_bias >= count :
        # if channelname == CHANNEL_NAME and time_bias >=count:

            print channel_name, curr_time, freader.get_messagenumber(channel_name)
            desc = freader.get_protodesc(channel_name)
            print("time_bias: ", time_bias)
            count += 1
            print('-' * 80)
            print('read [%d] messages' % count)
            print('channel_name -> %s' % channel_name)
            print('msgtime -> %d' % timestamp)
            print('msgnum -> %d' % freader.get_messagenumber(channel_name))
            print('msgtype -> %s' % datatype)
            # print "pbdesc -> %s" % freader.get_protodesc(channelname)
            print('message is -> %s' % msg)
            print('***After parse(if needed),the message is ->')
            if datatype == MSG_TYPE:
                msg_new = perception_obstacle_pb2.PerceptionObstacles()
                msg_new.ParseFromString(msg)
                # print(msg_new)
                msg_new_str = str(msg_new)
                print(msg_new_str)
                print("end")
                # msg_new_dict = headers_to_dict(msg_new_str)
                # data_list.append(msg_new_dict)
            if datatype == MSG_TYPE_CHATTER:
                msg_new = Chatter()
                msg_new.ParseFromString(msg)
                print(msg_new)

            
if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print('Usage: %s record_file' % sys.argv[0])
    #     sys.exit(0)

    record_path = "/apollo/data/cyber_record/trail-10-11-2021-01-23-52/2021-10-11-01-23-59/20211011012359.record.00000.00000"
    cyber.init()
    # test_record_trans(sys.argv[1])
    test_record_trans(record_path)
    cyber.shutdown()
