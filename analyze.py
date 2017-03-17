"""Analyze the result."""


# import os
# import sys
from itertools import permutations
from decimal import *
from functools import *
import pygal


def getTimeOut(filename):
        if filename[1] == 'E':
            return 60
        elif filename[1] == 'M':
            return 120
        else:
            if filename[2] in ['1', '2']:
                return 600
            else:
                return 1200


class performance:

    def __init__(self, fn, comid, com, back, ass, tt):
        self.filename = fn
        self.combid = int(comid)
        self.combination = com
        self.backtracks = int(back)
        self.assignments = int(ass)
        self.total_time = Decimal(tt)
        self.backtrack_avgtime = Decimal(0)
        if self.backtracks != 0:
            self.backtrack_avgtime = Decimal(tt)/Decimal(back)

    def difficulty_index(self):
        if self.filename[1] == 'E':
            return 0
        elif self.filename[1] == 'M':
            return 1
        else:
            return 2


class combination:
    def __init__(self, name):
        self.name = name
        self.list = []
        self.nonlist = []
        self.esum = 0
        self.ecount = 0
        self.msum = 0
        self.mcount = 0
        self.hsum = 0
        self.hcount = 0

    def add(self, data):
        for item in self.list:
            if item.combid == data.combid:
                item.add(data)

    def easyavg(self):
        sum = 0
        count = 0
        for item in self.list:
            sum += item.easyavg()
            count += 1
        return sum/count

    def mediumavg(self):
        sum = Decimal(0)
        count = 0
        for item in self.list:
            sum += item.mediumavg()
            count += 1
        return sum/count

    def hardavg(self):
        sum = 0
        count = 0
        for item in self.list:
            sum += item.hardavg()
            count += 1
        return sum/count


class combinationIndiv:
    def __init__(self, combid, combName):
        self.combid = combid
        self.combName = combName
        self.list = []
        self.esum = 0
        self.ecount = 0
        self.msum = 0
        self.mcount = 0
        self.hsum = 0
        self.hcount = 0
        self.disable = False

    def getcombStr(self):
        ss = str()
        for i in self.combName[0]:
            if i == 'ForwardChecking':
                ss += 'FC '
            elif i == 'ArcConsistency':
                ss += 'AC '
            else:
                ss += i+' '
        for i in range(1, 2):
            if self.combName[i] != 'None':
                ss += self.combName[i]+' '
        return ss

    def add(self, data):
        time = 0
        if data.total_time == Decimal('Infinity'):
            self.disable = True
            time = getTimeOut(data.filename)
        else:
            time = data.total_time
        if data.filename[1] == 'E':
            self.esum += time
            self.ecount += 1
        elif data.filename[1] == 'M':
            self.msum += time
            self.mcount += 1
        elif data.filename[1] == 'H':
            self.hsum += time
            self.hcount += 1
        self.list.append(data)

    def easyavg(self):
        return Decimal(self.esum / self.ecount)

    def mediumavg(self):
        return Decimal(self.msum / self.mcount)

    def hardavg(self):
        return Decimal(self.hsum / self.hcount)


difficulty_data = ['PE', 'PM', 'PH']
comb_list = []


