# std.
from os import cpu_count

# qa.
from qanalytics.Enum import *

class DataSource:
    def __init__(self, File = '', IsActivated = True):
        self.File = File
        self.IsActivated = IsActivated
        self.Status = False
    def serialize(self):
        return {
            'File': self.File,
            'IsActivated': self.IsActivated,
            'Status': self.Status
        }
    def deserialize(self, pRoot):
        self.File = pRoot['File']
        self.IsActivated = pRoot['IsActivated']
        self.Status = pRoot['Status']
        return self

class Data:
    def __init__(self,
        Username = '',
        Password = '',
        Sources = [],
        Attempts = 0,
        SuccessOnRepoRequestFailure = False,
        SuccessOnSpotRequestFailure = False,
        SuccessOnFXSpotRequestFailure = False,
        SuccessOnVolatilityRequestFailure = False,
        SuccessOnYieldRequestFailure = False,
        SuccessOnCorrelationRequestFailure = False
    ):
        self.Username = Username
        self.Password = Password
        self.Sources = Sources
        self.Attempts = Attempts
        self.SuccessOnRepoRequestFailure = SuccessOnRepoRequestFailure
        self.SuccessOnSpotRequestFailure = SuccessOnSpotRequestFailure
        self.SuccessOnFXSpotRequestFailure = SuccessOnFXSpotRequestFailure
        self.SuccessOnVolatilityRequestFailure = SuccessOnVolatilityRequestFailure
        self.SuccessOnYieldRequestFailure = SuccessOnYieldRequestFailure
        self.SuccessOnCorrelationRequestFailure = SuccessOnCorrelationRequestFailure
    def serialize(self):
        return {
            'Username': self.Username,
            'Password': self.Password,
            'Sources': [item.serialize() for item in self.Sources],
            'SuccessOnRepoRequestFailure': self.SuccessOnRepoRequestFailure,
            'SuccessOnSpotRequestFailure': self.SuccessOnSpotRequestFailure,
            'SuccessOnFXSpotRequestFailure': self.SuccessOnFXSpotRequestFailure,
            'SuccessOnVolatilityRequestFailure': self.SuccessOnVolatilityRequestFailure,
            'SuccessOnYieldRequestFailure': self.SuccessOnYieldRequestFailure,
            'SuccessOnCorrelationRequestFailure': self.SuccessOnCorrelationRequestFailure,
            'Attempts': self.Attempts
        }
    def deserialize(self, pRoot):
        self.Username = pRoot['Username']
        self.Password = pRoot['Password']
        self.Sources = [DataSource().deserialize(item) for item in pRoot['Sources']]
        self.Attempts = pRoot['Attempts']
        self.SuccessOnRepoRequestFailure = pRoot['SuccessOnRepoRequestFailure']
        self.SuccessOnSpotRequestFailure = pRoot['SuccessOnSpotRequestFailure']
        self.SuccessOnFXSpotRequestFailure = pRoot['SuccessOnFXSpotRequestFailure']
        self.SuccessOnVolatilityRequestFailure = pRoot['SuccessOnVolatilityRequestFailure']
        self.SuccessOnYieldRequestFailure = pRoot['SuccessOnYieldRequestFailure']
        self.SuccessOnCorrelationRequestFailure = pRoot['SuccessOnCorrelationRequestFailure']
        return self
    
class ICashFlow:
    def serialize(self):
        raise NotImplementedError
    def deserialize(self, _):
        raise NotImplementedError
    
class Console(ICashFlow):
    def __init__(self):
        self.Script = ''
    def serialize(self):
        return {
            'Script': self.Script
        }
    def deserialize(self, pRoot):
        self.Script = pRoot['Script']
        return self
    
class File(ICashFlow):
    def __init__(self):
        self.File = ''
    def serialize(self):
        return {
            'File': self.File
        }
    def deserialize(self, pRoot):
        self.File = pRoot['File']
        return self
    
class Vanilla(ICashFlow):
    def __init__(self):
        self.Cliquet = []
    def serialize(self):
        return [item.serialize() for item in self.Cliquet]
    def deserialize(self, pRoot):
        self.Cliquet = []
        return self
    
class BasketItem:
    def __init__(self, Ticker = '', Weight = 0.0):
        self.Ticker = Ticker
        self.Weight = Weight
    def serialize(self):
        return {
            'Ticker': self.Ticker,
            'Weight': self.Weight
        }
    def deserialize(self, pRoot):
        self.Ticker = pRoot['Ticker']
        self.Weight = pRoot['Weight']
        return self
    
class AutocallScheduleItem:
    def __init__(self,
        ObservationDate = '',
        PaymentDate = '',
        PaymentCurrency = '',
        Notional = 0.0,
        BarrierKind = '',
        AutocallBarrier = 0.0,
        AutocallBarrierSpreadLeft = 0.0,
        AutocallBarrierSpreadRight = 0.0,
        PhoenixCoupon = 0.0,
        CouponBarrier = 0.0,
        CouponBarrierSpreadLeft = 0.0,
        CouponBarrierSpreadRight = 0.0,
        BonusCoupon = 0.0
    ):
        self.ObservationDate = ObservationDate
        self.PaymentDate = PaymentDate
        self.PaymentCurrency = PaymentCurrency
        self.Notional = Notional
        self.BarrierKind = BarrierKind
        self.AutocallBarrier = AutocallBarrier
        self.AutocallBarrierSpreadLeft = AutocallBarrierSpreadLeft
        self.AutocallBarrierSpreadRight = AutocallBarrierSpreadRight
        self.PhoenixCoupon = PhoenixCoupon
        self.CouponBarrier = CouponBarrier
        self.CouponBarrierSpreadLeft = CouponBarrierSpreadLeft
        self.CouponBarrierSpreadRight = CouponBarrierSpreadRight
        self.BonusCoupon = BonusCoupon
    def serialize(self):
        return {
            'ObservationDate': self.ObservationDate,
            'PaymentDate': self.PaymentDate,
            'PaymentCurrency': self.PaymentCurrency,
            'Notional': self.Notional,
            'BarrierKind': self.BarrierKind,
            'AutocallBarrier': self.AutocallBarrier,
            'AutocallBarrierSpreadLeft': self.AutocallBarrierSpreadLeft,
            'AutocallBarrierSpreadRight': self.AutocallBarrierSpreadRight,
            'PhoenixCoupon': self.PhoenixCoupon,
            'CouponBarrier': self.CouponBarrier,
            'CouponBarrierSpreadLeft': self.CouponBarrierSpreadLeft,
            'CouponBarrierSpreadRight': self.CouponBarrierSpreadRight,
            'BonusCoupon': self.BonusCoupon
        }
    def deserialize(self, pRoot):
        self.ObservationDate = pRoot['ObservationDate']
        self.PaymentDate = pRoot['PaymentDate']
        self.PaymentCurrency = pRoot['PaymentCurrency']
        self.Notional = pRoot['Notional']
        self.BarrierKind = pRoot['BarrierKind']
        self.AutocallBarrier = pRoot['AutocallBarrier']
        self.AutocallBarrierSpreadLeft = pRoot['AutocallBarrierSpreadLeft']
        self.AutocallBarrierSpreadRight = pRoot['AutocallBarrierSpreadRight']
        self.PhoenixCoupon = pRoot['PhoenixCoupon']
        self.CouponBarrier = pRoot['CouponBarrier']
        self.CouponBarrierSpreadLeft = pRoot['CouponBarrierSpreadLeft']
        self.CouponBarrierSpreadRight = pRoot['CouponBarrierSpreadRight']
        self.BonusCoupon = pRoot['BonusCoupon']
        return self
    
class Point:
    def __init__(self, X = 0.0, Y = 0.0):
        self.X = X
        self.Y = Y
    def serialize(self):
        return {
            'X': self.X,
            'Y': self.Y
        }
    def deserialize(self, pRoot):
        self.X = pRoot['X']
        self.Y = pRoot['Y']
        return self

