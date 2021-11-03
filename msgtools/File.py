import sys
import os
sys.path.append("/apollo/cyber")
os.chdir("/apollo/cyber")
from cyber_py import cyber
from cyber_py import record
from modules.control.proto import control_cmd_pb2

class FileList:
    def __init__(self, type = "standard"): # dataPath : /+name
        self.type = type

    def file_name(self, file_dir):
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if os.path.splitext(file)[1] == '.00000':
                    L.append(os.path.join(root, file))
                    
    def listdir(self, path, list_name):
        for file in os.listdir(path):  
            file_path = os.path.join(path, file) 
            if os.path.isdir(file_path):  
                self.listdir(file_path, list_name)  
            elif os.path.splitext(file)[1]=='.00000':  
                list_name.append(file_path)
    
    def listdir_top(self, path, list_name):
        for file in os.listdir(path):  
            file_path = os.path.join(path, file) 
            list_name.append(file_path)

    def listdir_bottom(self, path, list_name):
        for file in os.listdir(path):
            file_path = os.path.join(path, file) 
            list_name.append(file_path)
                

    def test(self):
        path="/apollo/data/cyber_record/trail-10-11-2021-01-23-52/"
        path_list=[]
        self.listdir(path, path_list)
        path_list.sort() 
        for path in path_list:
            print(path)

if __name__ == '__main__':
    test_file = FileList()
    test_file.test()
    print('end')