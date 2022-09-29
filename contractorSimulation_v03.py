import numpy as np
import matplotlib.pyplot as plt

class contractorSimuration():

    def __init__(self, Nm, Rl, Rs, Rt, *args, **kwargs):
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

        Ndiscon: 契約終了者累計
        Mcurrent: 経過月数

        defaultDuration: 平均契約月数
        """
        self.Nm = Nm
        self.Rl = Rl
        self.Rs = Rs
        self.Rt = Rt
        self.Ndiscon = 0
        self.Mcurrent = 0

        self.parseOptionalDictionary(kwargs)
        self.setDefaultDurations()
        self.initializeContractDuration()

    def setDefaultDurations(self):
        """
        契約期間デフォルト値の設定
        """
        self.defaultDurationl = 4
        self.defaultDurations = 1
        self.defaultDurationt = 0


    def initializeContractDuration(self):
        """
        ContractDuration の初期化
        """
        self.contractDurationl = np.empty(0)
        self.contractDurations = np.empty(0)
        self.contractDurationt = np.empty(0)

    def genVisitors(self):
        """
        月訪問者の生成
        """
        Nl = np.round(self.Nm * self.Rl)
        Ns = np.round(self.Nm * self.Rs)
        Nt = np.round(self.Nm * self.Rt)
        self.contractDurationl = np.concatenate([self.contractDurationl, self.setDuration(Nl, 'long')])
        self.contractDurations = np.concatenate([self.contractDurations, self.setDuration(Ns, 'short')])
        self.contractDurationt = np.concatenate([self.contractDurationt, self.setDuration(Nt, 'trial')])
        return self.Nm

    def setDuration(self, N, type):
        """
        契約タイプに合わせた契約期間の設定
        """
        if type == 'long':
            return np.ones(int(N)) * self.defaultDurationl
        elif type == 'short':
            return np.ones(int(N)) * self.defaultDurations
        elif type == 'trial':
            return np.ones(int(N)) * self.defaultDurationt

    def stepMonth(self):
        """
        月ごとの全体処理
        """
        self.Mcurrent += 1
        self.contractDurationl -= 1
        self.contractDurations -= 1
        self.contractDurationt -= 1
        idxl = self.contractDurationl >= 0
        idxs = self.contractDurations >= 0
        idxt = self.contractDurationt >= 0

        for contD, idx in zip([self.contractDurationl, self.contractDurations, self.contractDurationt], [idxl, idxs, idxt]):
            self.Ndiscon += len(contD[np.logical_not(idx)])

        self.contractDurationl = self.contractDurationl[idxl]
        self.contractDurations = self.contractDurations[idxs]
        self.contractDurationt = self.contractDurationt[idxt]
    
    def parseOptionalDictionary(self, dic):
        for key, val in dic.items():
            pass

    def countCurrentContractor(self):
        """
        契約終了者累計計算
        """
        out = []
        for con in [self.contractDurationl, self.contractDurations, self.contractDurationt]:
            out.append(len(con))
        return out
    
    def __repr__(self) -> str:
        s = '{} class instance\n'.format(type(self).__name__)
        dic = self.__dict__
        for key in dic:
            s += '  {} : {}\n'.format(key, dic[key])
        return s[:-1]

def case1Defaults(self):
    self.defaultDurationl = 12
    self.defaultDurations = 2
    self.defaultDurationt = 1


if __name__ == '__main__':
    # sim = contractorSimuration(100, 2.5e-2, 10e-2, 20e-2)
    sim = contractorSimuration(100, 2.5e-2, 10e-2, 20e-2, 10, test=2.0, a='a')
    case1Defaults(sim)

    print(sim)
    for n in range(6):
        sim.genVisitors()
        sim.stepMonth()
        print(sim.countCurrentContractor())

    print(sim)
    print('program end')