class Autocall(ICashFlow):
    def __init__(self,
        Basket = [],
        Schedule = [],
        FinalPayment = [],
        BonusCouponWithMemory = False,
        BasketKind = BasketKind.BASKET,
        StrikeKind = StrikeKind.ASIAN,
        ForwardStartDate = ''
    ):
        self.Basket = Basket
        self.Schedule = Schedule
        self.FinalPayment = FinalPayment
        self.BonusCouponWithMemory = BonusCouponWithMemory
        self.BasketKind = BasketKind
        self.StrikeKind = StrikeKind
        self.ForwardStartDate = ForwardStartDate
    def serialize(self):
        return {
            'Basket': [item.serialize() for item in self.Basket],
            'Schedule': [item.serialize() for item in self.Schedule],
            'FinalPayment': [item.serialize() for item in self.FinalPayment],
            'BonusCouponWithMemory': self.BonusCouponWithMemory,
            'BasketKind': self.BasketKind,
            'StrikeKind': self.StrikeKind,
            'ForwardStartDate': self.ForwardStartDate
        }
    def deserialize(self, pRoot):
        self.Basket = [BasketItem().deserialize(item) for item in pRoot['Basket']]
        self.Schedule = [AutocallScheduleItem().deserialize(item) for item in pRoot['Schedule']]
        self.FinalPayment = [Point().deserialize(item) for item in pRoot['FinalPayment']]
        self.BonusCouponWithMemory = pRoot['BonusCouponWithMemory']
        self.BasketKind = pRoot['BasketKind']
        self.StrikeKind = pRoot['StrikeKind']
        self.ForwardStartDate = pRoot['ForwardStartDate'] 
        return self

class Contract:
    def __init__(self,
        Date = '',
        Kind = ContractKind.CONSOLE,
        CashFlow = None,
        PremiumCurrency = '',
        IntradayFixings = False,
        IntradayPayments = False,
        IntradayChoices = False
    ):
        self.Date = Date
        self.Kind = Kind
        self.CashFlow = CashFlow
        self.PremiumCurrency = PremiumCurrency
        self.IntradayFixings = IntradayFixings
        self.IntradayPayments = IntradayPayments
        self.IntradayChoices = IntradayChoices
    def serialize(self):
        root = self.CashFlow.serialize()
        root['Date'] = self.Date
        root['Kind'] = self.Kind.upper()
        root['PremiumCurrency'] = self.PremiumCurrency
        root['IntradayFixings'] = self.IntradayFixings
        root['IntradayPayments'] = self.IntradayPayments
        root['IntradayChoices'] = self.IntradayChoices
        return root
    def deserialize(self, pRoot):
        self.CashFlow.deserialize(pRoot)
        self.Date = pRoot['Date']
        self.PremiumCurrency = pRoot['PremiumCurrency']
        self.IntradayFixings = pRoot['IntradayFixings']
        self.IntradayPayments = pRoot['IntradayPayments']
        self.IntradayChoices = pRoot['IntradayChoices']
        return self

class Log:
    def __init__(self):
        self.Level = LogLevel.INFO
        self.Message = ''
    def serialize(self):
        return {
            'Level': self.Level,
            'Message': self.Message
        }
    def deserialize(self, pRoot):
        self.Level = pRoot['Level']
        self.Message = pRoot['Message']
        return self

class Logger:
    def __init__(self):
        self.Logs = []
    def serialize(self):
        return [item.serialize() for item in self.Logs]
    def deserialize(self, pRoot):
        self.Logs = [Log().deserialize(item) for item in pRoot]
        return self
    
class Underlying:
    def __init__(self):
        self.Ticker = ''
        self.CompleteName = ''
        self.QuoteCurrency = ''
        self.LastQuote = 0
        self.HasLastQuote = False
        self.AssetClass = AssetClass.DEPOSIT_RATE
        self.AssetKind = AssetKind.EQUITY
        self.IsQuanto = False
        self.IsInBasket = False
    def serialize(self):
        return {
            'Ticker': self.Ticker,
            'CompleteName': self.CompleteName,
            'LastQuote': self.LastQuote,
            'HasLastQuote': self.HasLastQuote,
            'AssetClass': self.AssetClass,
            'AssetKind': self.AssetKind,
            'IsQuanto': self.IsQuanto,
            'IsInBasket': self.IsInBasket
        }
    def deserialize(self, pRoot):
        self.Ticker = pRoot['Ticker']
        self.CompleteName = pRoot['CompleteName']
        self.LastQuote = pRoot['LastQuote']
        self.HasLastQuote = pRoot['HasLastQuote']
        self.AssetClass = pRoot['AssetClass']
        self.AssetKind = pRoot['AssetKind']
        self.IsQuanto = pRoot['IsQuanto']
        self.IsInBasket = pRoot['IsInBasket']
        return self

class Fixing:
    def __init__(self):
        self.Date = ''
        self.QuoteCurrency = ''
        self.Ticker = ''
        self.Quote = 0
        self.HasQuote = False
        self.IsPast = False
        self.Edit = False
    def serialize(self):
        return {
            'Date': self.Date,
            'QuoteCurrency': self.QuoteCurrency,
            'Ticker': self.Ticker,
            'Quote': self.Quote,
            'HasQuote': self.HasQuote,
            'IsPast': self.IsPast,
            'Edit': self.Edit
        }
    def deserialize(self, pRoot):
        self.Date = pRoot['Date']
        self.QuoteCurrency = pRoot['QuoteCurrency']
        self.Ticker = pRoot['Ticker']
        self.Quote = pRoot['Quote']
        self.HasQuote = pRoot['HasQuote']
        self.IsPast = pRoot['IsPast']
        self.Edit = pRoot['Edit']
        return self

class Correlation:
    def __init__(self):
        self.Value = 0
        self.HasValue = False
    def serialize(self):
        return {
            'Value': self.Value,
            'HasValue': self.HasValue
        }
    def deserialize(self, pRoot):
        self.Value = pRoot['Value']
        self.HasValue = pRoot['HasValue']
        return self

class CorrelationMatrix:
    def __init__(self):
        self.Rows = []
        self.Cols = []
        self.Data = [[]]
    def serialize(self):
        return {
            'Rows': self.Rows,
            'Cols': self.Cols,
            'Data': [[item.serialize() for item in jtem] for jtem in self.Data]
        }
    def deserialize(self, pRoot):
        self.Rows = pRoot['Rows']
        self.Cols = pRoot['Cols']
        self.Data = [[Correlation().deserialize(item) for item in jtem] for jtem in pRoot['Data']]
        return self

class IEvent:
    def serialize(self):
        raise NotImplementedError
    def deserialize(self, _):
        raise NotImplementedError
    
class PaymentEvent(IEvent):
    def __init__(self):
        self.Currency = ''
        self.Script = ''
        self.Value = 0
        self.HasValue = False
    def serialize(self):
        return {
            'Currency': self.Currency,
            'Script': self.Script,
            'HasValue': self.HasValue
        }
    def deserialize(self, pRoot):
        self.Currency = pRoot['Currency']
        self.Script = pRoot['Script']
        self.HasValue = pRoot['HasValue']
        return self
    
class PurchaseEvent(IEvent):
    def __init__(self):
        self.Quantity = 0
        self.Start = 0
        self.End = 0
    def serialize(self):
        return {
            'Quantity': self.Quantity,
            'Start': self.Start,
            'End': self.End
        }
    def deserialize(self, pRoot):
        self.Quantity = pRoot['Quantity']
        self.Start = pRoot['Start']
        self.End = pRoot['End']
        return self
    
class FixingEvent(IEvent):
    def __init__(self):
        self.Ticker = ''
        self.Value = 0
        self.HasValue = False
    def serialize(self):
        return {
            'Ticker': self.Ticker,
            'Value': self.Value,
            'HasValue': self.HasValued
        }
    def deserialize(self, pRoot):
        self.Ticker = pRoot['Ticker']
        self.Value = pRoot['Value']
        self.HasValue = pRoot['HasValue']
        return self
    
class SettingEvent(IEvent):
    def __init__(self):
        self.Name = ''
        self.Script = ''
        self.Value = 0
        self.HasValue = False
    def serialize(self):
        return {
            'Name': self.Name,
            'Script': self.Script,
            'Value': self.Value,
            'HasValue': self.HasValue
        }
    def deserialize(self, pRoot):
        self.Name = pRoot['Name']
        self.Script = pRoot['Script']
        self.Value = pRoot['Value']
        self.HasValue = pRoot['HasValue']
        return self
    
class ChoiceEvent(IEvent):
    def __init__(self):
        self.ChoiceOwnership = ''
        self.Starts = []
        self.Ends = []
        self.Value = 0
        self.HasValue = False
    def serialize(self):
        return {
            'ChoiceOwnership': self.ChoiceOwnership,
            'Starts': self.Starts,
            'Ends': self.Ends,
            'Value': self.Value,
            'HasValue': self.HasValue
        }
    def deserialize(self, pRoot):
        self.ChoiceOwnership = pRoot['ChoiceOwnership']
        self.Starts = pRoot['Starts']
        self.Ends = pRoot['Ends']
        self.Value = pRoot['Value']
        self.HasValue = pRoot['HasValue']
        return self
    
