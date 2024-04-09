from flask import Flask, request, render_template
import cv2
import os
import random
from gradio_client import Client


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['video_input']
        if file:
            # Сохраняем файл во временную директорию
            file_path = os.path.join('temp', file.filename)
            file.save(file_path)
            
            cap = cv2.VideoCapture(file_path)
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            random_frame = random.randint(0, total_frames - 1)
            cap.set(cv2.CAP_PROP_POS_FRAMES, random_frame)
            
            ret, frame = cap.read()
            if ret:
                cv2.imwrite("temp/frame.jpg", frame)
            
            cap.release()
            
            
            client = Client("https://tonyassi-image-story-teller.hf.space/--replicas/liw84/")
            result = client.predict('temp/frame.jpg', api_name="/predict")
            
            os.remove(file_path)

            return render_template('index.html', result=result)
    return render_template('index.html', result="Paste a video first...", img_place="../temp/frame.jpg")

if __name__ == '__main__':
    app.run(debug=True)