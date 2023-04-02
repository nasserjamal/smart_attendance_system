from flask import Flask, request, Response
import base64
import os

app = Flask(__name__)


@app.route('/init', methods=['POST'])
def camInit():
    return Response(status=200)


@app.route('/upload', methods=['POST'])
def receive_image():
    print("Now processing the request")
    # Get the image data from the request
    image_data = request.data

    # Convert the image data to a base64 string
    base64_image = base64.b64encode(image_data).decode('utf-8')

    # Save the image to disk
    if not os.path.exists('images'):
        os.makedirs('images')
    image_num = len(os.listdir('images')) + 1
    with open(f'images/image{image_num}.jpg', 'wb') as f:
        f.write(base64.b64decode(base64_image))

    print("Done processing")

    # Return a response
    return Response(status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
