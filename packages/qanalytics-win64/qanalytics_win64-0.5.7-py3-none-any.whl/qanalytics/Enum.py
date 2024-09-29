from enum import auto
from strenum import StrEnum

class LogLevel(StrEnum):
    INFO = auto()
    WARNING = auto()
    ERR = auto()
    EXCEPTION = auto()
    SUCCESS = auto()
    FAILURE = auto()

class AssetClass(StrEnum):
    SHARE = auto()
    FUND = auto()
    INDEX = auto()
    EXCHANGE_RATE = auto()
    ZERO_COUPON_BOND = auto()
    DEPOSIT_RATE = auto()
    SWAP_RATE = auto()

class AssetKind(StrEnum):
    EQUITY = auto()
    FOREIGN_EXCHANGE = auto()
    INTEREST_RATE = auto()

class EventKind(StrEnum):
    BARRIER = auto()
    CHOICE = auto()
    FIXING = auto()
    NOTHING = auto()
    PAYMENT = auto()
    PURCHASE = auto()
    RECEIPT = auto()
    SALE = auto()
    SETTING = auto()

class ContractKind(StrEnum):
    CONSOLE = auto()
    FILE = auto()
    AIRGBAG_CERTIFICATE_EXAMPLE = auto()
    AMERICAN_OPTION_EXAMPLE = auto()
    ASIAN_OPTION_EXAMPLE = auto()
    BARRIER_OPTION_EXAMPLE = auto()
    BARRIER_REVERSE_CONVERTIBLE_EXAMPLE = auto()
    BONUS_CERTIFICATE_EXAMPLE = auto()
    BUTTERFLY_SPREAD_EXAMPLE = auto()
    CAPPED_BONUS_CERTIFICATE_EXAMPLE = auto()
    CONDOR_SPREAD_EXAMPLE = auto()
    DIGITAL_OPTION_EXAMPLE = auto()
    DISCOUNT_CERTIFICATE_EXAMPLE = auto()
    DOUBLE_BARRIER_OPTION_EXAMPLE = auto()
    EUROPEAN_OPTION_EXAMPLE = auto()
    MULTI_ASSET_OPTION_EXAMPLE = auto()
    OUT_PERFORMANCE_BONUS_CERTIFICATE_EXAMPLE = auto()
    REVERSE_CONVERTIBLE_EXAMPLE = auto()
    RISK_REVERSAL_EXAMPLE = auto()
    SPREAD_OPTION_EXAMPLE = auto()
    STRADDLE_EXAMPLE = auto()
    STRANGLE_EXAMPLE = auto()
    TWIN_WIN_CERTIFICATE_EXAMPLE = auto()
    AUTOCALL = auto()
    VANILLA = auto()

class BasketKind(StrEnum):
    BASKET = auto()
    BEST_OF = auto()
    RAINBOW = auto()
    WORST_OF = auto()

class StrikeKind(StrEnum):
    ASIAN = auto()
    LOOKBACK_MIN = auto()
    LOOKBACK_MAX = auto()

class BarrierKind(StrEnum):
    KNOCK_OUT = auto()
    KNOCK_IN = auto()

class Calendar(StrEnum):
    DUMMY = auto()

class ModelName(StrEnum):
    BLACK_SCHOLES_MODEL = auto()
    BLACK_SCHOLES_TERM_STRUCTURE_MODEL = auto()
    DEFAULT_MODEL = auto()
    DUPIRE_LOCAL_VOLATILITY_MODEL = auto()
    FREE_MODEL = auto()
    HESTON_STOCHASTIC_VOLATILITY_MODEL = auto()

class BlackScholesCalibrationKind(StrEnum):
    MANUAL = auto()
    AT_THE_MONEY_FORWARD = auto()

class Basis(StrEnum):
    ACT_365 = auto()

class SmoothingType(StrEnum):
    NONE = auto()
    LOWER = auto()
    SYMETRIC = auto()
    UPPER = auto()

class PricingMethod(StrEnum):
    MONTE_CARLO = auto()
    FINITE_DIFFERENCE = auto()
    STATIC_REPLICATION = auto()
    AUTOMATIC_ADJOINT_DIFFERENTIATION = auto()

class SpotVolatilityDynamic(StrEnum):
    STICKY_STRIKE = auto()
    STICKY_DELTA = auto()
    STICKY_OPTION = auto()

class GreekDirection(StrEnum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()

class BoundaryCondition(StrEnum):
    DIRICHLET = auto()
    NEUMANN = auto()

class SequenceKind(StrEnum):
    UNIFORM = auto()
    CONSTANT = auto()
    CHEBYCHEV = auto()

class ObservationKind(StrEnum):
    FILE = auto()
    SPOT = auto()

class InitialGuessMethod(StrEnum):
    LEGACY = auto()
    STEFANICA_RADOICIC = auto()

class BasketKind(StrEnum):
    BASKET = auto()
    BEST_OF = auto()
    RAINBOW = auto()
    WORST_OF = auto()

class BarrierKind(StrEnum):
    KNOCK_OUT = auto()
    KNOCK_IN = auto()

class BarrierType(StrEnum):
    DOWN = auto()
    UP = auto()

class PayoffKind(StrEnum):
    CALL_TYPE = auto()
    PUT_TYPE = auto()

class BumpKind(StrEnum):
    MULTIPLICATIVE = auto()
    ADDITIVE = auto()
    ASSIGNMENT = auto()
    HYBRID = auto()

class LadderKind(StrEnum):
    MARKET = auto()
    CONTRACT = auto()

class BumpUnit(StrEnum):
    PERCENTAGE = auto()
    BASIS_POINT = auto()
    NONE = auto()

class SpaceKind(StrEnum):
    STRIKE = auto()
    MONEYNESS = auto()
    FORWARD_MONEYNESS = auto()
    MONEYNESS_PCT = auto()
    FORWARD_MONEYNESS_PCT = auto()
    LOG_MONEYNESS = auto()
    LOG_FORWARD_MONEYNESS = auto()

class PriceKind(StrEnum):
    CALL_PRICE = auto()
    PUT_PRICE = auto()
    CALL_PRICE_VS_SPOT = auto()
    PUT_PRICE_VS_SPOT = auto()
    CALL_PRICE_VS_SPOT_PCT = auto()
    PUT_PRICE_VS_SPOT_PCT = auto()
    VOLATILITY = auto()
    VOLATILITY_PCT = auto()
    VARIANCE = auto()
    TOTAL_VOLATILITY = auto()
    TOTAL_VARIANCE = auto()

class ObservableKind(StrEnum):
    BASKET = auto()