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
sys.path.append("/apollo/Cyber")
os.chdir("/apollo/cyber")
from cyber_py import cyber
from cyber_py import record
from modules.control.proto import control_cmd_pb2

MSG_TYPE = "apollo.control.ControlCommand"
CHANNEL_NAME = "/apollo/control"
MSG_TYPE_CHATTER = "apollo.Cyber.proto.Chatter"


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
                msg_new = control_cmd_pb2.ControlCommand()
                msg_new.ParseFromString(msg)
                print(msg_new)
            if datatype == MSG_TYPE_CHATTER:
                msg_new = Chatter()
                msg_new.ParseFromString(msg)
                print(msg_new)

            
if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print('Usage: %s record_file' % sys.argv[0])
    #     sys.exit(0)

    record_path = "/apollo/data/record_files/2021-09-27-11-30-56/20210927113056.record.00000"

    cyber.init()
    # test_record_trans(sys.argv[1])
    test_record_trans(record_path)
    cyber.shutdown()
