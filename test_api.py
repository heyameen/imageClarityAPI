import requests


api_url = 'http://localhost:5000/enhance'

image_path = 'image/4yearoldgirl.0.jpg'

with open(image_path, 'rb') as file:
    files = {'image': file}

    response = requests.post(api_url, files=files)


if response.status_code == 200:
    with open('enhanced_image.jpg', 'wb') as file:
        file.write(response.content)
    print('Enhanced image saved as enhanced_image.jpg')
else:
    print('Error:', response.status_code)
