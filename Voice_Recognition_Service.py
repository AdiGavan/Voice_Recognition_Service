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
        #response = json.dumps(text, ensure_ascii=False).encode('utf8')
            print(text['alternative'][0]['transcript'])
        
        except Exception as e:
            translated = False
            print('ERRRORRRRR ' + str(e))
    
    if not translated:
        status = "Failed"
        error = "Error at adding the line in the database."

    else:
        status = "Success"
        error = response

    return jsonify({"status" : status, "error" : error})

if __name__ == "__main__":
    app.run(host="0.0.0.0")