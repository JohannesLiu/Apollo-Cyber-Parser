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

def listdir_top(path, list_name):
    for file in os.listdir(path):  
        file_path = os.path.join(path, file) 
        list_name.append(file_path)

def listdir_bottom(path, list_name):
    for file in os.listdir(path):
        file_path = os.path.join(path, file) 
        list_name.append(file_path)
    
if __name__ == '__main__':            
    path="/apollo/data/cyber_record/trail-10-20-2021-07-52-34/"

    path_list=[]
    listdir_top(path, path_list)

    for path in path_list:
        file_path_list = []
        listdir_bottom(path, file_path_list)
        file_path_list.sort()
        file_path_list = file_path_list[:-1]

        print("file_path_list:", file_path_list)
        print("\n")
        