class BarrierEvent(IEvent):
    def __init__(self):
        self.WithSpread = False
        self.SpreadLeft = 0
        self.SpreadRight = 0
        self.Script = ''
        self.StartLeft = 0
        self.StartRight = 0
        self.EndLeft = 0
        self.EndRight = 0
        self.Value = 0
        self.HasValue = False
    def serialize(self):
        return {
            'WithSpread': self.WithSpread,
            'SpreadLeft': self.SpreadLeft,
            'SpreadRight': self.SpreadRight,
            'Script': self.Script,
            'StartLeft': self.StartLeft,
            'StartRight': self.StartRight,
            'EndLeft': self.EndLeft,
            'EndRight': self.EndRight,
            'Value': self.Value,
            'HasValue': self.HasValue
        }
    def deserialize(self, pRoot):
        self.WithSpread = pRoot['WithSpread']
        self.SpreadLeft = pRoot['SpreadLeft']
        self.SpreadRight = pRoot['SpreadRight']
        self.Script = pRoot['Script']
        self.StartLeft = pRoot['StartLeft']
        self.StartRight = pRoot['StartRight']
        self.EndLeft = pRoot['EndLeft']
        self.EndRight = pRoot['EndRight']
        self.Value = pRoot['Value']
        self.HasValue = pRoot['HasValue']
        return self

class EndEvent(IEvent):
    def serialize(self):
        return None
    def deserialize(self, _):
        return self
    
class Event:
    def __init__(self):
        self.EventKind = EventKind.BARRIER
        self.Date = ''
        self.Attributes = None
    def serialize(self):
        return {
            'EventKind': self.EventKind,
            'Date': self.Date,
            'Attributes': self.Attributes.serialize()
        }
    def deserialize(self, pRoot):
        self.EventKind = pRoot['EventKind']
        self.Date = pRoot['Date']
        self.Attributes.deserialize(pRoot['Attributes'])
        return self
    
class ContractResults:
    def __init__(self):
        # Input.
        self.RequestScript = True
        self.RequestUnderlyings = True
        self.RequestFixings = True
        self.RequestCorrelations = True
        self.RequestEvents = True

        # Output.
        self.Script = ''
        self.Underlyings = []
        self.Fixings = []
        self.CorrelationMatrix = CorrelationMatrix()
        self.Events = []
    def serialize(self):
        return {
            'RequestScript': self.RequestScript,
            'RequestUnderlyings': self.RequestUnderlyings,
            'RequestFixings': self.RequestFixings,
            'RequestCorrelations': self.RequestCorrelations,
            'RequestEvents': self.RequestEvents,
            'Script': self.Script,
            'Underlyings': self.Underlyings,
            'Fixings': self.Fixings,
            'CorrelationMatrix': self.CorrelationMatrix.serialize(),
            'Events': self.Events
        }
    def deserialize(self, pRoot):
        self.RequestScript = pRoot['RequestScript']
        self.RequestUnderlyings = pRoot['RequestUnderlyings']
        self.RequestFixings = pRoot['RequestFixings']
        self.RequestCorrelations = pRoot['RequestCorrelations']
        self.RequestEvents = pRoot['RequestEvents']
        self.Script = pRoot['Script']
        self.Underlyings = [Underlying().deserialize(item) for item in pRoot['Underlyings']]
        self.Fixings = [Fixing().deserialize(item) for item in pRoot['Fixings']]
        self.CorrelationMatrix.deserialize(pRoot['CorrelationMatrix'])
        self.Events = pRoot['Events']
        return self
    
class Schedule:
    def __init__(self):
        # Input.
        self.StartDate = ''
        self.EndDate = ''
        self.DateShift = ''
        self.Calendar = Calendar.DUMMY

        # Output.
        self.Dates = []
    def serialize(self):
        return {
            'StartDate': self.StartDate,
            'EndDate': self.EndDate,
            'DateShift': self.DateShift,
            'Calendar': self.Calendar.upper(),
            'Dates': self.Dates
        }
    def deserialize(self, pRoot):
        self.StartDate = pRoot['StartDate']
        self.EndDate = pRoot['EndDate']
        self.DateShift = pRoot['DateShift']
        self.Calendar = pRoot['Calendar']
        self.Dates = pRoot['Dates']
        return self
    
class DateShift:
    def __init__(self, pShift='', pCalendar=Calendar.DUMMY):
        self.Shift = pShift
        self.Calendar = pCalendar
    def serialize(self):
        return {
            'Shift': self.Shift,
            'Calendar': self.Calendar.upper()
        }
    def deserialize(self, pRoot):
        self.Shift = pRoot['Shift']
        self.Calendar = pRoot['Calendar']
        return self
    
class Model:
    def __init__(self,
        CalibrationDate = '',
        Name = ModelName.BLACK_SCHOLES_MODEL,
        BlackScholesFiniteDifferenceGridSize = 500,
        BlackScholesFiniteDifferenceConfidenceLevel = 97.50,
        BlackScholesCalibrationKind = BlackScholesCalibrationKind.MANUAL,
        BlackScholesVolatilityCalibrationTenor = DateShift()
    ):
        self.CalibrationDate = CalibrationDate
        self.Name = Name
        self.BlackScholesFiniteDifferenceGridSize = BlackScholesFiniteDifferenceGridSize
        self.BlackScholesFiniteDifferenceConfidenceLevel = BlackScholesFiniteDifferenceConfidenceLevel
        self.BlackScholesCalibrationKind = BlackScholesCalibrationKind
        self.BlackScholesVolatilityCalibrationTenor = BlackScholesVolatilityCalibrationTenor
    def serialize(self):
        return {
            'CalibrationDate': self.CalibrationDate,
            'Name': self.Name.upper(),
            'BlackScholesFiniteDifferenceGridSize': self.BlackScholesFiniteDifferenceGridSize,
            'BlackScholesFiniteDifferenceConfidenceLevel': self.BlackScholesFiniteDifferenceConfidenceLevel,
            'BlackScholesCalibrationKind': self.BlackScholesCalibrationKind.upper(),
            'BlackScholesVolatilityCalibrationTenor': self.BlackScholesVolatilityCalibrationTenor.serialize()
        }
    def deserialize(self, pRoot):
        self.CalibrationDate = pRoot['CalibrationDate']
        self.Name = pRoot['Name']
        self.BlackScholesFiniteDifferenceGridSize = pRoot['BlackScholesFiniteDifferenceGridSize']
        self.BlackScholesFiniteDifferenceConfidenceLevel = pRoot['BlackScholesFiniteDifferenceConfidenceLevel']
        self.BlackScholesCalibrationKind = pRoot['BlackScholesCalibrationKind']
        self.BlackScholesVolatilityCalibrationTenor.deserialize(pRoot['BlackScholesVolatilityCalibrationTenor'])
        return self
    
class DayCounter:
    def __init__(self, Basis=Basis.ACT_365, Calendar=Calendar.DUMMY):
        self.Basis = Basis
        self.Calendar = Calendar
    def serialize(self):
        return {
            'Basis': self.Basis.upper(),
            'Calendar': self.Calendar.upper()
        }
    def deserialize(self, pRoot):
        self.Basis = pRoot['Basis']
        self.Calendar = pRoot['Calendar']
        return self
    