def main():

    getcontext().prec = 4
    combinations = []

    consisList = ['ForwardChecking', 'ArcConsistency', 'NKD', 'NKT']
    Varlist = ['MRV', 'DH']
    Vallist = ['LCV']
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
                    combinations.append([consisChkPermute, VarH, ValH])

    plist = [[] for x in range(15)]  # 15 different test files PE1 -- PH5
    # dlist = [[] for x in range(3)]   # 3 different difficulties
    combPerformance = [combinationIndiv(xi, x)
                       for xi, x in enumerate(combinations)]  # performance

    clist = [combination(x) for x in consisList]
    for item in combPerformance:
        for citem in clist:
            if citem.name in item.combName[0]:
                citem.list.append(item)

    vlist = [combination(x) for x in Varlist]  # mrv or dh
    for item in combPerformance:
        for citem in vlist:
            if citem.name in item.combName:
                citem.list.append(item)

    lcvlist = [combination(x) for x in Vallist]  # lcv
    for item in combPerformance:
        for citem in lcvlist:
            if citem.name in item.combName:
                citem.list.append(item)

    for diffIndex, difficultyname in enumerate(difficulty_data):
        file = open('log/'+difficultyname+'.txt', 'r')
        next(file)
        for i in range(5):
            filename = file.readline().split('\n')[0]
            filenamenum = int(filename[2])
            for j in range(390):
                lresult = file.readline().split()
                combinationid = int(lresult[0])
                perfor = (performance(filename,
                          combinationid, combinations[combinationid-1],
                          lresult[1], lresult[2], lresult[3]))
                combPerformance[combinationid-1].add(perfor)
                plist[diffIndex*5+filenamenum-1].append(perfor)
                for cindex, consisCheck in enumerate(consisList):
                    if consisCheck in perfor.combination[0]:
                        clist[cindex].add(perfor)
                    else:
                        clist[cindex].nonlist.append(perfor)
                for vindex, varh in enumerate(Varlist):
                    if varh in perfor.combination:
                        vlist[vindex].add(perfor)
                    else:
                        vlist[vindex].nonlist.append(perfor)
                for lindex, valh in enumerate(Vallist):
                    if valh in perfor.combination:
                        lcvlist[lindex].add(perfor)
                    else:
                        lcvlist[lindex].nonlist.append(perfor)

    # nonlist
    nonsum = [0 for x in range(3)]
    noncount = [0 for x in range(3)]
    # for com in clist:
    #     line_chart = pygal.Line()
    #     line_chart.title = com.name+' VS Without '+com.name
    #     line_chart.x_labels = difficulty_data
    #     for index,item in enumerate(com.nonlist):
    #         time = Decimal(item.total_time)
    #         if item.total_time == Decimal('Infinity'):
    #             time = getTimeOut(item.filename)
    #         nonsum[item.difficulty_index()] += time;
    #         noncount[item.difficulty_index()] += 1
    #     line_chart.add(com.name,[com.easyavg(),com.mediumavg(),com.hardavg()])
    #     line_chart.add('Without '+com.name,[nonsum[0]/noncount[0],
    #                                         nonsum[1]/noncount[1],
    #                                         nonsum[2]/noncount[2]])
    #     line_chart.render_to_png('report/VS'+com.name+'.png')
    #     nonsum = [0 for x in range(3)]
    #     noncount = [0 for x in range(3)]

    for com in vlist:
        line_chart = pygal.Line()
        line_chart.title = com.name+' VS Without '+com.name
        line_chart.x_labels = difficulty_data
        for index, item in enumerate(com.nonlist):
            time = Decimal(item.total_time)
            if item.total_time == Decimal('Infinity'):
                time = getTimeOut(item.filename)
            nonsum[item.difficulty_index()] += time
            noncount[item.difficulty_index()] += 1
        print(com.easyavg())
        line_chart.add(com.name, [com.easyavg(),
                                  com.mediumavg(), com.hardavg()])
        line_chart.add('Without '+com.name, [nonsum[0]/noncount[0],
                                             nonsum[1]/noncount[1],
                                             nonsum[2]/noncount[2]])
        line_chart.render_to_png('report/VS'+com.name+'.png')
        nonsum = [0 for x in range(3)]
        noncount = [0 for x in range(3)]

    for com in lcvlist:
        line_chart = pygal.Line()
        line_chart.title = com.name+' VS Without '+com.name
        line_chart.x_labels = difficulty_data
        for index, item in enumerate(com.nonlist):
            time = Decimal(item.total_time)
            if item.total_time == Decimal('Infinity'):
                time = getTimeOut(item.filename)
            nonsum[item.difficulty_index()] += time
            noncount[item.difficulty_index()] += 1
        line_chart.add(com.name, [com.easyavg(),
                                  com.mediumavg(),
                                  com.hardavg()])
        line_chart.add('Without '+com.name, [nonsum[0]/noncount[0],
                                             nonsum[1]/noncount[1],
                                             nonsum[2]/noncount[2]])
        line_chart.render_to_png('report/VS'+com.name+'.png')
        nonsum = [0 for x in range(3)]
        noncount = [0 for x in range(3)]

    # for com in clist:
    #     line_chart = pygal.Line()
    #     line_chart.title = com.name
    #     line_chart.x_labels = difficulty_data
    #     for item in com.list:
    #         if not item.disable:
    #             if item.combName[0][0] == com.name:
    #                 line_chart.add(item.getcombStr(),[item.easyavg(),item.mediumavg(),item.hardavg()])
    #     line_chart.render_to_png('report/'+com.name+'.png')
    #     line_chart.title = com.name+' VS none'+com.name

    # output = open('report/analyze_combination.txt','w')
    # for i in range(390):
    #     id = combPerformance[i].list[0].combid
    #     output.write(str(id)+' '+str(combinations[id-1])+'\n\n')
    #     sumBacktracks = 0
    #     sumAssignments = 0
    #     sumSolutions = 0
    #     sumtime = Decimal(0)
    #     for iindex,item in enumerate(combPerformance[i].list):
    #         issolved = item.total_time != Decimal('Infinity')
    #         if issolved:
    #             sumSolutions += 1
    #         sumBacktracks += item.backtracks
    #         sumAssignments += item.assignments
    #         sumtime += item.total_time
    #         output.write(item.filename+' Time='+str(item.total_time)+
    #                      's Backtracks='+str(item.backtracks)+
    #                      ' Assignments='+str(item.assignments)+
    #                      ' Solved='+str(issolved)+'  AvgBacktrackTime='+
    #                      str(item.backtrack_avgtime)+'\n')
    #         if (iindex+1) %5==0:
    #             output.write("\nSolution:"+str(sumSolutions)+"/5\n:")
    #             output.write("Avg runtime: "+str(sumtime/5)+
    #                 " Avg Backtracks: "+str(sumBacktracks/5)+
    #                 " Avg Assignments: "+str(sumAssignments/5)+"\n")
    #             sumBacktracks = sumAssignments = sumSolutions = 0
    #             sumtime = Decimal(0)
    #             output.write('\n')
    #     output.write('\n')
    # output.close()

    # top40_list = [[] for x in range(15)]
    # pout = open('report/analyze_problem.txt','w')
    # for i in range(15):
    #     pout.write(plist[i][0].filename+'\n')
    #     successes = 0
    #     backtracks_sum = 0
    #     for j,item in enumerate(plist[i]):
    #         backtracks_sum += int(item.backtracks)
    #         if item.total_time != Decimal('Infinity'):
    #             successes += 1
    #     sucrate = Decimal(successes)/Decimal(390)
    #     pout.write("Success Rate="+str(sucrate)+'\n')
    #     avgBacktracks = Decimal(backtracks_sum) / Decimal(390)
    #     pout.write("Average Backtracks="+str(avgBacktracks)+'\n\n')

    #     pout.write("Top 80 Solutions:\n")

    #     for k in range(80):
    #         item = plist[i][k]
    #         id = item.combid
    #         issolved = item.total_time != Decimal('Infinity')
    #         if issolved:
    #             top40_list[i].append(item)
    #         pout.write(str(combinations[id-1])+' '+
    #             str(id)+'  Total Time='+str(item.total_time)+
    #             '  Backtracks='+str(item.backtracks)+'  AvgBacktrackTime='+
    #             str(item.backtrack_avgtime)+'\n\n')
    #     pout.write('\n')
    # pout.close()

    # for i in range(15):
    #     plist[i].sort(key=lambda perfor: perfor.total_time)

    # best_combs = [[] for x in range(15)]
    # for i in range(15):
    #     best_combs[i] = [x.combid for x in top40_list[i]]
    # # for i in [0,5,10]:
    # #     result = reduce(set.intersection, map(set, best_combs[i:i+5]))
    # #     print(result)
    # #     print()
    # result = reduce(set.intersection, map(set, best_combs))
    # line_chart = pygal.Line()
    # line_chart.title = "Top Solutions"
    # line_chart.x_labels = difficulty_data
    # for item in combPerformance:
    #     if item.combid in result:
    #         line_chart.add(item.getcombStr(),[item.easyavg(),
    #                        item.mediumavg(),item.hardavg()])
    # line_chart.render_to_png('report/Top Solutions.png')


if __name__ == '__main__':
    main()
