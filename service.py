import os
import uuid
from faster_whisper import WhisperModel, utils
from model_config import model_size, device, compute_type
from datetime import timedelta
from repository import save

model = WhisperModel(model_size,device=device,compute_type=compute_type,)

def transcribe(file_path,file_name):

    segments,info = model.transcribe(file_path, beam_size=5,word_timestamps=True)
    result = convert(segments,file_name)
    return result

def convert(segments,file_name):

    srt_dir = os.path.join(os.getcwd(),'srt_files')
    os.makedirs(srt_dir, exist_ok=True)
    file_uuid = str(uuid.uuid4())
    srtFileName = file_name.replace(".mp3",'_' + file_uuid + '.srt')
    srtFilePath = os.path.join(srt_dir, srtFileName)
    finalText = []

    for segment in segments:
        
        finalText.append(segment.text)
        startTime = str(0)+str(timedelta(seconds=int(segment.start)))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment.end)))+',000'
        text = segment.text
        segmentId = segment.id
        line = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
        segmentId = segment.id+1

        with open(srtFilePath, 'a', encoding='utf-8') as srtFile:
            srtFile.write(line)

    save(file_uuid,srtFilePath)

    return {
            "uuid": file_uuid,
            "text":''.join(finalText)
           }



