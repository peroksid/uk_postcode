import logging

from .handlers import get_handler


logger = logging.getLogger(__name__)


START_STATE = "S_INIT"
TRANSITIONS = {
    "S_AA": [
        "T_AA9"
    ],
    "S_X9": [
        "T_X9A"
    ],
    "S_A9": [
        "T_A99",
        "T_A9A3",
        "T_A9A2",
        "T_A9A1",
        "T_X1"
    ],
    "S_X": [
        "T_X92",
        "T_X93",
        "T_X94",
        "T_X91"
    ],
    "S_A9A": [
        "T_X15"
    ],
    "S_AA99": [
        "T_X17"
    ],
    "S_INIT": [
        "T_A"
    ],
    "S_A": [
        "T_A9",
        "T_AA"
    ],
    "S_X9A": [
        "T_X9AA"
    ],
    "S_AA9A": [
        "T_X16"
    ],
    "S_AA9": [
        "T_AA9A4",
        "T_AA9A5",
        "T_AA9A6",
        "T_AA9A7",
        "T_AA99",
        "T_AA9A8",
        "T_AA9A10",
        "T_X2",
        "T_X3",
        "T_X4",
        "T_X5",
        "T_X6",
        "T_X7",
        "T_X10",
        "T_X11",
        "T_X12",
        "T_X13",
        "T_AA9A3",
        "T_AA9A1",
        "T_AA9A2"
    ],
    "S_A99": [
        "T_X14"
    ]
}
STATES = {
    "T_AA9A10": "S_AA9A",
    "T_A9": "S_A9",
    "T_AA99": "S_AA99",
    "T_AA9": "S_AA9",
    "T_AA9A2": "S_AA9A",
    "T_AA9A3": "S_AA9A",
    "T_AA9A1": "S_AA9A",
    "T_AA9A6": "S_AA9A",
    "T_AA9A7": "S_AA9A",
    "T_AA9A4": "S_AA9A",
    "T_AA9A5": "S_AA9A",
    "T_AA9A8": "S_AA9A",
    "T_X7": "S_X",
    "T_X6": "S_X",
    "T_X5": "S_X",
    "T_X4": "S_X",
    "T_X3": "S_X",
    "T_X2": "S_X",
    "T_X1": "S_X",
    "T_A9A1": "S_A9A",
    "T_A9A2": "S_A9A",
    "T_A9A3": "S_A9A",
    "T_X9A": "S_X9A",
    "T_X93": "S_X9",
    "T_X92": "S_X9",
    "T_X91": "S_X9",
    "T_X94": "S_X9",
    "T_X13": "S_X",
    "T_X12": "S_X",
    "T_X11": "S_X",
    "T_X10": "S_X",
    "T_X17": "S_X",
    "T_X16": "S_X",
    "T_X15": "S_X",
    "T_X14": "S_X",
    "T_X9AA": "S_X9AA",
    "T_A": "S_A",
    "T_AA": "S_AA",
    "T_A99": "S_A99"
}
ACCUMULATORS = {
    "T_AA9A10": [
        "A_SECTOR",
        "A_OUTWARD"
    ],
    "T_A9": [
        "A_OUTWARD",
        "A_TOWN",
        "A_SECTOR"
    ],
    "T_AA99": [
        "A_SECTOR",
        "A_OUTWARD",
        "A_TOWN"
    ],
    "T_AA9": [
        "A_OUTWARD",
        "A_SECTOR",
        "A_TOWN"
    ],
    "T_AA9A2": [
        "A_OUTWARD",
        "A_SECTOR"
    ],
    "T_AA9A3": [
        "A_SECTOR",
        "A_OUTWARD"
    ],
    "T_AA9A1": [
        "A_OUTWARD",
        "A_SECTOR"
    ],
    "T_AA9A6": [
        "A_SECTOR",
        "A_OUTWARD"
    ],
    "T_AA9A7": [
        "A_SECTOR",
        "A_OUTWARD"
    ],
    "T_AA9A4": [
        "A_SECTOR",
        "A_OUTWARD"
    ],
    "T_AA9A5": [
        "A_OUTWARD",
        "A_SECTOR"
    ],
    "T_AA9A8": [
        "A_SECTOR",
        "A_OUTWARD"
    ],
    "T_X7": [
        "A_SECTOR"
    ],
    "T_X6": [
        "A_SECTOR"
    ],
    "T_X5": [
        "A_SECTOR"
    ],
    "T_X4": [
        "A_SECTOR"
    ],
    "T_X3": [
        "A_SECTOR"
    ],
    "T_X2": [
        "A_SECTOR"
    ],
    "T_X1": [
        "A_SECTOR"
    ],
    "T_A9A1": [
        "A_OUTWARD",
        "A_SECTOR"
    ],
    "T_A9A2": [
        "A_SECTOR",
        "A_OUTWARD"
    ],
    "T_A9A3": [
        "A_OUTWARD",
        "A_SECTOR"
    ],
    "T_X9A": [
        "A_UNIT",
        "A_INWARD"
    ],
    "T_X93": [
        "A_SECTOR",
        "A_INWARD"
    ],
    "T_X92": [
        "A_INWARD",
        "A_SECTOR"
    ],
    "T_X91": [
        "A_INWARD",
        "A_SECTOR"
    ],
    "T_X94": [
        "A_SECTOR",
        "A_INWARD"
    ],
    "T_X13": [
        "A_SECTOR"
    ],
    "T_X12": [
        "A_SECTOR"
    ],
    "T_X11": [
        "A_SECTOR"
    ],
    "T_X10": [
        "A_SECTOR"
    ],
    "T_X17": [
        "A_SECTOR"
    ],
    "T_X16": [
        "A_SECTOR"
    ],
    "T_X15": [
        "A_SECTOR"
    ],
    "T_X14": [
        "A_SECTOR"
    ],
    "T_X9AA": [
        "A_UNIT",
        "A_INWARD"
    ],
    "T_A": [
        "A_OUTWARD",
        "A_SECTOR",
        "A_AREA"
    ],
    "T_AA": [
        "A_OUTWARD",
        "A_AREA",
        "A_SECTOR"
    ],
    "T_A99": [
        "A_TOWN",
        "A_SECTOR",
        "A_OUTWARD"
    ]
}
POSITIVES = {
    "T_AA9A10": [
        "AE_OUTWARD_SE1",
        "X_P"
    ],
    "T_A9": [
        "C_DIGIT"
    ],
    "T_AA99": [
        "C_DIGIT"
    ],
    "T_AA9": [
        "C_DIGIT"
    ],
    "T_AA9A2": [
        "C_ALPHA",
        "AE_OUTWARD_EC2"
    ],
    "T_AA9A3": [
        "C_ALPHA",
        "AE_OUTWARD_EC3"
    ],
    "T_AA9A1": [
        "C_ALPHA",
        "AE_OUTWARD_EC1"
    ],
    "T_AA9A6": [
        "AE_OUTWARD_WC1",
        "C_ALPHA"
    ],
    "T_AA9A7": [
        "C_ALPHA",
        "AE_OUTWARD_WC2"
    ],
    "T_AA9A4": [
        "C_ALPHA",
        "AE_OUTWARD_EC4"
    ],
    "T_AA9A5": [
        "AE_OUTWARD_SW1",
        "C_ALPHA"
    ],
    "T_AA9A8": [
        "X_W",
        "AE_OUTWARD_NW1"
    ],
    "T_X7": [
        "AE_TOWN_0",
        "X_SPACE",
        "AE_AREA_FY"
    ],
    "T_X6": [
        "AE_AREA_CR",
        "X_SPACE",
        "AE_TOWN_0"
    ],
    "T_X5": [
        "X_SPACE",
        "AE_AREA_CM",
        "AE_TOWN_0"
    ],
    "T_X4": [
        "X_SPACE",
        "AE_TOWN_0",
        "AE_AREA_BS"
    ],
    "T_X3": [
        "X_SPACE",
        "AE_TOWN_0",
        "AE_AREA_BL"
    ],
    "T_X2": [
        "X_SPACE",
        "ARI_TOWN_0_123456789"
    ],
    "T_X1": [
        "X_SPACE",
        "ARI_AREA_0_BEGLMNSW"
    ],
    "T_A9A1": [
        "AE_OUTWARD_E1",
        "X_W"
    ],
    "T_A9A2": [
        "R_CP",
        "AE_OUTWARD_N1"
    ],
    "T_A9A3": [
        "R_ABCDEFGHIJKPSTUW",
        "AE_OUTWARD_W1"
    ],
    "T_X9A": [
        "C_ALPHA"
    ],
    "T_X93": [
        "X_0",
        "AE_TOWN_9"
    ],
    "T_X92": [
        "AE_AREA_NP",
        "X_0",
        "AE_AREA_CR",
        "AE_TOWN_9"
    ],
    "T_X91": [
        "R_123456789"
    ],
    "T_X94": [
        "X_0"
    ],
    "T_X13": [
        "X_SPACE",
        "AE_TOWN_0",
        "AE_AREA_SS"
    ],
    "T_X12": [
        "X_SPACE",
        "AE_TOWN_0",
        "AE_AREA_SL"
    ],
    "T_X11": [
        "AE_TOWN_0",
        "AE_AREA_PR",
        "X_SPACE"
    ],
    "T_X10": [
        "AE_TOWN_0",
        "AE_AREA_HA",
        "X_SPACE"
    ],
    "T_X17": [
        "X_SPACE"
    ],
    "T_X16": [
        "X_SPACE"
    ],
    "T_X15": [
        "X_SPACE"
    ],
    "T_X14": [
        "X_SPACE"
    ],
    "T_X9AA": [
        "C_ALPHA"
    ],
    "T_A": [
        "C_ALPHA"
    ],
    "T_AA": [
        "C_ALPHA"
    ],
    "T_A99": [
        "ARI_AREA_0_BEGLMNSW",
        "C_DIGIT"
    ]
}
NEGATIVES = {
    "T_A9": [
        "X_0"
    ],
    "T_AA99": [
        "AE_AREA_FY",
        "AE_AREA_HD",
        "AE_AREA_HR",
        "AE_AREA_WN",
        "AE_AREA_BR",
        "AE_AREA_SR",
        "AE_AREA_HX",
        "AE_AREA_HG",
        "AE_AREA_JE",
        "AE_AREA_SM",
        "AE_AREA_ZE",
        "AE_AREA_HA",
        "AE_AREA_LD",
        "AE_AREA_WC"
    ],
    "T_A": [
        "R_QVX"
    ],
    "T_X94": [
        "AE_TOWN_9"
    ],
    "T_AA": [
        "R_IJZ"
    ],
    "T_X9A": [
        "R_CIKMOV"
    ],
    "T_X9AA": [
        "R_CIKMOV"
    ],
    "T_X2": [
        "AE_AREA_AB",
        "AE_AREA_LL",
        "AE_AREA_SO"
    ]
}

