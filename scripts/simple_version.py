import librosa
import torch
import os, sys
# add current directory to the path
install_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(install_path)

from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
from utils.arg import get_args
from utils.tools import get_objects, get_motion

# define the platform
car_names = ['ADAM', 'MARY', 'JAM']
car_postion = [(0, 0), (-2, 1), (3, 0)]
platform_size = (5, 5)
platform = dict(zip(car_names, car_postion))
relations = ['LEFT', 'RIGHT', 'UP', 'DOWN']
# input()



if __name__ == "__main__":
    # get the arguments
    args = get_args()
    audio_file = args.AudioFile
    audio_rate = args.AudioRate
    show_flag = args.showflag

    # print the arguments
    print("show flag: ", show_flag)
    if show_flag:
        print("Audio file: ", audio_file)
        print("Audio rate: ", audio_rate)
        print("Platform: ", platform)
        print("Platform size: ", platform_size)

    audio, rate = librosa.load(audio_file, sr = audio_rate)

    # define the tokenizer and model
    tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

    # tokenize the audio
    input_values = tokenizer(audio, return_tensors = "pt").input_values
    logits = model(input_values).logits

    # get the predicted ids
    prediction = torch.argmax(logits, dim = -1)

    # decode the audio
    transcription = tokenizer.batch_decode(prediction)[0]

    if show_flag:
        print(transcription)

    # get the objects and relations

    TRG, REF = get_objects(transcription)
    REL = get_motion(transcription)

    if show_flag:
        print("Target: ", TRG)
        print("Reference: ", REF)
        print("Relation: ", REL)

    # get the position of the target and reference
    TRG_pos = platform[TRG]
    REF_pos = platform[REF]

    # get the position of the target after the motion
    if REL == 'LEFT':
        TRG_pos = (REF_pos[0] - 1, REF_pos[1])
    elif REL == 'RIGHT':
        TRG_pos = (REF_pos[0] + 1, REF_pos[1])
    elif REL == 'UP':
        TRG_pos = (REF_pos[0], REF_pos[1] + 1)
    elif REL == 'DOWN':
        TRG_pos = (REF_pos[0], REF_pos[1] - 1)

    # print the result
    print("The position of the target is: ", TRG_pos)