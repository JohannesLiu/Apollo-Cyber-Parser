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
import pickle
from msgtools import File, Parser

MSG_TYPE = "apollo.perception.PerceptionObstacles"
CHANNEL_NAME = "/apollo/perception/obstacles"
MSG_TYPE_CHATTER = "apollo.cyber.proto.Chatter"

# variable_to_record = ['brake', 'accleration', 'steering_rate', 'steering_target', 'speed', 'throttle']


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

def test_record_trans(reader_path):
    """
    Record trans.
    """
    data_list = list()
    header_parser = Parser.HeaderParser("Perception")

    
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
                data_list.append(header_parser.parse(msg_new_str))
                
                # msg_new_dict = headers_to_dict(msg_new_str)
                # data_list.append(msg_new_dict)
            if datatype == MSG_TYPE_CHATTER:
                msg_new = Chatter()
                msg_new.ParseFromString(msg)
                print(msg_new)
    return data_list
            
if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print('Usage: %s record_file' % sys.argv[0])
    #     sys.exit(0)

    trail_name = "trail-10-20-2021-07-52-34"
    trail_path = "/apollo/data/cyber_record/" + trail_name + "/"
    record_path_list=[]
    # Record_list: Storage record list 
    record_list = []    
    
    FileList = File.FileList()
    FileList.listdir_top(trail_path, record_path_list)
    for path in record_path_list:
        
        file_path_list = []
        FileList.listdir_bottom(path, file_path_list)
        file_path_list.sort()
        file_path_list = file_path_list[:-1]

        data_list = [] 
        cyber.init()
        # test_record_trans(sys.argv[1])
        for record_path in file_path_list:
            data_list.extend(test_record_trans(record_path))
        record_list.append(data_list)
        cyber.shutdown()    
    

    saveList(record_list, '/apollo/record_perception_obstacles.pkl_'+ trail_name + '.pkl')
    rlist = loadList('/apollo/record_perception_obstacles.pkl_'+ trail_name + '.pkl')
