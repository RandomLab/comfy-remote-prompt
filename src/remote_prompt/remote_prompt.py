import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import json
import uuid
import requests
import urllib.parse

from base64 import b64encode

def basic_auth_header(username, password):
    assert ':' not in username
    user_pass = f'{username}:{password}'
    basic_credentials = b64encode(user_pass.encode()).decode()
    return basic_credentials

class RemotePrompt:

    def __init__(self, url, workflow_data, username, password):
        self.url = "http://" + url
        # self.json_path = json_path
        self.username = username
        self.password = password
        self.prompt_url = self.url + "/prompt"

        self.client_id = str(uuid.uuid4())

        self.ws = websocket.WebSocket()
        self.ws.connect(f"ws://{url}/ws?clientId={self.client_id}", 
                   header={"Authorization": "Basic " + basic_auth_header(self.username, self.password)})
        

        # self.prompt = json.loads(workflow_data)
        self.prompt = workflow_data

    def queue_prompt(self):
        p = {"prompt": self.prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        try:
            # POST to prompt url
            request = requests.post(self.prompt_url, data = data, auth=(self.username, self.password))
        except Exception as e:
            print("[ERROR QUEUE PROMPT]", e)
        print("QUEUE_PROMPT :", request.json())
        return request.json()
        
    def get_image(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        url = f"{self.url}/view?{url_values}"
        print(f"GET IMAGE request : {url}")
        try:
            # Open the URL
            request = requests.get(url, auth=(self.username, self.password), stream=True)
        except Exception as e:
            print("[ERROR:GET IMAGE]", e)
        # print("GET_IMAGE : ", request.text)   
        # return request.raw.read()
        print(f"[INFO: GET IMAGE] {request.headers}")
        # request.raw.decode_content = True
        return (filename, request.content)

    def get_history(self, prompt_id):
        url = f"{self.url}/history/{prompt_id}"
        print(f"HISTORY request : {url}")
        try:
            # Open the URL
            request = requests.get(url, auth=(self.username, self.password))
        except Exception as e:
            print("[ERROR HISTORY]", e)
        print("HISTORY response : ", request.json())   
        return request.json()



    def get_images(self):
        prompt_id = self.queue_prompt()["prompt_id"]
        output_images = {}
        while True:
            out = self.ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break #Execution is done
            else:
                continue #previews are binary data

        history = self.get_history(prompt_id)[prompt_id]
        for o in history['outputs']:
            for node_id in history['outputs']:
                node_output = history['outputs'][node_id]
                if 'images' in node_output:
                    images_output = []
                    for image in node_output['images']:
                        image_data = self.get_image(image['filename'], image['subfolder'], image['type']) # self.get_image(image)
                        images_output.append(image_data)
                output_images[node_id] = images_output

        return output_images

    def upload_file(self, file, subfolder="", overwrite=False):
        # Wrap file in formdata so it includes filename
        body = {"image": open(file, "rb")}
        data = {}

        if overwrite:
            data["overwrite"] = "true"

        if subfolder:
            data["subfolder"] = subfolder

        url = f"{self.url}/upload/image"
        print(f"UPLOAD request : {url}")
        try:
            # Open the URL
            request = requests.post(url, auth=(self.username, self.password), files=body, data=data)
        except Exception as e:
            print("[ERROR UPLOAD]", e)
        print("UPLOAD response : ", request.json())   
        data = request.json()
        # Add the file to the dropdown list and update the widget value
        path = data["name"]
        if "subfolder" in data:
            if data["subfolder"] != "":
                path = data["subfolder"] + "/" + path

        return path


