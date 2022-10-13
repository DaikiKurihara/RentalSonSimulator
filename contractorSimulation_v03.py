import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle


class BaseRepr:
    def __str__(self):
        s = "{} class instance\n".format(type(self).__name__)
        dic = self.__dict__
        for key, val in dic.items():
            temp = "  {} : {}\n".format(key, val)
            if len(temp) >= 64:
                temp = temp[0:30] + " ... " + temp[-30::]
            s += temp
        return s[:-1]

    def __format__(self, __format_spec: str) -> str:
        s = self.__repr__() + "\n"
        return s[:-1]

    def __repr__(self):
        s = "{} object".format(type(self).__name__)
        return s


class ContractorSimuration(BaseRepr):
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
        self.setMedianSales()
        self.initializeContractDuration()

    def setDefaultDurations(self):
        """
        契約期間デフォルト値の設定
        """
        self.defaultDurationl = 4
        self.defaultDurations = 1
        self.defaultDurationt = 1

    def setMedianSales(self):
        self.contractSalesl = 0.98
        self.contractSaless = 0.98
        self.contractSalest = 0.35

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
        self.contractDurationl = np.concatenate([self.contractDurationl, self.setDuration(Nl, "long")])
        self.contractDurations = np.concatenate([self.contractDurations, self.setDuration(Ns, "short")])
        self.contractDurationt = np.concatenate([self.contractDurationt, self.setDuration(Nt, "trial")])
        return self.Nm

    def setDuration(self, N, type):
        """
        契約タイプに合わせた契約期間の設定
        """
        if type == "long":
            return np.ones(int(N)) * self.defaultDurationl
        elif type == "short":
            return np.ones(int(N)) * self.defaultDurations
        elif type == "trial":
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
        # やめた人数カウント
        for contD, idx in zip(
            [self.contractDurationl, self.contractDurations, self.contractDurationt], [idxl, idxs, idxt]
        ):
            self.Ndiscon += len(contD[np.logical_not(idx)])
        # 継続だけ残す
        self.contractDurationl = self.contractDurationl[idxl]
        self.contractDurations = self.contractDurations[idxs]
        self.contractDurationt = self.contractDurationt[idxt]

    def parseOptionalDictionary(self, dic):
        for key, val in dic.items():
            pass

    def countCurrentContractor(self):
        """
        契約者数計計算
        """
        out = []
        for con in [self.contractDurationl, self.contractDurations, self.contractDurationt]:
            out.append(len(con))
        return out

    def computeSales(self):
        N = [len(contD) for contD in [self.contractDurationl, self.contractDurations, self.contractDurationt]]
        saleTemp = [self.contractSalesl, self.contractSaless, self.contractSalest]
        sale = [n * s for n, s in zip(N, saleTemp)]
        totalN = sum(N)
        totalSales = sum(sale)
        return totalN, totalSales, N, sale


class Log(BaseRepr):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        if kwargs:
            self.assignVariable(kwargs["kwargs"])

    def assignVariable(self, attributes: dict) -> None:
        for name, val in attributes.items():
            setattr(self, name, val)

    def copy(self):
        return self.__class__(kwargs=self.__dict__)


class Logger(BaseRepr):
    def __init__(self) -> None:
        super().__init__()
        self.logList = []

    def log(self, val):
        self.logList.append(val.copy())

    def save(self, filename):
        with open(filename, "wb") as fobj:
            print("write: %s" % filename)
            pickle.dump(self, fobj, pickle.HIGHEST_PROTOCOL)

    def load(filename):
        with open(filename, "rb") as fobj:
            print("load: %s" % filename)
            obj = pickle.load(fobj)
        return obj


def case1Defaults():
    """
    Nm	[people]	月訪問者数			   10 people
    Rl	[-]		    長期契約率			   2.5 %
    Rs	[-]		    短期契約率			   10 %
    Rt	[-]		    単発率                  20 %
    """
    Nm = 50
    Rl = 2.5e-2
    Rs = 10e-2
    Rt = 20e-2
    sim = ContractorSimuration(Nm, Rl, Rs, Rt)
    sim.defaultDurationl = 12
    sim.defaultDurations = 2
    sim.defaultDurationt = 1
    sim.contractSalesl = 0.98
    sim.contractSaless = 0.98
    sim.contractSalest = 0.35
    return sim


def getVariableList(obj):
    s = obj.__dict__
    varList = []
    for key, val in s.items():
        if not isinstance(val, list):
            varList.append(key)
    return varList


def makePandasDataFrame(obj, key):
    table = []
    for o in obj:
        data = [getattr(o, name) for name in key]
        table.append(data)
    df = pd.DataFrame(table, columns=key)
    return df


def parseLoggerData(log, varList=None):
    if varList is None:
        varList = getVariableList(log.logList[0])
    df = makePandasDataFrame(log.logList, varList)
    return df


if __name__ == "__main__":
    sim = case1Defaults()
    logger = Logger()
    log = Log()

    for n in range(18):
        sim.genVisitors()
        sim.stepMonth()
        totalN, totalSales, N, sale = sim.computeSales()
        print("M[{:2d}] #{:6d}: {:.4f}万円".format(n + 1, totalN, totalSales))
        logDict = {
            "M": sim.Mcurrent,
            "Nm": sim.Nm,
            "Nl": len(sim.contractDurationl),
            "Ns": len(sim.contractDurations),
            "Nt": len(sim.contractDurationt),
            "totalN": totalN,
            "salesl": sale[0],
            "saless": sale[1],
            "salest": sale[2],
            "totalSales": totalSales,
        }
        log.assignVariable(logDict)
        logger.log(log)

    saveDir = "./results"
    key = "test01Log"
    fname = "{}/{}.pkl".format(saveDir, key)
    logger.save(fname)
    # logLoad = Logger.load(fname)
    varList = ["totalN", "totalSales"]
    # df = parseLoggerData(logger, varList)
    df = parseLoggerData(logger)
    df.to_csv("{}/{}.csv".format(saveDir, key), index=False)
    #     print(sim.countCurrentContractor())

    # print(sim)
    print("program end")
