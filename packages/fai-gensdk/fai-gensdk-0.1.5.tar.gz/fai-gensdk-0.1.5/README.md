# Fotographer.ai sdk modules

## Installation

Install the SDK using pip:

```bash
pip install fai-gensdk
```

## Usage of InstantLight

Here’s an example of how to use the InstantLight SDK to make an API call and handle the response:

```bash
from InstantLight import InstantLightSDK
from PIL import Image
import base64
from io import BytesIO

# Initialize the SDK
sdk = InstantLightSDK(
    base_url='https://api.fotographer.ai/instantLight',
    api_key='your_api_key',
    email='your_email@example.com'
)

# Convert images to base64
def image_to_base64(image_path):
    with Image.open(image_path) as img:
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Prepare the image data
foreground_image64 = image_to_base64('path_to_foreground_image.png')
background_image64 = image_to_base64('path_to_background_image.png')

# Example mode 0: Edit Light With a Prompt
# Mode 0 is used to edit the light in an image using a prompt.
image_data_mode_0 = {
    "foreground_image64": foreground_image64,
    "background_image64": background_image64,
    "prompt": "",
    "mode": 0,
    "prompt_strength": 3.0,
    "inf_factor": 1.00,
    "mask_strength": 0.5,
    "image_width": 1400,
    "image_height": 1400,
    "additional_prompt": "",
    "negative_prompt": "",
    "lights": []  # leave as blank here for 
}

# Example mode 1: Edit Light With a Prompt
# Mode 1 is used to edit the light in an image using a prompt.
image_data_mode_1 = {
    "foreground_image64": foreground_image64,
    "background_image64": background_image64,
    "prompt": "neon light",
    "mode": 0,
    "prompt_strength": 3.0,
    "inf_factor": 1.00,
    "mask_strength": 0.5,
    "image_width": 1400,
    "image_height": 1400,
    "additional_prompt": "",
    "negative_prompt": "",
    "lights": []  # Specify the lighting parameters as needed 
    #for example:
    #"lights": [{"light_position": [0.5, 0.5],"light_intensity": 0.8,"light_z": 0.3,"color": [255, 200, 150],"presets": "Light1"},{"light_position": [0.2, 0.8],"light_intensity": 0.5,"light_z": 0.1,"color": [100, 100,255],"presets": "Light2"}]
}

# Example mode 2: Edit Light and Change Background
# Mode 2 is used to edit the light and change the background of an image.
image_data_mode_2 = {
    "foreground_image64": foreground_image64,
    "background_image64": background_image64,
    "prompt": "sunset background",
    "mode": 2,
    "prompt_strength": 3.0,
    "inf_factor": 1.00,
    "mask_strength": 0.5,
    "image_width": 1400,
    "image_height": 1400,
    "additional_prompt": "",
    "negative_prompt": "",
    "lights": []  # Specify the lighting parameters as needed
    #for example:
    #"lights": [{"light_position": [0.5, 0.5],"light_intensity": 0.8,"light_z": 0.3,"color": [255, 200, 150],"presets": "Light1"},{"light_position": [0.2, 0.8],"light_intensity": 0.5,"light_z": 0.1,"color": [100, 100,255],"presets": "Light2"}]
}

# Select the desired mode for the example
image_data = image_data_mode_2

# Make the API call
response = sdk.image_generation.get_image_gen(image_data)

# Print the response keys for debugging
print("Response Keys:", response.keys())

# Print the keys at all levels of the response for debugging
for key, value in response.items():
    if isinstance(value, dict):
        print(f"Response[{key}] Keys: {value.keys()}")

# Save the image and mask image if they exist in the response
if 'image' in response:
    image_data = response['image']
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))
    image.save("output_image.png")
    print("Image retrieved and saved as output_image.png.")
    
    if 'mask_image' in response:
        mask_data = response['mask_image']
        mask_bytes = base64.b64decode(mask_data)
        mask_image = Image.open(BytesIO(mask_bytes))
        mask_image.save("output_mask_image.png")
        print("Mask retrieved and saved as output_mask_image.png.")
else:
    print("Response does not contain 'image'")
```

Make sure to update `your_api_key` and `your_email@example.com` with the actual values in the example usage section.

## Usage of ImageGen

