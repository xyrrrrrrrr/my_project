import os


def get_objects(instruct):
    instruct = instruct.split()
    return instruct[1], instruct[-1]

def get_motion(instruct):
    instruct = instruct.split()
    if 'LEFT' in instruct:
        return 'LEFT'
    elif 'RIGHT' in instruct:
        return 'RIGHT'
    elif 'UP' in instruct:
        return 'UP'
    elif 'DOWN' in instruct:
        return 'DOWN'
    else:
        RuntimeError('No motion detected')