# Remote prompt

## Installation

Download this repo as a zip file, unzip, create a virtual env using python (optional) and run __pip install .__ in the root of the uncompressed folder.

Usage :

```text
Usage :
remote-prompt workflow_api.json

You have to create a file named secret.ini and put url, username and password :
username:password:ia.yourdomain.fr:port
```

You can import RemotePrompt in your python script to use the class directly :

```python
from remote_prompt.remote_prompt import RemotePrompt
url = 'YOUR COMFYUI URL WITHOUT http://'
username = 'YOUR USER NAME'
password = 'YOUR PASSWORD'
json_path = 'workflow_api.json'

with open(json_path, "r", encoding="utf-8") as f:
    workflow_data = json.load(f)

remote = RemotePrompt(url, workflow_data, username, password)
images = remote.get_images()
for node_id in images:
    for filename, image_data in images[node_id]:
        with open(filename, 'wb') as f:
            f.write(image_data)

# Upload an image
with open("example.png", "rb") as f:
    comfyui_path_image = remote.upload_file(f, "", True)


```
