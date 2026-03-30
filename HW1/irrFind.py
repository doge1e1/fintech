import numpy as np
from scipy import optimize
from scipy.optimize import fsolve
def irrFind(cashFlowVec, cashFlowPeriod, compoundPeriod):
    def npv(rate, cashflows, cashFlowPeriod, compoundPeriod):
        periods = np.arange(len(cashflows))
        if compoundPeriod == 12:  # 年複利
            discount_factors = (1 + rate) ** (-periods * cashFlowPeriod / 12)
        elif compoundPeriod == 6:  # 半年複利
            discount_factors = (1 + rate/2) ** (-periods * cashFlowPeriod / 6)
        elif compoundPeriod == 4:  # 季複利
            discount_factors = (1 + rate/3) ** (-periods * cashFlowPeriod / 4)
        elif compoundPeriod == 3:  # 四月複利
            discount_factors = (1 + rate/4) ** (-periods * cashFlowPeriod / 3)
        elif compoundPeriod == 2:  # 二月複利
            discount_factors = (1 + rate/6) ** (-periods * cashFlowPeriod / 2)
        elif compoundPeriod == 1:  # 月複利
            discount_factors = (1 + rate/12) ** (-periods * cashFlowPeriod)
        else:
            raise ValueError("compoundPeriod must be 1, 2, 3, 4, 6, or 12")
        
        return np.sum(np.array(cashflows) * discount_factors)

    def irr_equation(rate):
        return npv(rate, cashFlowVec, cashFlowPeriod, compoundPeriod)

    initial_guesses = [-0.00521]
    for guess in initial_guesses:
        try:
            irr_solution, infodict, ier, mesg = fsolve(irr_equation, guess, full_output=True)
            if ier == 1: 
                if abs(irr_solution[0]) < 1e-6: 
                    return 0
                return irr_solution[0]
        except:
            continue
    return 0
