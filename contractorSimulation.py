import numpy as np
import matplotlib.pyplot as plt
from torch import empty


class Parson():

    def __init__(self) -> None:
        #%% long short stranger initialized
        longTermContractRate = 0.025 + (np.random.rand()-0.5) * 2 * 0.005
        shortTermContractRate = 0.1 + (np.random.rand()-0.5) * 2 * 0.02
        d = np.random.rand()
        if d < longTermContractRate:
            self.durationType = 'long'
        elif d < shortTermContractRate + longTermContractRate:
            self.durationType = 'short'
        else:
            self.durationType = 'stranger'
        self.durationHist = []
        self.contractTypeHist = []
        self.returnRate = 0.01
        self.duration = 0
        self.discontinueRate = 0.01
        self.contractStatus = 1
        self.contractType = 'new'
        if self.durationType == 'long':
            self.durationThreshold = 4
        elif self.durationType == 'short':
            self.durationThreshold = 1
        elif self.durationType == 'stranger':
            self.durationThreshold = 0
            self.contractStatus = 0
            self.contractType = 'NA'
    
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
    
    def contractContenue(self):
            self.contractStatus = 1
            self.contractType = 'continue'
            self.durationThreshold = 12
            self.durationType = 'return'

    def contractReturn(self):
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
    for _ in range(int(nParson)):
        a.append(Parson())
    for _ in range(nMonth):
        for p in a:
            p.step()
    dShortMean, dLongMean, dReturnMean = 0, 0, 0
    nLong, nShort, nReturn = 0, 0, 0
    for p in a:
        if p.durationType == 'short':
            dShortMean += p.duration
            nShort += 1
        elif p.durationType == 'long':
            dLongMean += p.duration
            nLong += 1
        elif p.durationType == 'return':
            nReturn += 1
            dReturnMean += p.duration
    if nShort > 0:
        dShortMean /= nShort
    if nLong > 0:
        dLongMean /= nLong
    if nReturn > 0:
        dReturnMean /= nReturn
    print('%d [%.2f] %d [%.2f] %d [%.2f] %d' %(nShort, dShortMean, nLong, dLongMean, nReturn, dReturnMean, nParson))



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