class Pricer:
    def __init__(self,
        DayCounter = DayCounter(),
        SmoothingType = SmoothingType.NONE,
        Method = PricingMethod.MONTE_CARLO,
        SpotVolatilityDynamic = SpotVolatilityDynamic.STICKY_STRIKE,
        MonteCarloTrials = 100000,
        MonteCarloTimeStep = 2,
        MonteCarloSeed = 19940523,
        MonteCarloNbThreads = cpu_count(),
        MonteCarloConfidenceLevel = 97.50,
        MonteCarloAntitheticFactor = 50.00,
        FiniteDifferenceBoundaryCondition = BoundaryCondition.DIRICHLET,
        FiniteDifferenceTimeStep = 1,
        FiniteDifferenceExplicitRate = 0.00,
        FiniteDifferenceUseRichardsonRombergExtrapolation = False,
        ClosedFormMoneynessGridSize = 100,
        ClosedFormMoneynessGridLowerBound = 50.00,
        ClosedFormMoneynessGridUpperBound = 150.00,
        WithGreeks = False,
        ComputeDelta = False,
        DeltaSpotBump = 1.0,
        DeltaDirection = GreekDirection.CENTER,
        ComputeGamma = False,
        GammaSpotBump = 1.0,
        ComputeXGamma = False,
        XGammaSpotBump = 1.0,
        ComputeVega = False,
        VegaVolatilityBump = 1.0,
        VegaDirection = GreekDirection.CENTER,
        ComputeVolga = False,
        VolgaVolatilityBump = 1.0,
        ComputeXVolga = False,
        XVolgaVolatilityBump = 1.0,
        ComputeVanna = False,
        VannaVolatilityBump = 1.0,
        VannaSpotBump = 1.0,
        ComputeXVanna = False,
        XVannaVolatilityBump = 1.0,
        XVannaSpotBump = 1.0,
        ComputeCega = False,
        CegaCorrelationBump = 1.0,
        CegaDirection = GreekDirection.CENTER
    ):
        self.DayCounter = DayCounter
        self.SmoothingType = SmoothingType
        self.Method = Method
        self.SpotVolatilityDynamic = SpotVolatilityDynamic
        self.MonteCarloTrials = MonteCarloTrials
        self.MonteCarloTimeStep = MonteCarloTimeStep
        self.MonteCarloSeed = MonteCarloSeed
        self.MonteCarloNbThreads = MonteCarloNbThreads
        self.MonteCarloConfidenceLevel = MonteCarloConfidenceLevel
        self.MonteCarloAntitheticFactor = MonteCarloAntitheticFactor
        self.FiniteDifferenceBoundaryCondition = FiniteDifferenceBoundaryCondition
        self.FiniteDifferenceTimeStep = FiniteDifferenceTimeStep
        self.FiniteDifferenceExplicitRate = FiniteDifferenceExplicitRate
        self.FiniteDifferenceUseRichardsonRombergExtrapolation = FiniteDifferenceUseRichardsonRombergExtrapolation
        self.ClosedFormMoneynessGridSize = ClosedFormMoneynessGridSize
        self.ClosedFormMoneynessGridLowerBound = ClosedFormMoneynessGridLowerBound
        self.ClosedFormMoneynessGridUpperBound = ClosedFormMoneynessGridUpperBound
        self.WithGreeks = WithGreeks
        self.ComputeDelta = ComputeDelta
        self.DeltaSpotBump = DeltaSpotBump
        self.DeltaDirection = DeltaDirection
        self.ComputeGamma = ComputeGamma
        self.GammaSpotBump = GammaSpotBump
        self.ComputeXGamma = ComputeXGamma
        self.XGammaSpotBump = XGammaSpotBump
        self.ComputeVega = ComputeVega
        self.VegaVolatilityBump = VegaVolatilityBump
        self.VegaDirection = VegaDirection
        self.ComputeVolga = ComputeVolga
        self.VolgaVolatilityBump = VolgaVolatilityBump
        self.ComputeXVolga = ComputeXVolga
        self.XVolgaVolatilityBump = XVolgaVolatilityBump
        self.ComputeVanna = ComputeVanna
        self.VannaVolatilityBump = VannaVolatilityBump
        self.VannaSpotBump = VannaSpotBump
        self.ComputeXVanna = ComputeXVanna
        self.XVannaVolatilityBump = XVannaVolatilityBump
        self.XVannaSpotBump = XVannaSpotBump
        self.ComputeCega = ComputeCega
        self.CegaCorrelationBump = CegaCorrelationBump
        self.CegaDirection = CegaDirection
    def serialize(self):
        return {
            'DayCounter': self.DayCounter.serialize(),
            'SmoothingType': self.SmoothingType,
            'Method': self.Method,
            'SpotVolatilityDynamic': self.SpotVolatilityDynamic,
            'MonteCarloTrials': self.MonteCarloTrials,
            'MonteCarloTimeStep': self.MonteCarloTimeStep,
            'MonteCarloSeed': self.MonteCarloSeed,
            'MonteCarloNbThreads': self.MonteCarloNbThreads,
            'MonteCarloConfidenceLevel': self.MonteCarloConfidenceLevel,
            'MonteCarloAntitheticFactor': self.MonteCarloAntitheticFactor,
            'FiniteDifferenceBoundaryCondition': self.FiniteDifferenceBoundaryCondition,
            'FiniteDifferenceTimeStep': self.FiniteDifferenceTimeStep,
            'FiniteDifferenceExplicitRate': self.FiniteDifferenceExplicitRate,
            'FiniteDifferenceUseRichardsonRombergExtrapolation': self.FiniteDifferenceUseRichardsonRombergExtrapolation,
            'ClosedFormMoneynessGridSize': self.ClosedFormMoneynessGridSize,
            'ClosedFormMoneynessGridLowerBound': self.ClosedFormMoneynessGridLowerBound,
            'ClosedFormMoneynessGridUpperBound': self.ClosedFormMoneynessGridUpperBound,
            'WithGreeks': self.WithGreeks,
            'ComputeDelta': self.ComputeDelta,
            'DeltaSpotBump': self.DeltaSpotBump,
            'DeltaDirection': self.DeltaDirection,
            'ComputeGamma': self.ComputeGamma,
            'GammaSpotBump': self.GammaSpotBump,
            'ComputeXGamma': self.ComputeXGamma,
            'XGammaSpotBump': self.XGammaSpotBump,
            'ComputeVega': self.ComputeVega,
            'VegaVolatilityBump': self.VegaVolatilityBump,
            'VegaDirection': self.VegaDirection,
            'ComputeVolga': self.ComputeVolga,
            'VolgaVolatilityBump': self.VolgaVolatilityBump,
            'ComputeXVolga': self.ComputeXVolga,
            'XVolgaVolatilityBump': self.XVolgaVolatilityBump,
            'ComputeVanna': self.ComputeVanna,
            'VannaVolatilityBump': self.VannaVolatilityBump,
            'VannaSpotBump': self.VannaSpotBump,
            'ComputeXVanna': self.ComputeXVanna,
            'XVannaVolatilityBump': self.XVannaVolatilityBump,
            'XVannaSpotBump': self.XVannaSpotBump,
            'ComputeCega': self.ComputeCega,
            'CegaCorrelationBump': self.CegaCorrelationBump,
            'CegaDirection': self.CegaDirection
        }
    def deserialize(self, pRoot):
        self.DayCounter.deserialize(pRoot['DayCounter'])
        self.SmoothingType = pRoot['SmoothingType']
        self.Method = pRoot['Method']
        self.SpotVolatilityDynamic = pRoot['SpotVolatilityDynamic']
        self.MonteCarloTrials = pRoot['MonteCarloTrials']
        self.MonteCarloTimeStep = pRoot['MonteCarloTimeStep']
        self.MonteCarloSeed = pRoot['MonteCarloSeed']
        self.MonteCarloNbThreads = pRoot['MonteCarloNbThreads']
        self.MonteCarloConfidenceLevel = pRoot['MonteCarloConfidenceLevel']
        self.MonteCarloAntitheticFactor = pRoot['MonteCarloAntitheticFactor']
        self.FiniteDifferenceBoundaryCondition = pRoot['FiniteDifferenceBoundaryCondition']
        self.FiniteDifferenceTimeStep = pRoot['FiniteDifferenceTimeStep']
        self.FiniteDifferenceExplicitRate = pRoot['FiniteDifferenceExplicitRate']
        self.FiniteDifferenceUseRichardsonRombergExtrapolation = pRoot['FiniteDifferenceUseRichardsonRombergExtrapolation']
        self.ClosedFormMoneynessGridSize = pRoot['ClosedFormMoneynessGridSize']
        self.ClosedFormMoneynessGridLowerBound = pRoot['ClosedFormMoneynessGridLowerBound']
        self.ClosedFormMoneynessGridUpperBound = pRoot['ClosedFormMoneynessGridUpperBound']
        self.WithGreeks = pRoot['WithGreeks']
        self.ComputeDelta = pRoot['ComputeDelta']
        self.DeltaSpotBump = pRoot['DeltaSpotBump']
        self.DeltaDirection = pRoot['DeltaDirection']
        self.ComputeGamma = pRoot['ComputeGamma']
        self.GammaSpotBump = pRoot['GammaSpotBump']
        self.ComputeXGamma = pRoot['ComputeXGamma']
        self.XGammaSpotBump = pRoot['XGammaSpotBump']
        self.ComputeVega = pRoot['ComputeVega']
        self.VegaVolatilityBump = pRoot['VegaVolatilityBump']
        self.VegaDirection = pRoot['VegaDirection']
        self.ComputeVolga = pRoot['ComputeVolga']
        self.VolgaVolatilityBump = pRoot['VolgaVolatilityBump']
        self.ComputeXVolga = pRoot['ComputeXVolga']
        self.XVolgaVolatilityBump = pRoot['XVolgaVolatilityBump']
        self.ComputeVanna = pRoot['ComputeVanna']
        self.VannaVolatilityBump = pRoot['VannaVolatilityBump']
        self.VannaSpotBump = pRoot['VannaSpotBump']
        self.ComputeXVanna = pRoot['ComputeXVanna']
        self.XVannaVolatilityBump = pRoot['XVannaVolatilityBump']
        self.XVannaSpotBump = pRoot['XVannaSpotBump']
        self.ComputeCega = pRoot['ComputeCega']
        self.CegaCorrelationBump = pRoot['CegaCorrelationBump']
        self.CegaDirection = pRoot['CegaDirection']
        return self
    
