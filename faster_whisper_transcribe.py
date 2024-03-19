from faster_whisper import WhisperModel, utils

from model_config import model_size, device, compute_type

from utils import convert

model = WhisperModel(model_size,device=device,compute_type=compute_type,)

def transcribe(file_path,file_name):

    segments,info = model.transcribe(file_path, beam_size=5,word_timestamps=True)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    uuid,text = convert(segments,file_name)
    
    # for segment in segments:
    #     print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    #     result.append(segment.text)

    return uuid, text



