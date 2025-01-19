import requests
from datetime import datetime
from dotenv import load_dotenv



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
    import os
    from dotenv import load_dotenv
    load_dotenv()

    IP_ADDRESS = os.getenv("PRUSALINK_IP")
    API_KEY = os.getenv("PRUSALINK_API_KEY")

    getSnap(IP_ADDRESS, API_KEY)