class Sequence:
    def __init__(self):
        self.Kind = SequenceKind.UNIFORM;
        self.LowerValue = 0.0
        self.UpperValue = 1.0
        self.Size = 10
        self.Values = []
    def serialize(self):
        return {
            'Kind': self.Kind.upper(),
            'LowerValue': self.LowerValue,
            'UpperValue': self.UpperValue,
            'Size': self.Size,
            'Values': self.Values
        }
    def deserialize(self, pRoot):
        self.Kind = pRoot['Kind']
        self.LowerValue = pRoot['LowerValue']
        self.UpperValue = pRoot['UpperValue']
        self.Size = pRoot['Size']
        self.Values = pRoot['Values']
        return self
    
class TickerVolatility:
    def __init__(self):
        self.Ticker = ''
        self.Volatility = 0.0
    def serialize(self):
        return {
            'Ticker': self.Ticker,
            'Volatility': self.Volatility
        }
    def deserialize(self, pRoot):
        self.Ticker = pRoot['Ticker']
        self.Volatility = pRoot['Volatility']
        return self
    
class BlackScholesCalibrationResults:
    def __init__(self):
        self.Volatility = []
    def serialize(self):
        return {
            'Volatility': [item.serialize() for item in self.Volatility]
        }
    def deserialize(self, pRoot):
        self.Volatility = [TickerVolatility().deserialize(item) for item in pRoot['Volatility']]
        return self
    
class TermStructureVolatility:
    def __init__(self):
        self.Tenor = ''
        self.Volatility = 0.0
    def serialize(self):
        return {
            'Tenor': self.Tenor,
            'Volatility': self.Volatility
        }
    def deserialize(self, pRoot):
        self.Tenor = pRoot['Tenor']
        self.Volatility = pRoot['Volatility']
        return self
    
class TickerTermStructureVolatility:
    def __init__(self):
        self.Ticker = ''
        self.Volatility = TermStructureVolatility()
    def serialize(self):
        return {
            'Ticker': self.Ticker,
            'Volatility': self.Volatility.serialize()
        }
    def deserialize(self, pRoot):
        self.Ticker = pRoot['Ticker']
        self.Volatility = [TermStructureVolatility().deserialize(item) for item in pRoot['Volatility']]
        return self
    
class BlackScholesTermStructureCalibrationResults:
    def __init__(self):
        self.Volatility = []
    def serialize(self):
        return {
            'Volatility': self.Volatility.serialize()
        }
    def deserialize(self, pRoot):
        self.Volatility = [TickerTermStructureVolatility().deserialize(item) for item in pRoot['Volatility']]
        return self
    
class PricingResult:
    def __init__(self):
        self.Mean = 0.0
        self.Lower = 0.0
        self.Upper = 0.0
        self.Stddev = 0.0
    def serialize(self):
        return {
            'Mean': self.Mean,
            'Lower': self.Lower,
            'Upper': self.Upper,
            'Stddev': self.Stddev
        }
    def deserialize(self, pRoot):
        self.Mean = pRoot['Mean']
        self.Lower = pRoot['Lower']
        self.Upper = pRoot['Upper']
        self.Stddev = pRoot['Stddev']
        return self
    
class PriceResult:
    def __init__(self):
        self.Value = PricingResult()
    def serialize(self):
        return {
            'Value': self.Value.serialize()
        }
    def deserialize(self, pRoot):
        self.Value = PricingResult().deserialize(pRoot['Value'])
        return self

class NameValueResult:
    def __init__(self):
        self.Name = ''
        self.Value = PricingResult()
    def serialize(self):
        return {
            'Name': self.Name,
            'Value': self.Value.serialize()
        }
    def deserialize(self, pRoot):
        self.Name = pRoot['Name']
        self.Value = PricingResult().deserialize(pRoot['Value'])
        return self
    
class TickerValueResult:
    def __init__(self):
        self.Ticker = ''
        self.Value = PricingResult()
    def serialize(self):
        return {
            'Ticker': self.Ticker,
            'Value': self.Value.serialize()
        }
    def deserialize(self, pRoot):
        self.Ticker = pRoot['Ticker']
        self.Value = PricingResult().deserialize(pRoot['Value'])
        return self
    
class XGreek:
    def __init__(self):
        self.FirstTicker = ''
        self.SecondTicker = ''
        self.Value = PricingResult()
    def serialize(self):
        return {
            'FirstTicker': self.FirstTicker,
            'SecondTicker': self.SecondTicker,
            'Value': self.Value.serialize()
        }
    def deserialize(self, pRoot):
        self.FirstTicker = pRoot['FirstTicker']
        self.SecondTicker = pRoot['SecondTicker']
        self.Value = PricingResult().deserialize(pRoot['Value'])
        return self
    
class PricingResults:
    def __init__(self):
        self.All = [];
        self.Price = []
        self.Delta = []
        self.Gamma = []
        self.Vega = []
        self.Volga = []
        self.Vanna = []
        self.XGamma = []
        self.XVolga = []
        self.XVanna = []
        self.Cega = []
    def serialize(self):
        return {
            'All': [item.serialize() for item in self.All],
            'Price': [item.serialize() for item in self.Price],
            'Delta': [item.serialize() for item in self.Delta],
            'Gamma': [item.serialize() for item in self.Gamma],
            'Vega': [item.serialize() for item in self.Vega],
            'Volga': [item.serialize() for item in self.Volga],
            'Vanna': [item.serialize() for item in self.Vanna],
            'XGamma': [item.serialize() for item in self.XGamma],
            'XVolga': [item.serialize() for item in self.XVolga],
            'XVanna': [item.serialize() for item in self.XVanna],
            'Cega': [item.serialize() for item in self.Cega]
        }
    def deserialize(self, pRoot):
        self.All = [NameValueResult().deserialize(item) for item in pRoot['All']],
        self.Price = [PriceResult().deserialize(item) for item in pRoot['Price']],
        if(pRoot['Delta'] != None):
            self.Delta = [TickerValueResult().deserialize(item) for item in pRoot['Delta']],
        if(pRoot['Gamma'] != None):
            self.Gamma = [TickerValueResult().deserialize(item) for item in pRoot['Gamma']],
        if(pRoot['Vega'] != None):
            self.Vega = [TickerValueResult().deserialize(item) for item in pRoot['Vega']],
        if(pRoot['Volga'] != None):
            self.Volga = [TickerValueResult().deserialize(item) for item in pRoot['Volga']],
        if(pRoot['Vanna'] != None):
            self.Vanna = [TickerValueResult().deserialize(item) for item in pRoot['Vanna']],
        if(pRoot['XGamma'] != None):
            self.XGamma = [XGreek().deserialize(item) for item in pRoot['XGamma']],
        if(pRoot['XVolga'] != None):
            self.XVolga = [XGreek().deserialize(item) for item in pRoot['XVolga']],
        if(pRoot['XVanna'] != None):
            self.XVanna = [XGreek().deserialize(item) for item in pRoot['XVanna']],
        if(pRoot['Cega'] != None):
            self.Cega = [XGreek().deserialize(item) for item in pRoot['Cega']]
        return self
    
