# Speed ranges
SPEED_0_RANGE = range(0, 2)
SPEED_1_RANGE = range(2, 4)
SPEED_2_RANGE = range(4, 6)

# Reward factors for having a higher speed
REWARD_SPEED_0_FACTOR = 1.0
REWARD_SPEED_1_FACTOR = 1.3
REWARD_SPEED_2_FACTOR = 1.8

# Distance from center ranges
CENTER_DISTANCE_0_PERCENT = 0.25
CENTER_DISTANCE_1_PERCENT = 0.5
CENTER_DISTANCE_2_PERCENT = 0.75

# Reward factors for being closer to the center of the track
REWARD_CENTER_DISTAMCE_0_FACTOR = 1.3
REWARD_CENTER_DISTANCE_1_FACTOR = 1.8
REWARD_CENTER_DISTANCE_2_FACTOR = 1.0
REWARD_CENTER_DISTANCE_3_FACTOR = 0.1

# Desired max steering angle
MAX_STEERING_ANGLE = 20

# Reward factor for oversteering
REWARD_OVERSTEERING_FACTOR = 0.8


# Reward factors for being on the track
REWARD_ON_TRACK_FACTOR = 1.5
REWARD_OFF_TRACK_FACTOR = 0.001

# Reward factor for being on the short side of the track (left for counter-clockwise, right for clock-wise).
REWARD_SHORT_SIDE_FACTOR = 1.3

def reward_function(params):
    '''
    Reward Zoomie for (with descending priority):
        - Staying on the track
        - Staying on the short side of the track
        - Going fast 
        - Staying within 50% of the track width from the center of the track
        - Being closer to the end of the race
        - Not oversteering
    '''
    
    progress = params['progress']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    is_reversed = params['is_reversed']
    is_left_of_center = params['is_left_of_center']
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    steering_angle = abs(params['steering_angle'])  

    reward = 1.0

    # Ordered least to most important to give later functions more weight
    reward = process_steering(reward, steering_angle)
    reward = process_progress(reward, progress)
    reward = process_center_distance(reward, distance_from_center, track_width)
    reward = process_speed(reward, speed)
    reward = process_placement(reward, all_wheels_on_track, is_reversed, is_left_of_center)

    return float(reward)

def process_progress(reward, progress):
    reward *= (1 + (progress / 100.0))

    return reward

def process_steering(reward, steering_angle):
    if steering_angle > MAX_STEERING_ANGLE:
        reward *= REWARD_OVERSTEERING_FACTOR

    return reward

def process_speed(reward, speed):
    if speed in SPEED_0_RANGE:
        reward *= REWARD_SPEED_0_FACTOR
    elif speed in SPEED_1_RANGE:
        reward *= REWARD_SPEED_1_FACTOR
    elif speed in SPEED_2_RANGE:
        reward *= REWARD_SPEED_2_FACTOR

    return reward

def process_placement(
    reward,
    all_wheels_on_track,
    is_reversed,
    is_left_of_center
):
    if all_wheels_on_track:
        reward *= REWARD_ON_TRACK_FACTOR
    else:
        reward *= REWARD_OFF_TRACK_FACTOR

    if is_left_of_center and not is_reversed:
        reward *= REWARD_SHORT_SIDE_FACTOR
    elif not is_left_of_center and is_reversed:
        reward *= REWARD_SHORT_SIDE_FACTOR

    return reward

def process_center_distance(
    reward,
    distance, 
    track_width
):
    if distance <= CENTER_DISTANCE_0_PERCENT * track_width:
        reward *= REWARD_CENTER_DISTAMCE_0_FACTOR
    elif distance <= CENTER_DISTANCE_1_PERCENT * track_width:
        reward *= REWARD_CENTER_DISTANCE_1_FACTOR
    elif distance <= CENTER_DISTANCE_2_PERCENT * track_width:
        reward *= REWARD_CENTER_DISTANCE_2_FACTOR
    elif distance > CENTER_DISTANCE_2_PERCENT * track_width:
        reward *= REWARD_CENTER_DISTANCE_3_FACTOR
    
    return reward
