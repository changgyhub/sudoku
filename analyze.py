import os
import sys
from itertools import permutations
from decimal import *




class performance:

    def __init__(self,fn,com,back,ass,tt):
        self.filename = fn
        self.combid = int(com)
        self.backtracks = int(back)
        self.assignments = int(ass)
        self.total_time = Decimal(tt)
        self.backtrack_avgtime = Decimal(0)
        if self.backtracks != 0:
            self.backtrack_avgtime = Decimal(tt)/Decimal(back)


def main():
    getcontext().prec = 6
    combinations = []
    consisList = ['ForwardChecking', 'ArcConsistency', 'NKD', 'NKT']
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
                perfor = (performance(filename,combinationid,lresult[1],lresult[2],
                    lresult[3]))
                combPerformance[combinationid-1].append(perfor)
                plist[diffIndex*5+filenamenum-1].append(perfor)

    # for i in range(15):
    #     sorted(plist[i],key=lambda perfor: perfor[5])
        

    output = open('report/analyze_combination.txt','w')
    for i in range(390):
        id = combPerformance[i][0].combid
        output.write(str(id)+' '+str(combinations[id-1])+'\n')
        for iindex,item in enumerate(combPerformance[i]):
            issolved = item.total_time != Decimal('Infinity')
            output.write(item.filename+'  Backtracks='+str(item.backtracks)+
                '  Solved='+str(issolved)+'  AvgBacktrackTime='+
                str(item.backtrack_avgtime)+'\n')
            if (iindex+1) %5==0:
                output.write('\n')
        output.write('\n')
    output.close()  

    pout = open('report/analyze_problem.txt','w')
    for i in range(15):
        pout.write(plist[i][0].filename+'\n')
        successes = 0
        backtracks_sum = 0
        for j,item in enumerate(plist[i]):
            if item.total_time != Decimal('Infinity'):
                successes += 1
                backtracks_sum += int(item.backtracks)
        sucrate = Decimal(successes)/Decimal(390)
        pout.write("Success Rate="+str(sucrate)+'\n')
        avgBacktracks = Decimal(backtracks_sum) / Decimal(390)
        pout.write("Average Backtracks="+str(avgBacktracks)+'\n\n')
        pout.write("Top Ten Solutions:\n")
        for k in range(10):
            item = plist[i][k]
            id = item.combid
            pout.write(str(combinations[id-1])+'  Total Time='+str(item.total_time)+
                '\n\t  Backtracks='+str(item.backtracks)+
                '  Solved='+str(issolved)+'  AvgBacktrackTime='+
                str(item.backtrack_avgtime)+'\n\n')
        pout.write('\n')
    pout.close()


if __name__ == '__main__':
    main()
