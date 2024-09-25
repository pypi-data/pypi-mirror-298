# FAIsdk/FAImageGen/harmonizer.py
import base64
from io import BytesIO
from PIL import Image
from .api_client import APIClient

class Fuzer:
    def __init__(self, client: APIClient):
        self.client = client

    def image_to_base64(self, image_path):
        with Image.open(image_path) as img:
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def fuzer(self, image_path, prompt, refprompt, mode, intensity, width, height, isbgremove, resize, preprocess, preprocess_val, postprocess, postprocess_val, timeout=120):
        image_base64 = self.image_to_base64(image_path)
        data = {
            "foreground_image64": image_base64,
            "prompt": prompt,
            "refprompt": refprompt,
            "mode": mode,
            "intensity": intensity,
            "width": width,
            "height": height,
            "rmbg": isbgremove,
            "resize": resize,
            "preprocess": preprocess,
            "preprocess_val": preprocess_val,
            "postprocess": postprocess,
            "postprocess_val": postprocess_val
        }
    
        # Make the API call
        response = self.client.post('Image-gen', json_data=data, timeout=timeout)

        # Print response keys for debugging
        print("Response Keys:", response.keys())

        # Save the image and mask image if they exist in the response
        if 'image' in response:
            image_data = response['image']
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
            image.save("output_image.png")
            print("Image retrieved and saved as output_image.png.")
        else:
            print("Response does not contain 'image'")

        return response

