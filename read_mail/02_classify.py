#coding:utf-8

import os
import os.path

rootdir = 'F:\\alibaba\\read_mail\\3.5'
non_tech = 0
tech = 0

tech_dir = '3.5_tech'
nontech_dir = '3.5_nontech'

for parents, dirnames, filenames in os.walk(rootdir):
    for i in range(0, len(filenames)):
        if parents!=rootdir:
            break
        
        cur_str = filenames[i]
        if '\xb2\xfa\xc6\xb7' in cur_str or '\xd3\xce\xcf\xb7\xc4\xda\xc8\xdd\xd4\xcb\xd3\xaa' in cur_str or '\xd3\xce\xcf\xb7\xd4\xcb\xd3\xaa\xd7\xa8\xd4\xb1' in cur_str or '\xb9\xa4\xd2\xd5\xb9\xa4\xb3\xcc\xca\xa6' in cur_str or '\xbd\xbb\xbb\xa5\xc9\xe8\xbc\xc6\xca\xa6' in cur_str or '\xca\xd3\xbe\xf5\xc9\xe8\xbc\xc6\xca\xa6' in cur_str:
            if i==0 or filenames[i-1][:22] != filenames[i][:22]:
                non_tech += 1
                
            new_file = '%d' % non_tech
            new_file = '0'*(3-len(new_file)) + new_file + ',' + filenames[i]

            new_file = os.path.join(rootdir, nontech_dir, new_file)
            old_file = os.path.join(rootdir, filenames[i])
            command = "copy \"" + old_file + '" "' + new_file + "\""
            print command
            os.system(command)
        else:
            if i==0 or filenames[i-1][:22] != filenames[i][:22]:
                tech += 1
                
            new_file = '%d' % tech
            new_file = '0'*(3-len(new_file)) + new_file + ',' + filenames[i]

            new_file = os.path.join(rootdir, tech_dir, new_file)
            old_file = os.path.join(rootdir, filenames[i])
            command = "copy \"" + old_file + '" "' + new_file + "\""
            print command
            os.system(command)

