#coding:utf-8

import os
import os.path

rootdir = 'F:\\alibaba\\read_mail\\3.5\\3.5_nontech'

count = 0
f = open(os.path.join(rootdir, 'info.txt'), 'w')

for parents, dirnames, filenames in os.walk(rootdir):
    for i in range(0, len(filenames)):
        if filenames[i] == 'info.txt':
            break
        print filenames[i]

        if len(filenames[i].split('_')) <= 5:
            info = filenames[i].split('_')[0] + '\t' + filenames[i].split('_')[1] + '\t' + filenames[i].split('_')[2] + '\t' + filenames[i].split('_')[3] + '\t' + filenames[i].split('_')[4] + '\n'
        elif len(filenames[i].split('_')) == 6:
            info = filenames[i].split('_')[0] + '\t' + filenames[i].split('_')[1] + '\t' + filenames[i].split('_')[2] + '\t' + filenames[i].split('_')[3] + '\t' + filenames[i].split('_')[4] + '\t' + filenames[i].split('_')[5] + '\n'
        else:
            info = filenames[i].split('_')[0] + '\t' + filenames[i].split('_')[1] + '\t' + filenames[i].split('_')[2] + '\t' + filenames[i].split('_')[3] + '\t' + filenames[i].split('_')[4] + '\t' + filenames[i].split('_')[5] + '\t' + filenames[i].split('_')[6] + '\n'
        f.write(info)

f.close()
