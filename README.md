# Remote prompt

## Installation

Download this repo as a zip file, unzip, create a virtual env using python (optional) and run __pip install .__ in the root of the uncompressed folder.

Usage :

```python
Usage :
remote-prompt workflow_api.json

You have to create a file named secret.ini and put url, username and password :
username:password:ia.yourdomain.fr:port

You can import RemotePrompt in your python script to use the class directly :

from remote_prompt.remote_prompt import RemotePrompt
url = 'YOUR COMFYUI URL WITHOUT http://'
username = 'YOUR USER NAME'
password = 'YOUR PASSWORD'
json_path = 'workflow_api.json'
remote = RemotePrompt(url, json_path, username, password)
images = remote.get_images()
for node_id in images:
    for filename, image_data in images[node_id]:
        with open(filename, 'wb') as f:
            f.write(image_data)

```
