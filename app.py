from flask import Flask, render_template,request
import cv2
import numpy as np
import os
import shutil

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('Get_Image.html')


@app.route('/show_image',methods=['GET','POST'])
def detect_objects():
    # Saving the input image
    if request.method == "POST":
        image = request.files["img"].read()

        #convert string data to numpy array
        file_bytes = np.fromstring(image, np.uint8)
        
        # convert numpy array to image
        img = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)
        
        # Saving the image file
        if not (os.path.isdir('input_image')):
            os.mkdir('input_image')

        input_path = os.path.join('input_image','Saved.jpg')
        cv2.imwrite(input_path,img)
        print('file saved')

    # Detecting objects
    script_path = os.path.join('yolov5','detect.py')
    weights_path = os.path.join('yolov5', 'best.pt')
    IP_img_path = os.path.join('input_image','Saved.jpg')
    OP_image_folder = os.path.join('output_image')
    
    path_ls = ['Python', script_path, '--weights', weights_path, '--img 416 --conf 0.4', '--source', IP_img_path, '--project', OP_image_folder]

    run_command = ' '.join(path_ls) 
    os.system(run_command)

    # Move Output image to Static folder
    OP_image_path = os.path.join(OP_image_folder, 'exp', 'Saved.jpg')
    Static_folder_img_path = os.path.join('static','Saved.jpg')
    shutil.move(OP_image_path, Static_folder_img_path)
    os.rmdir(os.path.join(OP_image_folder, 'exp'))

    # Show detected object on webpage
    return render_template('Show_Image.html',img_path = OP_image_path)

if __name__ == '__main__':
    app.run(debug=True)