for collection in (ACCUMULATORS, POSITIVES, NEGATIVES):
    for t_id, node in collection.items():
        collection[t_id] = [get_handler(x) for x in node]


def decode(code):
    state = START_STATE
    context = {}
    for index, char in enumerate(code):
        logger.debug('char: "%s"', char)
        logger.debug('states: %s', state)
        logger.debug('context %s', context)
        transitions = TRANSITIONS[state]
        logger.debug('transitions %s', transitions)
        for t in transitions:
            logger.debug('transition %s', t)
            positives = POSITIVES.get(t, [])
            logger.debug('positives %s', positives)
            positive_results = [x(context, char) for x in positives]
            if all(positive_results):
                negatives = NEGATIVES.get(t, [])
                logger.debug('negatives %s', negatives)
                negative_results = [x(context, char) for x in negatives]
                if not any(negative_results):
                    state = STATES.get(t)
                    logger.debug('new state %s', state)
                    logger.debug('accumulators %s', ACCUMULATORS.get(t, []))
                    for a in ACCUMULATORS.get(t, []):
                        a(context, char)
                    break
                else:
                    logger.debug('negatives rejected %s', negative_results)
            else:
                logger.debug('positives rejected %s', positive_results)
        else:
            raise RuntimeError("all transitions are inactive")
    return context