class Ladder1DPlot:
    def __init__(self, BumpValue=0.0, Results=PricingResults()):
        self.BumpValue = BumpValue
        self.Results = Results
    def serialize(self):
        return {
            'BumpValue': 0.0,
            'Results': self.Results.serialize()
        }
    def deserialize(self, pRoot):
        self.BumpValue = pRoot['BumpValue']
        self.Results = PricingResults().deserialize(pRoot['Results'])
        return self
    
class Ladder1DResults:
    def __init__(self):
        self.Name = ''
        self.LadderKind = LadderKind.MARKET
        self.BumpKind = BumpKind.ADDITIVE
        self.BumpUnit = BumpUnit.BASIS_POINT
        self.OutputNames = []
        self.CentralResult = PricingResults()
        self.Plots = []
    def serialize(self):
        return {
            'Name': self.Name,
            'LadderKind': self.LadderKind.upper(),
            'BumpKind': self.BumpKind.upper(),
            'BumpUnit': self.BumpUnit.upper(),
            'OutputNames': [item.serialize() for item in self.OutputNames],
            'CentralResult': self.CentralResult.serialize(),
            'Plots': [item.serialize() for item in self.Plots]
        }
    def deserialize(self, pRoot):
        self.Name = pRoot['Name']
        self.LadderKind = pRoot['LadderKind']
        self.BumpKind = pRoot['BumpKind']
        self.BumpUnit = pRoot['BumpUnit']
        self.OutputNames = [NameValueResult().deserialize(item) for item in pRoot['OutputNames']]
        self.CentralResult = PricingResults().deserialize(pRoot['CentralResult'])
        self.Plots = [Ladder1DPlot().deserialize(item) for item in pRoot['Plots']]
        return self

class Ladder2DPlot:
    def __init__(self):
        self.Results = PricingResults()
    def serialize(self):
        return {
            'Results': self.Results.serialize()
        }
    def deserialize(self, pRoot):
        self.Results = PricingResults().deserialize(pRoot['Results'])
        return self
    
class Ladder2DPlots:
    def __init__(self):
        self.Rows = []
        self.Cols = []
        self.Data = [[]]
    def serialize(self):
        return {
            'Rows': self.Rows,
            'Cols': self.Cols,
            'Data': [[item.serialize() for item in jtem] for jtem in self.Data]
        }
    def deserialize(self, pRoot):
        self.Rows = pRoot['Rows']
        self.Cols = pRoot['Cols']
        self.Data = [[Ladder2DPlot().deserialize(item) for item in jtem] for jtem in pRoot['Data']]
        return self

class Ladder2DResults:
    def __init__(self):
        self.LadderKind = LadderKind.MARKET
        self.FirstName = ''
        self.SecondName = ''
        self.FirstBumpKind = BumpKind.ADDITIVE
        self.SecondBumpKind = BumpKind.ADDITIVE
        self.FirstBumpUnit = BumpUnit.BASIS_POINT
        self.SecondBumpUnit = BumpUnit.BASIS_POINT
        self.FirstBumpValues = []
        self.SecondBumpValues = []
        self.Plots = Ladder2DPlots()
        self.OutputNames = []
        self.CentralResult = PricingResults()
    def serialize(self):
        return {
            'LadderKind': self.LadderKind.upper(),
            'FirstName': self.FirstName,
            'SecondName': self.SecondName,
            'FirstBumpKind': self.FirstBumpKind.upper(),
            'SecondBumpKind': self.SecondBumpKind.upper(),
            'FirstBumpUnit': self.FirstBumpUnit.upper(),
            'SecondBumpUnit': self.SecondBumpUnit.upper(),
            'FirstBumpValues': self.FirstBumpValues,
            'SecondBumpValues': self.SecondBumpValues,
            'Plots': self.Plots.serialize(),
            'OutputNames': [item.serialize() for item in self.OutputNames],
            'CentralResult': self.CentralResult.serialize()
        }
    def deserialize(self, pRoot):
        self.LadderKind = pRoot['LadderKind']
        self.FirstName = pRoot['FirstName']
        self.SecondName = pRoot['SecondName']
        self.FirstBumpKind = pRoot['FirstBumpKind']
        self.SecondBumpKind = pRoot['SecondBumpKind']
        self.FirstBumpUnit = pRoot['FirstBumpUnit']
        self.SecondBumpUnit = pRoot['SecondBumpUnit']
        self.FirstBumpValues = pRoot['FirstBumpValues']
        self.SecondBumpValues = pRoot['SecondBumpValues']
        self.Plots = Ladder2DPlots().deserialize(pRoot['Plots'])
        self.OutputNames = [NameValueResult().deserialize(item) for item in pRoot['OutputNames']]
        self.CentralResult = PricingResults().deserialize(pRoot['CentralResult'])
        return self

class FeatureToSolve:
    def __init__(self, Name='', Min=0.0, Max=0.0, Precision=1):
        self.Name = Name
        self.Min = Min
        self.Max = Max
        self.Precision = Precision
        self.Lower = 0.0
        self.Upper = 0.0
        self.Root = 0.0
        self.HasLower = False
        self.HasUpper = False
        self.HasRoot = False
    def serialize(self):
        return {
            'Name': self.Name,
            'Min': self.Min,
            'Max': self.Max,
            'Precision': self.Precision,
            'Lower': self.Lower,
            'Upper': self.Upper,
            'Root': self.Root,
            'HasLower': self.HasLower,
            'HasUpper': self.HasUpper,
            'HasRoot': self.HasRoot
        }
    def deserialize(self, pRoot):
        self.Name = pRoot['Name']
        self.Min = pRoot['Min']
        self.Max = pRoot['Max']
        self.Precision = pRoot['Precision']
        self.Lower = pRoot['Lower']
        self.Upper = pRoot['Upper']
        self.Root = pRoot['Root']
        self.HasLower = pRoot['HasLower']
        self.HasUpper = pRoot['HasUpper']
        self.HasRoot = pRoot['HasRoot']
        return self
    
class Target:
    def __init__(self):
        self.Price = 0.0
        self.Lower = 0.0
        self.Upper = 0.0
        self.HasLower = False
        self.HasUpper = False
    def serialize(self):
        return {
            'Price': self.Price,
            'Lower': self.Lower,
            'Upper': self.Upper,
            'HasLower': self.HasLower,
            'HasUpper': self.HasUpper
        }
    def deserialize(self, pRoot):
        self.Price = pRoot['Price']
        self.Lower = pRoot['Lower']
        self.Upper = pRoot['Upper']
        self.HasLower = pRoot['HasLower']
        self.HasUpper = pRoot['HasUpper']
        return self
    
class ImpliedContractFeatureResults:
    def __init__(self):
        self.FeaturesToSolve = []
        self.Target = Target()
    def serialize(self):
        Results = self.Target.serialize()
        Results['FeaturesToSolve'] = [item.serialize() for item in self.FeaturesToSolve]
        return Results
    def deserialize(self, pRoot):
        self.FeaturesToSolve = [FeatureToSolve().deserialize(item) for item in pRoot['FeaturesToSolve']]
        self.Target = Target().deserialize(pRoot)
        return self

class ZeroCoupon:
    def __init__(self):
        self.MaturityDate = ''
        self.Quantity = 0.0
        self.Value = 0.0
    def serialize(self):
        return {
            'MaturityDate': self.MaturityDate,
            'Quantity': self.Quantity,
            'Value': self.Value
        }
    def deserialize(self, pRoot):
        self.MaturityDate = pRoot['MaturityDate']
        self.Quantity = pRoot['Quantity']
        self.Value = pRoot['Value']
        return self

class CallPut:
    def __init__(self):
        self.PayoffKind = PayoffKind.CALL_TYPE
        self.MaturityDate = ''
        self.Strike = 0.0
        self.Quantity = 0.0
        self.Price = 0.0
    def serialize(self):
        return {
            'PayoffKind': self.PayoffKind.upper(),
            'MaturityDate': self.MaturityDate,
            'Strike': self.Strike,
            'Quantity': self.Quantity,
            'Price': self.Price
        }
    def deserialize(self, pRoot):
        self.PayoffKind = pRoot['PayoffKind']
        self.MaturityDate = pRoot['MaturityDate']
        self.Strike = pRoot['Strike']
        self.Quantity = pRoot['Quantity']
        self.Price = pRoot['Price']
        return self
    
class Replication:
    def __init__(self):
        self.Spot = 0.0
        self.Payoff = 0.0
        self.Replication = 0.0
    def serialize(self):
        return {
            'Spot': self.Spot,
            'Payoff': self.Payoff,
            'Replication': self.Replication
        }
    def deserialize(self, pRoot):
        self.Spot = pRoot['Spot']
        self.Payoff = pRoot['Payoff']
        self.Replication = pRoot['Replication']
        return self
    
