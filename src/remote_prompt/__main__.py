import os
import sys
from remote_prompt import __version__
from remote_prompt.remote_prompt import RemotePrompt

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

    if len(args) == 0:
        usage()
        exit(1)

    if len(args) == 1:
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

        print(f"Using http://{url} as backend with {json_path}")

        remote = RemotePrompt(url, json_path, username, password)

        images = remote.get_images()

        for node_id in images:
            for filename, image_data in images[node_id]:
                with open(filename, "wb") as f:
                    f.write(image_data)


if __name__ == '__main__':
    main()

