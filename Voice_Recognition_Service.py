from flask import Flask, request, jsonify
import psycopg2
from prometheus_flask_exporter import PrometheusMetrics
import werkzeug
import speech_recognition as sr
import os

app = Flask(__name__)

metrics = PrometheusMetrics(app)

metrics.info('app_info_voice_recognition', 'Application info', version='1.0.0')

@app.route('/', methods=['POST'])
def recognize_voice():
    
    videofile = request.files['video']
    filename = werkzeug.utils.secure_filename(videofile.filename)
    videofile.save(os.path.join("/usr/src/app/", filename))
    os.system('ffmpeg -i ' + os.path.join("/usr/src/app/", filename) + ' /usr/src/app/translate.wav')

    r = sr.Recognizer()

    translated = True

    with sr.AudioFile('/usr/src/app/translate.wav') as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language = 'en-US', show_all = True)
            response = str(text['alternative'][0]['transcript'])
        
        except:
            translated = False
    
    if not translated:
        status = "Failed"
        message = "Error while recognizing the voice."

    else:
        status = "Success"
        message = response

    os.remove('/usr/src/app/translate.wav')

    return jsonify({"status" : status, "message" : message})

if __name__ == "__main__":
    app.run(host="0.0.0.0")