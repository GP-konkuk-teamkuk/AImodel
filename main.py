
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import pickle
import subprocess
import os

app = FastAPI()

# Define the port variable
PORT = 8000
MYENV = "myenv"

@app.post("/process/")
async def process(sentence: str = Form(...), file: UploadFile = File(...), idx: int = Form(...)):
    embeddings_dir = os.path.join(os.path.dirname(__file__),'sv2tts_korean', 'embeddings')
    print(embeddings_dir)
    os.makedirs(embeddings_dir, exist_ok=True)
    file_path = os.path.join(embeddings_dir, file.filename)
    with open(file_path, 'wb') as f:
        f.write(await file.read())

    hash_and_time = f"{os.path.splitext(file.filename)[0]}_{idx}"
    
    print("hell")
    current_dir = os.path.dirname(__file__)
    command = f"conda run -n {MYENV} python {os.path.join(current_dir, 'sv2tts_korean', 'synthesize_voice.py')} --text '{sentence}' --hash_and_time {hash_and_time}"
    subprocess.run(command, shell=True)

    wav_file_path = os.path.join(current_dir, 'sv2tts_korean', 'synthesized_samples', f"{hash_and_time}.wav")

    return FileResponse(wav_file_path, media_type='audio/wav', filename='output.wav')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
