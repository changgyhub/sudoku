import os
import sys
import filereader
import btsolver
import signal
import time
from itertools import permutations
from decimal import *

def main():
    combinations = []
    consisList = ['ForwardChecking', 'ArcConsistency', 'NKD', 'NKT']
    headline = 'id numBacktracks numAssignments avgtime'
    combid = 0
    timeHeap = []
    for consisNum in range(16):
        consisChk = []
        consisBits = "{0:04b}".format(consisNum)
        for bit, consisBit in enumerate(consisBits):
            if consisBit == '1':
                consisChk.append(consisList[bit])
        if not consisChk:
            consisChk = ['None']
        for consisChkPermute in permutations(consisChk):
            for VarH in ['None', 'MRV', 'DH']:
                for ValH in ['None', 'LCV']:
                    combinations.append([consisChkPermute,VarH,ValH])

    plist = [[] for x in range(15)] #15 different test files PE1 -- PH5
    combPerformance = [[] for x in range(390) ] #performance for each combination
    plogs = ['PE','PM','PH']
    for diffIndex, difficultyname in enumerate(plogs):
        file = open('log/'+difficultyname+'.txt','r')
        next(file)
        for i in range(5):
            filename = file.readline().split('\n')[0]
            filenamenum = int(filename[2])
            for j in range(390):
                lresult = file.readline().split()
                combinationid = int(lresult[0])
                perfor = (filename,combinationid,lresult[1],lresult[2],
                    Decimal(lresult[3]))
                combPerformance[combinationid-1].append(perfor)
                plist[diffIndex*5+filenamenum-1].append(perfor)

    # for i in range(15):
    #     sorted(plist[i],key=lambda perfor: perfor[5])
        

    output = open('report/analyze_combination.txt','w')
    for i in range(390):
        id = combPerformance[i][0][1]
        output.write(str(id)+' '+str(combinations[id-1])+'\n')
        for iindex,item in enumerate(combPerformance[i]):
            issolved = item[4] != Decimal('Infinity')
            getcontext().prec = 6
            backtracks = Decimal(item[2])
            avgTimePerBacktrack = 0
            if backtracks != 0:
                avgTimePerBacktrack = Decimal(item[4])/Decimal(backtracks)
            output.write(item[0]+'  Backtracks='+str(item[2])+
                '  Solved='+str(issolved)+'  AvgBacktrackTime='+
                str(avgTimePerBacktrack)+'\n')
            if (iindex+1) %5==0:
                output.write('\n')
        output.write('\n')
    output.close()  

    pout = open('report/analyze_problem.txt','w')
    for i in range(15):
        pout.write(plist[i][0][0]+'\n')
        successes = 0
        backtracks_sum = 0
        for j,item in enumerate(plist[i]):
            if item[4] != Decimal('Infinity'):
                successes += 1
                backtracks_sum += int(item[2])
        sucrate = Decimal(successes)/Decimal(390)
        pout.write("Success Rate="+str(sucrate)+'\n')
        avgBacktracks = Decimal(backtracks_sum) / Decimal(390)
        pout.write("Average Backtracks="+str(avgBacktracks)+'\n\n')
        pout.write("Top Ten Solutions:\n")
        for k in range(10):
            item = plist[i][k]
            id = item[1]
            backtracks = Decimal(item[2])
            avgTimePerBacktrack = 0
            if backtracks != 0:
                avgTimePerBacktrack = Decimal(item[4])/Decimal(backtracks)
            pout.write(str(combinations[id-1])+'  Total Time='+str(item[4])+
                '\n\t  Backtracks='+str(item[2])+
                '  Solved='+str(issolved)+'  AvgBacktrackTime='+
                str(avgTimePerBacktrack)+'\n\n')
        pout.write('\n')
    pout.close()


if __name__ == '__main__':
    main()
