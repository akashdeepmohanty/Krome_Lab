from flask import Flask, request, jsonify, send_file, after_this_request
from flask_cors import CORS
import json
import os
import uuid
import librosa
import soundfile as sf
import time

app = Flask(__name__)
CORS(app)


UPLOAD_FOLDER = "files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

current_file = None
current_tempo = 20
current_Orignal_tempo = 1
current_pitch = 0


@app.route("/upload", methods=["POST"])
def upload():
    global current_file
    try:

        if "music" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["music"]

        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        filename = f"input_{int(time.time())}.mp3"
        path = os.path.join(UPLOAD_FOLDER, "input.mp3")

        file.save(path)

        current_file = path

        return jsonify({
            "message": "File uploaded successfully",
            "filename": filename
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/process", methods=["POST"])
def process_audio():
    global current_file, current_tempo, current_pitch, current_Orignal_tempo
    try:

        if current_file is None:
            return jsonify({"error": "No uploaded file"}), 400

        data = request.json
       
        current_tempo = float(data["tempo"]) 
        current_Orignal_tempo = float(data["tempoOrignal"]) 
        current_pitch = int(data["pitch"])

        return jsonify({"message": "Audio processed successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Downlode
@app.route("/download", methods=["GET"])
def download():
    global current_file, current_tempo, current_pitch, current_Orignal_tempo

    try:
        if current_file is None or not os.path.exists(current_file):
            return jsonify({"error": "File not found"}), 404

        # 🎧 Process same as play
        y, sr = librosa.load(current_file, sr=None)

        if current_Orignal_tempo is None or current_Orignal_tempo == 0:
            return jsonify({"error": "Original BPM not set"}), 400
        
        tempo_factor = current_tempo / current_Orignal_tempo

        y = librosa.effects.pitch_shift(y, sr=sr, n_steps=current_pitch)
        y = librosa.effects.time_stretch(y, rate=tempo_factor)
        

        output_path = os.path.join(UPLOAD_FOLDER, "processed.wav")
        sf.write(output_path, y, sr)

        return send_file(
            output_path,
            as_attachment=True,
            download_name="processed.wav"
        )

    except Exception as e:
        print("Download error:", e)
        return jsonify({"error": str(e)}), 500
    

@app.route("/play", methods=["GET"])
def play_audio():
    global current_file, current_tempo, current_pitch, current_Orignal_tempo

    try:
        if current_file is None or not os.path.exists(current_file):
            return jsonify({"error": "No file"}), 404


        y, sr = librosa.load(current_file, sr=None)

        if current_Orignal_tempo is None or current_Orignal_tempo == 0:
            return jsonify({"error": "Original BPM not set"}), 400
        
        tempo_factor = current_tempo / current_Orignal_tempo

        y = librosa.effects.pitch_shift(y, sr=sr, n_steps=current_pitch)
        y = librosa.effects.time_stretch(y, rate=tempo_factor)
        

        output_path = os.path.join(UPLOAD_FOLDER, "processed.wav")
        sf.write(output_path, y, sr)

        return send_file(output_path, mimetype="audio/wav")

    except Exception as e:
        print("Play error:", e)
        return jsonify({"error": str(e)}), 500
    
@app.route("/home")
def home():
    return "Hello, Flask!"


if __name__ == "__main__":
    app.run(debug=True)