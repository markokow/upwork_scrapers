import os
import shutil
from os import walk
def sort_files(path,sort_type):
    files = []
    for (dirpath, dirnames, filenames) in walk(path):
        files.extend(filenames)
        break
    if sort_type == 'ext':
        if path[-1]!='/':
            path = path + '/'
        extention_dict = {}
        for file in files:
            name,ext = os.path.splitext(file)
            if ext=='':
                key = 'file'
            else:
                key = ext[1:]
            if key in extention_dict:
                extention_dict[key].append(file)
            else:
                extention_dict[key] = []
                extention_dict[key].append(file)
        
        for key,value in extention_dict.items():
            if os.path.isdir(path+key):
                for file in value:
                    shutil.move(path+file,path+key+"/"+file)
            else:
                os.mkdir(path+key)
                for file in value:
                    shutil.move(path+file,path+key+"/"+file)

    elif sort_type=='size':
        if path[-1]!='/':
            path = path + '/'
        size_dict = {
            'small_files':[],
            'medium_files':[],
            'large_files':[]
            }
        for file in files:
            fs = os.stat(path+file).st_size
            scale = 1024*1024
            fs = fs/scale
            if fs < 100:
                size_dict['small_files'].append(file)
            elif fs < 500:
                size_dict['medium_files'].append(file)
            else:
                size_dict['large_files'].append(file)

        for key,value in size_dict.items():
            if os.path.isdir(path+key):
                for file in value:
                    shutil.move(path+file,path+key+"/"+file)
            else:
                os.mkdir(path+key)
                for file in value:
                    shutil.move(path+file,path+key+"/"+file)
