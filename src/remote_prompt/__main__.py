import os
import sys
from remote_prompt import __version__
from remote_prompt.remote_prompt import RemotePrompt
import configparser
import json

def update_workflow(config, workflow):
    print(config["inputs"]["prompt"], workflow)
    workflow["4"]["inputs"]["ckpt_name"] = config["inputs"]["ckpt_name"]
    workflow["5"]["inputs"]["batch_size"] = config["inputs"]["batch_size"]
    workflow["6"]["inputs"]["text"] =       config["inputs"]["prompt"]
    workflow["7"]["inputs"]["text"] =       config["inputs"]["neg_prompt"]
    return workflow

def usage():
    print(f"Usage :")
    print(f"remote-prompt workflow_api.json")
    print()
    print("You have to create a file named secret.ini and put url, username and password :")
    print("username:password:ia.yourdomain.fr:port")
    print()
    print("You can import RemotePrompt in your python script to use the class directly :")
    print()
    print("from remote_prompt.remote_prompt import RemotePrompt")
    print("url = 'YOUR COMFYUI URL WITHOUT http://'")
    print("username = 'YOUR USER NAME'")
    print("password = 'YOUR PASSWORD'")
    print("json_path = 'workflow_api.json'")
    print("remote = RemotePrompt(url, json_path, username, password)")
    print("images = remote.get_images()")
    print("for node_id in images:")
    print("    for filename, image_data in images[node_id]:")
    print("        with open(filename, 'wb') as f:")
    print("            f.write(image_data)")

def main():
    print(f"Remote prompt version {__version__}")
    print()

    args = sys.argv[1:]
    config_file = None

    if len(args) == 0:
        usage()
        exit(1)

    if len(args) == 1:
        print(f"Using {args[0]} as workflow.")
        json_path = args[0]
    elif len(args) == 2:
        print(f"Using {args[0]} as workflow and {args[1]} as config file.")
        json_path = args[0]
        config_file = args[1]

    print("Trying to load secrets from secrets.ini")
    if os.path.isfile("secrets.ini"):
        with open("secrets.ini", "r") as f:
            secrets = f.read().strip()
    else:
        print("No secrets.ini file found")
        usage()
        exit(1)
    secrets = secrets.split(':')
    if len(secrets) != 4:
        print("Malformed secrets.ini file")
        usage()
        exit(1)

    username = secrets[0]
    password = secrets[1]
    url = secrets[2] + ":" + secrets[3]
    json_path = args[0]
    # Open the workflow json file
    with open(json_path, "r", encoding="utf-8") as f:
        # workflow_data = f.read()
        workflow_data = json.load(f)

    print(f"Using http://{url} as backend with {json_path}")
    print()
    print("Trying to load params from config.ini")
    if config_file is not None and os.path.isfile(config_file):
        print("Reading config file and update workflow.")
        config = configparser.ConfigParser(allow_no_value=True, interpolation=configparser.ExtendedInterpolation())
        config.read(config_file)
        workflow_data = update_workflow(config, workflow_data)
    else:
        print("No config.ini file found")
        print("Using unmodified workflow")

    print()
    remote = RemotePrompt(url, workflow_data, username, password)

    images = remote.get_images()

    for node_id in images:
        for filename, image_data in images[node_id]:
            with open(filename, "wb") as f:
                f.write(image_data)


if __name__ == '__main__':
    main()

