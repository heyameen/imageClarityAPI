from flask import Flask, request, send_file
from PIL import Image
import numpy as np
from io import BytesIO
from RealESRGAN import RealESRGAN
import torch

app = Flask(__name__)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model_scale = 4
model = RealESRGAN(device, scale=model_scale)
model.load_weights(f'weights/RealESRGAN_x{model_scale}.pth')


@app.route('/enhance', methods=['POST'])
def enhance_image():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    image_file = request.files['image']
    image = Image.open(BytesIO(image_file.read())).convert('RGB')

    enhanced_image = model.predict(np.array(image))

    # Convert the enhanced image to bytes
    img_bytes = BytesIO()
    enhanced_image.save(img_bytes, format='PNG' if image_file.filename.lower().endswith('.png') else 'JPEG')
    img_bytes.seek(0)

    # Return the enhanced image as a file
    return send_file(img_bytes, mimetype='image/png' if image_file.filename.lower().endswith('.png') else 'image/jpeg')


if __name__ == '__main__':
    app.run()