class StaticReplication1DResults:
    def __init__(self):
        self.ZeroCoupon = ZeroCoupon()
        self.Vanillas = []
        self.Replications = []
        self.Price = 0.0
    def serialize(self):
        return {
            'ZeroCoupon': self.ZeroCoupon.serialize(),
            'Vanillas': [item.serialize() for item in self.Vanillas],
            'Replications': [item.serialize() for item in self.Replication],
            'Price': self.Price
        }
    def deserialize(self, pRoot):
        self.ZeroCoupon = ZeroCoupon().deserialize(pRoot['ZeroCoupon'])
        self.Vanillas = [Vanilla().deserialize(item) for item in pRoot['Vanillas']]
        self.Replications = [Replication().deserialize(item) for item in pRoot['Replications']]
        self.Price = pRoot['Price']
        return self

class ModelImpliedVolatilitySlice:
    def __init__(self, Space=0.0):
        self.Space = Space
        self.Market = 0.0
        self.Model = PricingResult()
        self.Error = 0.0
    def serialize(self):
        return {
            'Space': self.Space,
            'Market': self.Market,
            'Model': self.Model.serialize(),
            'Error': self.Error
        }
    def deserialize(self, pRoot):
        self.Space = pRoot['Space']
        self.Market = pRoot['Market']
        self.Model.deserialize(pRoot['Model'])
        self.Error = pRoot['Error']
        return self
    
class ModelImpliedVolatilityResults:
    def __init__(self):
        self.Ticker = ''
        self.MaturityDate = ''
        self.SpaceKind = SpaceKind.FORWARD_MONEYNESS_PCT
        self.PriceKind = PriceKind.VOLATILITY_PCT
        self.PayoffKind = PayoffKind.CALL_TYPE
        self.Slice = []
    def serialize(self):
        return {
            'Ticker': self.Ticker,
            'MaturityDate': self.MaturityDate,
            'SpaceKind': self.SpaceKind.upper(),
            'PriceKind': self.PriceKind.upper(),
            'PayoffKind': self.PayoffKind.upper(),
            'Slice': [item.serialize() for item in self.Slice]
        }
    def deserialize(self, pRoot):
        self.Ticker = pRoot['Ticker']
        self.MaturityDate = pRoot['MaturityDate']
        self.SpaceKind = pRoot['SpaceKind']
        self.PriceKind = pRoot['PriceKind']
        self.PayoffKind = pRoot['PayoffKind']
        self.Slice = [ModelImpliedVolatilitySlice().deserialize(item) for item in pRoot['Slice']]
        return self
    
class OptionSpaceValue:
    def __init__(self, Space=0.0):
        self.Space = Space
        self.Value = 0.0
    def serialize(self):
        return {
            'Space': self.Space,
            'Value': self.Value
        }
    def deserialize(self, pRoot):
        self.Space = pRoot['Space']
        self.Value = pRoot['Value']
        return self
    
class HestonImpliedVolatilityResults:
    def __init__(self):
        self.SpaceKind = SpaceKind.FORWARD_MONEYNESS_PCT
        self.ValueKind = PriceKind.VOLATILITY_PCT
        self.SpaceSize = 0
        self.RiskFreeRate = 0.0
        self.InitialSpot = 0.0
        self.MaturityTime = 0.0
        self.InitialVolatility = 0.0
        self.VarianceVolatility = 0.0
        self.LongTermVolatility = 0.0
        self.MeanReversionRate = 0.0
        self.SpotVarianceCorrelation = 0.0
        self.Slice = []
    def serialize(self):
        return {
            'SpaceKind': self.SpaceKind,
            'ValueKind': self.ValueKind,
            'SpaceSize': self.SpaceSize,
            'RiskFreeRate': self.RiskFreeRate,
            'InitialSpot': self.InitialSpot,
            'MaturityTime': self.MaturityTime,
            'InitialVolatility': self.InitialVolatility,
            'VarianceVolatility': self.VarianceVolatility,
            'LongTermVolatility': self.LongTermVolatility,
            'MeanReversionRate': self.MeanReversionRate,
            'SpotVarianceCorrelation': self.SpotVarianceCorrelation,
            'Slice': [item.serialize() for item in self.Slice]
        }
    def deserialize(self, pRoot):
        self.SpaceKind = pRoot['SpaceKind'] 
        self.ValueKind = pRoot['ValueKind'] 
        self.SpaceSize = pRoot['SpaceSize'] 
        self.RiskFreeRate = pRoot['RiskFreeRate'] 
        self.InitialSpot = pRoot['InitialSpot'] 
        self.MaturityTime = pRoot['MaturityTime'] 
        self.InitialVolatility = pRoot['InitialVolatility'] 
        self.VarianceVolatility = pRoot['VarianceVolatility'] 
        self.LongTermVolatility = pRoot['LongTermVolatility'] 
        self.MeanReversionRate = pRoot['MeanReversionRate'] 
        self.SpotVarianceCorrelation = pRoot['SpotVarianceCorrelation'] 
        self.Slice = [OptionSpaceValue().deserialize(item) for item in pRoot['Slice']]
        return self
    
class TestImpliedVolatilityComputationSpace:
    def __init__(self, pSpace = 0.0):
        self.Space = pSpace
    def serialize(self):
        return {
            'Space': self.Space
        }
    def deserialize(self, pRoot):
        self.Space = pRoot['Space']
        return self
    
class TestImpliedVolatilityComputationValue:
    def __init__(self, pValue = 0.0):
        self.Value = pValue
    def serialize(self):
        return {
            'Value': self.Value
        }
    def deserialize(self, pRoot):
        self.Value = pRoot['Value']
        return self

class TestImpliedVolatilityComputationError:
    def __init__(self):
        self.Error = 0
        self.Status = False
    def serialize(self):
        return {
            'Error': self.Error,
            'Status': self.Status
        }
    def deserialize(self, pRoot):
        self.Error = pRoot['Error']
        self.Status = pRoot['Status']
        return self
    
class TestImpliedVolatilityComputationErrorMatrix:
    def __init__(self):
        self.Rows = []
        self.Cols = []
        self.Data = [[]]
    def serialize(self):
        return {
            'Rows': self.Rows,
            'Cols': self.Cols,
            'Data': [[item.serialize() for item in jtem] for jtem in self.Data]
        }
    def deserialize(self, pRoot):
        self.Rows = pRoot['Rows']
        self.Cols = pRoot['Cols']
        self.Data = [[TestImpliedVolatilityComputationError().deserialize(item) for item in jtem] for jtem in pRoot['Data']]
        return self
    
class TestImpliedVolatilityComputationResults:
    def __init__(self):
        self.InitialGuessMethod = InitialGuessMethod.LEGACY
        self.ToleranceExponant = 8
        self.MaximumIterations = 100
        self.Spaces = []
        self.Values = []
        self.Errors = TestImpliedVolatilityComputationErrorMatrix()
        self.AverageError = 0.0
        self.AverageIterations = 0.0
    def serialize(self):
        return {
            'InitialGuessMethod': self.InitialGuessMethod.upper(),
            'ToleranceExponant': self.ToleranceExponant,
            'MaximumIterations': self.MaximumIterations,
            'Spaces': [item.serialize() for item in self.Spaces],
            'Values': [item.serialize() for item in self.Values],
            'Errors': self.Errors.serialize(),
            'AverageError': self.AverageError,
            'AverageIterations': self.AverageIterations
        }
    def deserialize(self, pRoot):
        self.InitialGuessMethod = pRoot['InitialGuessMethod']
        self.ToleranceExponant = pRoot['ToleranceExponant']
        self.MaximumIterations = pRoot['MaximumIterations']
        self.Spaces = [TestImpliedVolatilityComputationSpace().deserialize(item) for item in pRoot['Spaces']]
        self.Values = [TestImpliedVolatilityComputationValue().deserialize(item) for item in pRoot['Values']]
        self.Errors = TestImpliedVolatilityComputationErrorMatrix().deserialize(pRoot['Errors'])
        self.AverageError = pRoot['AverageError']
        self.AverageIterations = pRoot['AverageIterations']
        return self

