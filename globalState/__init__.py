_global_state = {
    'patterns': [],
    'gestures': []
}


def get_global_state(key):
    global _global_state
    try:
        return _global_state[key]
    except NameError:
        return None


def set_global_state(key, value):
    global _global_state
    _global_state[key] = value


def get_gestures():
    return get_global_state('gestures')


def get_patterns():
    return get_global_state('patterns')


def set_gestures(gestures):
    set_global_state('gestures', gestures)


def set_patterns(patterns):
    set_global_state('patterns', patterns)
