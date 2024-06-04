DEFAULT_WARMUP_KM = 1.5
DEFAULT_COOL_DOWN_KM = 1.5

MOCK_DATA = {
    # Suggestions for the athlete: unit: min-max normalised z-score values
    'suggestion': [
    [0.5, 0.7, 0.1, 0.2, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
    [0.5, 0.7, 0.1, 0.2, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
    [0.5, 0.7, 0.1, 0.2, 1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.5, 0.7, 0.1, 0.2, 1.0, 0.0, 0.0]
],
    # output by model: Range of stdv and mean
    'range_per_metric' : {
        "nr. sessions": {"min": 0, "max": 4},
        "total km": {"min": 0, "max": 4},
        "km Z3-4": {"min": 0, "max": 4},
        "km Z5-T1-T2": {"min": 0, "max": 4},
        "km sprinting": {"min": 0, "max": 4},
        "strength training": {"min": 0, "max": 1},
        "hours alternative": {"min": 0, "max": 1}
    },

    # Retrieved from database
    'athlete_data' : {
        "nr. sessions": {"mean": 1, "std_dev": 0.2},
        "total km": {"mean": 5, "std_dev": 1},
        "km Z3-4": {"mean": 1, "std_dev": 1},
        "km Z5-T1-T2": {"mean": 2, "std_dev": 1},
        "km sprinting": {"mean": 0.5, "std_dev": 1},
        "strength training": {"mean": 0.4, "std_dev": 1},
        "hours alternative": {"mean": 0.5, "std_dev": 1}
    }
}

INTERVALS = {
        'default': {
            'effort': {'Z5': 1.0},
            'recovery': {'Z2': 1.0}
    }
}