class LadderScenario:
    def __init__(self, Name='', BumpKind=BumpKind.ADDITIVE, BumpUnit=BumpUnit.BASIS_POINT, BumpValue=0.0):
        self.Name = Name
        self.BumpKind = BumpKind
        self.BumpUnit = BumpUnit
        self.BumpValue = BumpValue
    def serialize(self):
        return {
            'Name': self.Name,
            'BumpKind': self.BumpKind,
            'BumpUnit': self.BumpUnit,
            'BumpValue': self.BumpValue
        }
    def deserialize(self, pRoot):
        self.Name = pRoot['Name']
        self.BumpKind = pRoot['BumpKind']
        self.BumpUnit = pRoot['BumpUnit']
        self.BumpValue = pRoot['BumpValue']
        return self

class LadderPlot:
    def __init__(self, Scenarios=[]):
        self.Scenarios = Scenarios
        self.Results = PricingResults()
        self.Mean = 0.0
        self.Lower = 0.0
        self.Upper = 0.0
        self.Stddev = 0.0
    def serialize(self):
        return {
            'Scenarios': [item.serialize() for item in self.Scenarios],
            'Results': self.Results.serialize()
        }
    def deserialize(self, pRoot):
        self.Scenarios = [LadderScenario().deserialize(item) for item in pRoot['Scenarios']]
        self.Results = PricingResults().deserialize(pRoot['Results'])
        return self

class LadderResults:
    def __init__(self):
        self.LadderKind = LadderKind.MARKET
        self.Plots = []
        self.OutputNames = []
        self.CentralResult = PricingResults()
    def serialize(self):
        return {
            'LadderKind': self.LadderKind.upper(),
            'Plots': [item.serialize() for item in self.Plots],
            'OutputNames': [item.serialize() for item in self.OutputNames],
            'CentralResult': self.CentralResult.serialize()
        }
    def deserialize(self, pRoot):
        self.LadderKind = pRoot['LadderKind']
        self.Plots = [LadderPlot().deserialize(item) for item in pRoot['Plots']]
        self.OutputNames = [NameValueResult().deserialize(item) for item in pRoot['OutputNames']]
        self.CentralResult = PricingResults().deserialize(pRoot['CentralResult'])
        return self

class Decomposition:
    def __init__(self):
        self.Date = ''
        self.Price = PricingResult()
        self.ProbaExists = PricingResult()
        self.ProbaPositive = PricingResult()
        self.ProbaIsKilled = PricingResult()
        self.ProbaHasBeenKilled = PricingResult()
    def serialize(self):
        return {
            'Date': self.Date,
            'Price': self.Price.serialize(),
            'ProbaExists': self.ProbaExists.serialize(),
            'ProbaPositive': self.ProbaPositive.serialize(),
            'ProbaIsKilled': self.ProbaIsKilled.serialize(),
            'ProbaHasBeenKilled': self.ProbaHasBeenKilled.serialize()
        }
    def deserialize(self, pRoot):
        self.Date = pRoot['Date']
        self.Price = PricingResult().deserialize(pRoot['Price'])
        self.ProbaExists = PricingResult().deserialize(pRoot['ProbaExists'])
        self.ProbaPositive = PricingResult().deserialize(pRoot['ProbaPositive'])
        self.ProbaIsKilled = PricingResult().deserialize(pRoot['ProbaIsKilled'])
        self.ProbaHasBeenKilled = PricingResult().deserialize(pRoot['ProbaHasBeenKilled'])
        return self
    
class ForwardFixing:
    def __init__(self):
        self.FixingDate = ''
        self.Ticker = ''
        self.Value = 0.0
        self.Currency = ''
    def serialize(self):
        return {
            'FixingDate': self.FixingDate,
            'Ticker': self.Ticker,
            'Value': self.Value,
            'Currency': self.Currency
        }
    def deserialize(self, pRoot):
        self.FixingDate = pRoot['FixingDate']
        self.Ticker = pRoot['Ticker']
        self.Value = pRoot['Value']
        self.Currency = pRoot['Currency']
        return self
    
class Barrier:
    def __init__(self):
        self.EventDate = ''
        self.EventScript = ''
        self.ProbaIn = PricingResult()
    def serialize(self):
        return {
            'EventDate': self.EventDate,
            'EventScript': self.EventScript,
            'ProbaIn': self.ProbaIn.serialize()
        }
    def deserialize(self, pRoot):
        self.EventDate = pRoot['EventDate']
        self.EventScript = pRoot['EventScript']
        self.ProbaIn = PricingResult().deserialize(pRoot['ProbaIn'])
        return self
    
class Convergence:
    def __init__(self):
        self.Trials = 0
        self.Result = PricingResult()
    def serialize(self):
        return {
            'Trials': self.Trials,
            'Result': self.Result.serialize()
        }
    def deserialize(self, pRoot):
        self.Trials = pRoot['Trials']
        self.Result = PricingResult().deserialize(pRoot['Result'])
        return self
    
class GetMCPriceWithDetailsResults:
    def __init__(self):
        self.Duration = PricingResult()
        self.Decomposition = []
        self.ForwardFixings = []
        self.Barriers = []
        self.Convergence = []
        self.ConvergenceSize = 1000
    def serialize(self):
        return {
            'Duration': self.Duration.serialize(),
            'Decomposition': [item.serialize() for item in self.Decomposition],
            'ForwardFixings': [item.serialize() for item in self.ForwardFixings],
            'Barriers': [item.serialize() for item in self.Barriers],
            'Convergence': [item.serialize() for item in self.Convergence],
            'ConvergenceSize': self.ConvergenceSize
        }
    def deserialize(self, pRoot):
        self.Duration = PricingResult().deserialize(pRoot['Duration'])
        self.Decomposition = [Decomposition().deserialize(item) for item in pRoot['Decomposition']]
        self.ForwardFixings = [ForwardFixing().deserialize(item) for item in pRoot['ForwardFixings']]
        self.Barriers = [Barrier().deserialize(item) for item in pRoot['Barriers']]
        self.Convergence = [Convergence().deserialize(item) for item in pRoot['Convergence']]
        self.ConvergenceSize = 0.0
        return self
    
class Observable:
    def __init__(self):
        self.Date = ''
        self.Epoch = 0
        self.Value = 0.0
        self.Status = False
    def serialize(self):
        return {
            'Date': self.Date,
            'Epoch': self.Epoch,
            'Value': self.Value,
            'Status': self.Status
        }
    def deserialize(self, pRoot):
        self.Date = pRoot['Date']
        self.Epoch = pRoot['Epoch']
        self.Value = pRoot['Value']
        self.Status = pRoot['Status']
        return self
    
class Observation:
    def __init__(self, Kind=ObservableKind.BASKET, Observable=None):
        self.Kind = Kind
        self.Observable = Observable
        self.TimeSeries = []
    def serialize(self):
        Result = self.Observable.serialize()
        Result['Kind'] = self.Kind.upper()
        Result['TimeSeries'] = [item.serialize() for item in self.TimeSeries]
        return Result
    def deserialize(self, pRoot):
        self.Kind = pRoot['Kind']
        self.TimeSeries = [Observable().deserialize(item) for item in pRoot['TimeSeries']]
        return self
    
class DataResult:
    def __init__(self):
        self.Schedule = []
        self.Observations = []
    def serialize(self):
        return {
            'Schedule': self.Schedule,
            'Observations': [item.serialize() for item in self.Observations]
        }
    def deserialize(self, pRoot):
        self.Observations = [Observation().deserialize(item) for item in pRoot['Observations']]
        self.Schedule = pRoot['Schedule']
        return self
    
class IObservable:
    def serialize(self):
        raise NotImplementedError
    def deserialize(self, _):
        raise NotImplementedError
    
class BasketObservable(IObservable):
    def __init__(self, Basket=[], ForwardStartDate='', BasketKind=BasketKind.BASKET, StrikeKind=StrikeKind.ASIAN):
        self.Basket = Basket
        self.ForwardStartDate = ForwardStartDate
        self.BasketKind = BasketKind
        self.StrikeKind = StrikeKind
    def serialize(self):
        return {
            'Basket': [item.serialize() for item in self.Basket],
            'ForwardStartDate': self.ForwardStartDate,
            'BasketKind': self.BasketKind.upper(),
            'StrikeKind': self.StrikeKind.upper()
        }
    def deserialize(self, pRoot):    
        self.Basket = [BasketItem().deserialize(item) for item in pRoot['Basket']]
        self.ForwardStartDate = pRoot['ForwardStartDate']
        self.BasketKind = pRoot['BasketKind']
        self.StrikeKind = pRoot['StrikeKind']
        return self