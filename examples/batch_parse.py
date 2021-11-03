import sys
import os
sys.path.append("/apollo/cyber")
os.chdir("/apollo/cyber")
from cyber_py import cyber
from cyber_py import record
from modules.control.proto import control_cmd_pb2

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.00000':
                L.append(os.path.join(root, file))
                
def listdir(path, list_name):
    for file in os.listdir(path):  
        file_path = os.path.join(path, file) 
        if os.path.isdir(file_path):  
            listdir(file_path, list_name)  
        elif os.path.splitext(file)[1]=='.00000':  
            list_name.append(file_path)
            
path="/apollo/data/cyber_record/trail-10-11-2021-01-23-52/"

path_list=[]
listdir(path, path_list)

print(path_list)