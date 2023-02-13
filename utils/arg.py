import argparse

def get_args():
    parser = argparse.ArgumentParser(description = 'Get the essential arguments for the program')
    parser.add_argument('--AudioFile', type = str, default = 'audio.wav', help = 'The audio file to be processed')
    parser.add_argument('--AudioRate', type = int, default = 16000, help = 'The audio rate of the audio file')
    parser.add_argument('--showflag', type = bool, default = False, help = 'Show the informations or not')
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()