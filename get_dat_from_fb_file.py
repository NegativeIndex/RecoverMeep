#!/usr/bin/env python
import re,sys
import numpy as np
import argparse

# filepath = 'fb-rad-8105175.txt'
# sfile='CY_Ex_F0.500_A300R160C0_L1300L1300.dat'
# collect data from fb file
def get_dat_from_fb_file(filepath,sfile): 

    data=np.empty(shape=(0,2));
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 0
        while line: 
            line=line.strip()
            if re.match('^field decay',line):
                matchobj=re.search('= ([0-9]\.[0-9]*(e-[0-9]+)?)',line)
                try:
                    decay=matchobj.group(1)
                    decay=float(decay)
                except: 
                    decay=10
                data=np.concatenate((data, [[cnt,decay]]), axis=0)
            cnt+=1
            line = fp.readline()
                
    # print(data)
    # print(cnt)
    # get the right section
    maxline=data[data[:,1].argmin(),0]
    mindecay=data[:,1].min()
    # print(maxline)

    # get flux data
    line_f0=0
    line_f1=0
    isfirst=True
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 0
        while line and cnt<=maxline:
            if re.match('^flux',line):
                if isfirst:
                    line_f0=cnt
                    isfirst=False
                else:
                    line_f1=cnt
            else:
                isfirst=True
 
            line = fp.readline()
            cnt+=1

    # copy file and summary
    if sfile:
        sfp=open(sfile,'w')
        print("Decay is {}; save to {}.".format(mindecay,sfile))
    else:
        sfp=sys.stdout
        print("Decay is {}.".format(mindecay))

    with open(filepath) as fp:
        line = fp.readline()
        cnt = 0
        while line and cnt<line_f0:
            line = fp.readline()
            cnt+=1
        while line and cnt<=line_f1:
            sfp.write(line)
            line = fp.readline()
            cnt+=1
          
    

#########################
if __name__=='__main__':
    str4='This function analyzes the an unfinished fb file'
    str5=' and recovers the simulation results.'
    parser=argparse.ArgumentParser(description='\n'.join((str4,str5)) )

    parser.add_argument("-s","--savefile", default=None, 
                        help="Saved file name")

    parser.add_argument("fbfile", default=None, 
                        help="FB file to be analyzed")

    args = parser.parse_args()

    # print(args.fbfile)
    # print(args.savefile)

    # filepath = 'fb-rad-8105175.txt'
    # sfile='CY_Ex_F0.500_A300R160C0_L1300L1300.dat'
    get_dat_from_fb_file(args.fbfile,args.savefile) 
