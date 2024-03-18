from faster_whisper import WhisperModel

from model_config import model_size, device, compute_type

model = WhisperModel(model_size,device=device,compute_type=compute_type,)

def transcribe(file_path):
    
    segments, info = model.transcribe(file_path, beam_size=5,word_timestamps=True)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    text = []

    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

        text.append(segment.text + "\n")
    
    
    
    return ''.join(text)




