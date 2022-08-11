import numpy as np
import matplotlib.pyplot as plt

class Parents():

    def __init__(self) -> None:
        self.parentsList = []
        self.total = 0
        self.NHist = []
        self.returnRate = 0.01

    def gen(self, N):
        self.total += N
        self.NHist.append(int(N))
        for _ in range(int(N)):
            self.parentsList.append(Parson())
    
    def step(self):
        nDiscon = 0
        for p in self.parentsList:
            p.step()
            if p.contractType == 'discontinue':
                nDiscon += 1
        print(nDiscon)
        nReturnParents = np.floor(nDiscon * self.returnRate)
        nReturn = 0
        for p in self.parentsList:
            if p.contractType == 'discontinue':
                nReturn += 1
                p.setContractTypeReturn()
                print('call')
                if nReturnParents <= nReturn:
                    break

    def statistics(self, type=None):
        dShortMean, dLongMean, dReturnMean = 0, 0, 0
        nLong, nShort, nReturn, nDiscon = 0, 0, 0, 0
        for p in self.parentsList:
            if p.durationType == 'short':
                dShortMean += p.duration
                nShort += 1
            elif p.durationType == 'long':
                dLongMean += p.duration
                nLong += 1
            elif p.durationType == 'return':
                nReturn += 1
                dReturnMean += p.duration
            if p.contractType == 'discontinue':
                nDiscon += 1
        if nShort > 0:
            dShortMean /= nShort
        if nLong > 0:
            dLongMean /= nLong
        if nReturn > 0:
            dReturnMean /= nReturn
        return nShort, dShortMean, nLong, dLongMean, nReturn, dReturnMean, nDiscon

class Parson():

    def __init__(self) -> None:
        #%% long short stranger initialized
        longTermContractRate = 0.025 + (np.random.rand()-0.5) * 2 * 0.005
        shortTermContractRate = 0.1 + (np.random.rand()-0.5) * 2 * 0.02
        d = np.random.rand()
        if d < longTermContractRate:
            self.setContractTypeLong()
        elif d < shortTermContractRate + longTermContractRate:
            self.setContractTypeShort()
        else:
            self.setContractTypeStranger()
        self.durationHist = []
        self.contractTypeHist = []
        self.duration = 0
        self.discontinueRate = 0.01
    
    def step(self):
        #%% condition: person who is in "continue" or "new"
        if self.contractStatus == 1:
            self.duration += 1
            rate = np.random.rand()
            #%% contract ducation short and long terms
            if self.duration >= self.durationThreshold:
                self.discontinueRate = 0.9
                self.contractType = 'continue'
            if rate < self.discontinueRate:
                self.contractStatus = -1
                self.contractType = 'discontinue'
    
    def setContractTypeLong(self):
        self.contractStatus = 1
        self.contractType = 'new'
        self.durationThreshold = 4
        self.durationType = 'long'

    def setContractTypeShort(self):
        self.contractStatus = 1
        self.contractType = 'new'
        self.durationThreshold = 1
        self.durationType = 'short'

    def setContractTypeStranger(self):
        self.contractStatus = 0
        self.contractType = 'NA'
        self.durationThreshold = 0
        self.durationType = 'stranger'

    def setContractTypeReturn(self):
        #%% condition: person who has made a contract at least once
        if self.contractStatus == -1:
            self.durationHist.append(self.duration)
            self.contractTypeHist.append(self.contractType)
            self.duration = 0
            self.contractStatus = 1
            self.contractType = 'return'
            self.durationThreshold = 12
            self.durationType = 'return'

    def __repr__(self) -> str:
        s = 'Parson class\n'
        s += 'Type: %s\n' %self.durationType
        s += 'Duration: %s month\n' %self.duration
        s += 'Status: %d' %self.status
        return s


def contractorStatusCheck(contractorList):
    nNew, nNewShort, nNewLong, nReturn, nContract = 0, 0, 0, 0, 0
    nShort, nLong = 0, 0
    for p in contractorList:
        if p.contractType == 'new':
            nNew += 1
            if p.durationType == 'short':
                nNewShort += 1
            elif p.durationType == 'long':
                nNewLong += 1
        if p.durationType == 'short':
            nShort += 1
        if p.durationType == 'long':
            nLong += 1
        if p.contractType == 'return':
            nReturn += 1
        if p.contractStatus == 1:
            nContract += 1
    nTotal = len(contractorList)
    out = [nNew, nNewShort, nNewLong, nReturn, nContract, nTotal, nShort, nLong]
    return out

def initializationCheck(N):
    #%% initialization check
    nLong, nShort = 0, 0
    a = []
    for _ in range(int(N)):
        a.append(Parson())
    for p in a:
        if p.durationType == 'short':
            nShort += 1
        elif p.durationType == 'long':
            nLong += 1
    print('%d [%.2f] %d [%.2f] %d' %(nShort, 100*nShort/N, nLong, 100*nLong/N, N))
    return a

def durationCheck(nParson, nMonth):
    nLong, nShort = 0, 0
    a = []
    for _ in range(int(nParson)):
        a.append(Parson())
    for _ in range(nMonth):
        for p in a:
            p.step()
    dShortMean, dLongMean = 0, 0
    nLong, nShort = 0, 0
    for p in a:
        if p.durationType == 'short':
            dShortMean += p.duration
            nShort += 1
        elif p.durationType == 'long':
            dLongMean += p.duration
            nLong += 1
    dShortMean /= nShort
    dLongMean /= nLong
    print('%d [%.2f] %d [%.2f] %d' %(nShort, dShortMean, nLong, dLongMean, nParson))

def returnRateCheck(nParson, nMonth):
    nLong, nShort = 0, 0
    a = []
    parents = Parents()
    parents.gen(nParson)
    for _ in range(nMonth):
        parents.step()
    nShort, dShortMean, nLong, dLongMean, nReturn, dReturnMean, nDiscon = parents.statistics()
    print('%d [%.2f] %d [%.2f] %d [%.2f] %d, (%d)' %(nShort, dShortMean, nLong, dLongMean, nReturn, dReturnMean, nParson, nDiscon))



if __name__ == '__main__':
    # initializationCheck(20e3)
    # durationCheck(20e3, 12)
    returnRateCheck(2e3, 120)

    # nParson = 0
    # contractorList = []
    # for n in range(12):
    #     newContractorCandidates = 20 + np.round((np.random.rand()-0.5) * 2 * 10)
    #     if newContractorCandidates < 0:
    #         newContractorCandidates = 0
    #     nParson += newContractorCandidates
    #     for _ in range(int(newContractorCandidates)):
    #         contractorList.append(Parson())
    #     for p in contractorList:
    #         p.step()
    #     nNew, nNewShort, nNewLong, nReturn, nContract, nTotal, nShort, nLong = contractorStatusCheck(contractorList)
    #     print('total: %4d (cont: %4d)' %(newContractorCandidates, nContract))





        # print('[%04d m] total: %4d, contract: %4d, New: %4d (S%4d:L%4d), Return: %4d' %(n+1, nTotal, nContract, nNew, nNewShort, nNewLong, nReturn))
    # for p in contractorList:
    #     if p.duration != 0:
    #         print('duration: %d' %p.duration)

