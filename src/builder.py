import numpy as np
import pprint
from config.config import DEFAULT_WARMUP_KM, DEFAULT_COOL_DOWN_KM, MOCK_DATA, INTERVALS

def convert_to_absolute(suggestion, range_data, athlete_data):
    """
    Converts relative values in the 'suggestion' to absolute values based on 'range_data' and 'athlete_data'.
    Parameters:
    suggestion (list): A list of relative values to be converted.
    range_data (dict): A dictionary containing the range (min and max) of the dataset.
    athlete_data (dict): A dictionary containing the mean and standard deviation for the athlete.
    Returns:
    absolute_suggestion (dict): A dictionary with the same keys as 'range_data' and 'athlete_data', 
                               but with the values from 'suggestion' converted to absolute terms.
    The function 
    1. scales the values in the 'suggestion' using the range of the dataset (min and max values in 'range_data').
    2. converts these scaled values to absolute terms using the athlete's mean and standard deviation from 'athlete_data'.
    """
    keys = list(range_data.keys())
    absolute_suggestion = {}
    suggestion = list(map(list, zip(*suggestion)))
    suggestion_np = np.array(suggestion)

    for i, key in enumerate(keys):
        min_val = range_data[key]['min']
        max_val = range_data[key]['max']
        mean = athlete_data[key]['mean']
        std_dev = athlete_data[key]['std_dev']
        # Scale the values using the range of the dataset
        scaled_values = suggestion_np[i, :] * (max_val - min_val) + min_val
        # Convert to absolute terms using the athlete's mean and standard deviation
        absolute_values = scaled_values * std_dev + mean
        absolute_suggestion[key] = absolute_values.tolist()
    return absolute_suggestion

def post_process(absolute_suggestion):
    """
    Post-process the absolute suggestion values.
    1. Round values for 'nr. sessions' and 'strength training'
    2. Set all negative values to zero
    3. Add "km Z5-T1-T2" and "km sprinting" together to "km Z5"
    """
    for key in absolute_suggestion.keys():
        # 1. Round values for 'nr. sessions' and 'strength training'
        if key in ['nr. sessions', 'strength training']:
            absolute_suggestion[key] = [round(val) for val in absolute_suggestion[key]]
        
        # 2. Set all negative values to zero
        absolute_suggestion[key] = [val if val >= 0 else 0 for val in absolute_suggestion[key]]
    
    # 3. Add "km Z5-T1-T2" and "km sprinting" together to "km Z5"
    if 'km Z5-T1-T2' in absolute_suggestion and 'km sprinting' in absolute_suggestion:
        absolute_suggestion['km Z5'] = [sum(x) for x in zip(absolute_suggestion['km Z5-T1-T2'], absolute_suggestion['km sprinting'])]
        del absolute_suggestion['km Z5-T1-T2']
        del absolute_suggestion['km sprinting']

    return absolute_suggestion

def create_training_plan(suggestion):
    """
    Creates a 7-day training plan based on the provided suggestion.

    Parameters:
    suggestion (dict): A dictionary containing the suggested training load in absolute units. 

    Returns:
    training_plan (dict): A dictionary representing the 7-day training plan. Each day includes a running plan with warmup, 
                          main intervals, and cooldown, as well as strength training and alternative hours.

    The function iterates over each day of the week, and for each day, it creates a running plan 
    based on the remaining kilometers for the day. The running plan includes a warmup, main intervals, 
    and a cooldown. The main intervals are created in a loop until the remaining kilometers for the day 
    or the remaining kilometers for Z5 are exhausted. Each interval includes an effort and recovery phase. 
    If the remaining kilometers are not enough for an interval, the interval is not included in the plan. 
    The function also includes strength training and alternative hours in the plan for each day.
    """
    
    interval_type = 'default'
    training_plan = {}

    for i in range(7):
        remaining_km = suggestion['total km'][i]  # Get the remaining km for the day

        if remaining_km < DEFAULT_WARMUP_KM:
            continue

        # Add warumup and cooldown to the plan
        running_plan = {'session_1': {'warmup': {'Z2': DEFAULT_WARMUP_KM}, 'main': {}}}
        remaining_km -= running_plan['session_1']['warmup']['Z2']

        if remaining_km > 0:
            running_plan['session_1']['cooldown'] = {'Z2': min(DEFAULT_COOL_DOWN_KM, remaining_km)}
            remaining_km -= running_plan['session_1']['cooldown']['Z2']

        # Add Zone 5 intervals to the plan
        interval_number = 1
        remaining_km_zone5 = suggestion['km Z5'][i]
        effort_key = list(INTERVALS[interval_type]['effort'].keys())[0]
        recovery_key = list(INTERVALS[interval_type]['recovery'].keys())[0]
        km_effort = INTERVALS[interval_type]['effort'][effort_key]
        km_recovery = INTERVALS[interval_type]['recovery'][recovery_key]
        
        while remaining_km_zone5 >= km_effort and remaining_km >= km_effort + km_recovery:
            running_plan['session_1']['main'][f'interval_{interval_number}'] = [] # Initialize the interval list
            running_plan['session_1']['main'][f'interval_{interval_number}'].append({effort_key: km_effort})
            running_plan['session_1']['main'][f'interval_{interval_number}'].append({recovery_key: km_recovery})
            remaining_km -= (km_effort + km_recovery)
            remaining_km_zone5 -= km_effort
            interval_number += 1

        day_plan = {
            'running': running_plan,
            'strength': suggestion['strength training'][i],
            'alternative': suggestion['hours alternative'][i]
        }
        training_plan[f'day_{i+1}'] = day_plan

    return training_plan

def run():
    pp = pprint.PrettyPrinter(indent=0.5)
    absolute_suggestion = convert_to_absolute(MOCK_DATA['suggestion'], MOCK_DATA['range_per_metric'], MOCK_DATA['athlete_data'])
    print("Absolute training load:")
    pp.pprint(absolute_suggestion)
    post_processed = post_process(absolute_suggestion)
    print("Absolute training load:") 
    pp.pprint(post_processed)
    print("Derived training_plan \n")
    pp.pprint(create_training_plan(post_processed))

if __name__ == '__main__':
    run()