```bash
from FAImageGen import ImageGen as FAImageGenSDK
from PIL import Image
import base64
from io import BytesIO

# Initialize the SDK API
api = FAImageGenSDK(
    base_url='https://api.fotographer.ai/Image-gen',
    api_key='your_api_key',
    email='your_email@example.com'
)

# Convert images to base64
def image_to_base64(image_path):
    with Image.open(image_path) as img:
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')



# Prepare the image data
image_path = 'path_to_your_image.png'
prompt = 'a black perfume bottle on top of mounntain in front of the sea'

# Make the API call
response = api.image_generation.get_image_gen(image_path, prompt)

try:
    # Make the API call
    response = api.image_generation.get_image_gen(image_path, prompt)

    # Print the response keys for debugging
    #logging.debug("Response Keys: %s", response.keys())

    # Print the keys at all levels of the response for debugging
    for key, value in response.items():
        if isinstance(value, dict):
            logging.debug(f"Response[{key}] Keys: %s", value.keys())

    # Save the image and mask image if they exist in the response
    if 'image' in response:
        logging.debug("Success")
    else:
        logging.debug("Response does not contain 'image'")

except requests.exceptions.RequestException as e:
    logging.error(f"HTTP error occurred: {e}")
    if hasattr(e, 'response') and e.response is not None:
        logging.error(f"Response content: {e.response.content}")
except Exception as e:
    logging.error("An unexpected error occurred: %s", e)
```

## Usage of Background Removal

```bash
from FAImageGen import ImageGen
from PIL import Image
import base64
from io import BytesIO

# Initialize the SDK API
api = ImageGen(
    base_url='https://api.fotographer.ai/Image-gen',
    api_key='your_api_key',
    email='your_email@example.com'
)

# Image path for the background removal
image_path = 'path_to_your_image.png'

# Remove the background
bg_removed_image = api.image_generation.remove_background(image_path)

# Save the background-removed image if it exists in the response
if 'image' in bg_removed_image:
    image_data = bg_removed_image['image']
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))
    image.save("background_removed_image.png")
    print("Background removed image retrieved and saved as background_removed_image.png.")
else:
    print("Response does not contain 'image'")

```

## Usage of Harmonizer

```bash
from FAImageGen import ImageGen
from PIL import Image
import base64
from io import BytesIO

# Initialize the Harmonizer
image_gen = ImageGen(
    base_url='https://api.fotographer.ai/Image-gen',
    api_key='your_api_key',
    email='your_email@example.com'
)

# Convert images to base64
def image_to_base64(image_path):
    with Image.open(image_path) as img:
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Prepare the image data
image_path = 'path_to_your_image.png'

# Harmonize the image
harmonized_image = image_gen.harmonizer.harmonize_image(image_path)

# Print the response keys for debugging
print("Response Keys:", response.keys())

# Print the keys at all levels of the response for debugging
for key, value in response.items():
    if isinstance(value, dict):
        print(f"Response[{key}] Keys: {value.keys()}")

# Save the harmonized image if it exists in the response
if 'image' in response:
    image_data = response['image']
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))
    image.save("harmonized_output_image.png")
    print("Harmonized image retrieved and saved as harmonized_output_image.png.")
else:
    print("Response does not contain 'image'")

```

## Usage of Fuzer

```bash
from FAImageGen import ImageGen
from PIL import Image
import base64
from io import BytesIO

# Initialize the Harmonizer
image_gen = ImageGen(
    base_url='https://api.fotographer.ai/Image-gen',
    api_key='your_api_key',
    email='your_email@example.com'
)

# Convert images to base64
def image_to_base64(image_path):
    with Image.open(image_path) as img:
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Prepare the image data
image_path = 'path_to_your_image.png'
prompt = 'a black perfume bottle on top of a mountain in front of the sea'
refprompt = '(( transparent clear water bottle )) vibrant, studio light, spotlight, nature green label'
mode = 'full'  # or 'first-stage' or 'refiner'
intensity = 3.50  # 1 to 11
width = 1000
height = 1000
isbgremove = True  # if True, the background will be removed
resize = True  # if True, the image will be resized
preprocess = True  # if True, preprocessing will be applied
preprocess_val = 0.50  # a value for preprocessing
postprocess = False  # if False, postprocessing will be skipped
postprocess_val = 25  # a value for postprocessing

# Fuse the image
fuzed_image = image_gen.fuzer.fuzer(
    image_path, prompt, refprompt, mode, intensity, width, height, isbgremove,
    resize=resize, preprocess=preprocess, preprocess_val=preprocess_val,
    postprocess=postprocess, postprocess_val=postprocess_val
)

# Save the fuzed image if it exists in the response
if fuzed_image:
    print("Fuzed image processing successful.")
else:
    print("Fuzing failed or image not found in the response.")


```