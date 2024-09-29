from qanalytics.Request import *
from qanalytics.Enum import *

def WriteLogger(pLogger):
    for Log in pLogger.Logs[1:]:
        print(f'[ {Log.Level:7} ] -- {Log.Message}')

def GetConnectionStatus(pDataConfiguration, pLogger):
    return Request(
        '/GetConnectionStatus',
        [(['DataConfiguration'], pDataConfiguration)],
        pLogger
    )

def GetContract(pDataConfiguration, pContractConfiguration, pResults, pLogger):
    return Request(
        '/GetContract',
        [(['DataConfiguration'], pDataConfiguration), (['ContractConfiguration'], pContractConfiguration), (['Contract'], pResults)],
        pLogger
    )

def GetSequence(pResults, pLogger):
    return Request(
        '/GetSequence',
        [(['Sequence'], pResults)],
        pLogger
    )

def GetSchedule(pResults, pLogger):
    return Request(
        '/GetSchedule',
        [(['Schedule'], pResults)],
        pLogger
    )

def GetImpliedVolatilityComputation(pResults, pLogger):
    return Request(
        '/TestImpliedVolatilityComputation',
        [(['ImpliedVolatilityComputationTester'], pResults)],
        pLogger
    )

def GetBlackScholesCalibration(pData, pContract, pModel, pResults, pLogger):
    return Request(
        '/GetBlackScholesCalibration',
        [(['DataConfiguration'], pData), (['ContractConfiguration'], pContract), (['ModelConfiguration'], pModel), (['ModelConfiguration', 'BlackScholesModel'], pResults)],
        pLogger
    )

def GetBlackScholesTermStructureCalibration(pData, pContract, pModel, pResults, pLogger):
    return Request(
        '/GetBlackScholesTermStructureCalibration',
        [(['DataConfiguration'], pData), (['ContractConfiguration'], pContract), (['ModelConfiguration'], pModel), (['ModelConfiguration', 'BlackScholesTermStructureModel'], pResults)],
        pLogger
    )

def GetHestonImpliedVolatility(pResults, pLogger):
    return Request(
        '/GetHestonImpliedVolatility',
        [(['ModelConfiguration', 'HestonStochasticVolatilityModel'], pResults)],
        pLogger
    )

def GetStaticReplication1D(pData, pContract, pPricer, pResults, pLogger):
    return Request(
        '/GetStaticReplication1D',
        [(['DataConfiguration'], pData), (['ContractConfiguration'], pContract), (['PricerConfiguration'], pPricer), (['Pricer', 'StaticReplication1D'], pResults)],
        pLogger
    )

def GetPrice(pData, pContract, pModel, pPricer, pResults, pLogger):
    return Request(
        '/GetPrice',
        [(['DataConfiguration'], pData), (['ContractConfiguration'], pContract), (['ModelConfiguration'], pModel), (['PricerConfiguration'], pPricer), (['Pricer', 'Pricer'], pResults)],
        pLogger
    )

def GetLadder1D(pData, pContract, pModel, pPricer, pResults, pLogger):
    return Request(
        '/GetLadder1D',
        [(['DataConfiguration'], pData), (['ContractConfiguration'], pContract), (['ModelConfiguration'], pModel), (['PricerConfiguration'], pPricer), (['Pricer', 'Ladder1D'], pResults)],
        pLogger
    )

def GetLadder2D(pData, pContract, pModel, pPricer, pResults, pLogger):
    return Request(
        '/GetLadder2D',
        [(['DataConfiguration'], pData), (['ContractConfiguration'], pContract), (['ModelConfiguration'], pModel), (['PricerConfiguration'], pPricer), (['Pricer', 'Ladder2D'], pResults)],
        pLogger
    )

def GetLadder(pData, pContract, pModel, pPricer, pResults, pLogger):
    return Request(
        '/GetLadder',
        [(['DataConfiguration'], pData), (['ContractConfiguration'], pContract), (['ModelConfiguration'], pModel), (['PricerConfiguration'], pPricer), (['Pricer', 'Ladder'], pResults)],
        pLogger
    )

def GetImpliedContractFeature(pData, pContract, pModel, pPricer, pResults, pLogger):
    return Request(
        '/GetImpliedContractFeature',
        [(['DataConfiguration'], pData), (['ContractConfiguration'], pContract), (['ModelConfiguration'], pModel), (['PricerConfiguration'], pPricer), (['Pricer', 'Solver'], pResults)],
        pLogger
    )

def GetModelImpliedVolatility(pData, pContract, pModel, pPricer, pResults, pLogger):
    return Request(
        '/GetModelImpliedVolatility',
        [(['DataConfiguration'], pData), (['ContractConfiguration'], pContract), (['ModelConfiguration'], pModel), (['PricerConfiguration'], pPricer), (['Model', 'Repricing'], pResults)],
        pLogger
    )

def GetData(pData, pResults, pLogger):
    return Request(
        '/GetData',
        [(['DataConfiguration'], pData), (['Data', 'Observable'], pResults)],
        pLogger
    )

def GetMCPriceWithDetails(pData, pContract, pModel, pPricer, pResults, pLogger):
    return Request(
        '/GetMCPriceWithDetails',
        [(['DataConfiguration'], pData), (['ContractConfiguration'], pContract), (['ModelConfiguration'], pModel), (['PricerConfiguration'], pPricer), (['Pricer', 'MCDetails'], pResults)],
        pLogger
    )