import requests
from datetime import datetime



def apiGet(ipadress, key, endpoint):
    url = f"http://{ipadress}{endpoint}"
    headers = {
        "X-Api-Key": key,
    }
    snap_response = requests.get(url, headers=headers)
    snap_response.raise_for_status()
    return snap_response

def getSnap(ipadress, key):
    response = apiGet(ipadress, key, "/api/v1/cameras/snap")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    content_type = response.headers.get("Content-Type")
    
    # Determine the file extension based on the Content-Type
    if content_type == "image/jpeg":
        extension = ".jpg"
    elif content_type == "image/png":
        extension = ".png"
    else:
        print (f"Unkown content type: {content_type}")

    if (len(extension) > 0):
        filename = f"{timestamp}{extension}"
        # Save the image to a file
        with open(filename, "wb") as file:
            file.write(response.content)

if __name__ == "__main__":
    import json
    with open("secrets.json", "r") as file:
        settings = json.load(file)
        getSnap(settings["ipadress"], settings["key"])
