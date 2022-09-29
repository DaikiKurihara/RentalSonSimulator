import numpy as np
import matplotlib.pyplot as plt

class contractorSimuration():

    def __init__(self, Nm, Rl, Rs, Rt, *args):
        """
        Nm	[people]	月訪問者数			   10 people
        Rl	[-]		    長期契約率			   2.5 %
        Rs	[-]		    短期契約率			   10 %
        Rt	[-]		    単発率                  20 %
        M	[month]	    シミュレーション期間    6 months

        Nc	[people]	現契約者数			    6 people
        S	[yen]		売上				    1e3 yen

        Nl  [people]    月長期契約者数          2 poeple
        Ns  [people]    月短期契約者数          10 poeple
        Nt  [people]    月単発人数              20 poeple

        defaultDuration: 平均契約月数
        """
        self.Nm = Nm
        self.Rl = Rl
        self.Rs = Rs
        self.Rt = Rt
        self.args = args

        self.defaultDurationl = 4
        self.defaultDurations = 1
        self.defaultDurationt = 0

        self.contractDurationl = np.empty(0)
        self.contractDurations = np.empty(0)
        self.contractDurationt = np.empty(0)
    
    def genVisitors(self):
        Nl = np.round(self.Nm * self.Rl)
        Ns = np.round(self.Nm * self.Rs)
        Nt = np.round(self.Nm * self.Rt)
        self.contractDurationl = np.concatenate([self.contractDurationl, self.setDuration(Nl, 'long')])
        self.contractDurations = np.concatenate([self.contractDurations, self.setDuration(Ns, 'short')])
        self.contractDurationt = np.concatenate([self.contractDurationt, self.setDuration(Nt, 'trial')])
        return self.Nm

    def setDuration(self, N, type):
        if type is 'long':
            return np.ones(int(N)) * self.defaultDurationl
        elif type is 'short':
            return np.ones(int(N)) * self.defaultDurations
        elif type is 'trial':
            return np.ones(int(N)) * self.defaultDurationt

    def stepMonth(self):
        self.contractDurationl -= 1
        self.contractDurations -= 1
        self.contractDurationt -= 1
        idxl = self.contractDurationl >= 0
        idxs = self.contractDurations >= 0
        idxt = self.contractDurationt >= 0
        self.contractDurationl = self.contractDurationl[idxl]
        self.contractDurations = self.contractDurations[idxs]
        self.contractDurationt = self.contractDurationt[idxt]
        

if __name__ == '__main__':
    sim = contractorSimuration(100, 2.5e-2, 10e-2, 20e-2)
    for n in range(6):
        sim.genVisitors()
        sim.stepMonth()
