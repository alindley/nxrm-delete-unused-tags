import requests
import time

nxrm_dns = "localhost:8081"
username = "admin"
password = "admin123"
tags_url = "http://" + nxrm_dns + "/service/rest/v1/tags"
search_assets_url = "http://" + nxrm_dns + "/service/rest/v1/search/assets"
delete_tag_url = "http://" + nxrm_dns + "/service/rest/v1/tags/{tag}"

# Retrieve all tags
tags = []
continuation_token = None

while True:
    params = {}
    if continuation_token:
        params["continuationToken"] = continuation_token

    response = requests.get(tags_url, auth=(username, password), params=params)
    if response.status_code == 200:
        tags_data = response.json()
        for tag in tags_data["items"]:
            tags.append(tag["name"])
        continuation_token = tags_data.get("continuationToken")
        if continuation_token is None:
            break
    else:
        print("Error retrieving tags:", response.status_code)
        exit()


# Check if each tag has any associated assets and delete if not
for tag in tags:
    # Search for assets with the tag
    params = {"tag": tag}
    response = requests.get(search_assets_url, params=params, auth=(username, password))
    if response.status_code == 200:
        search_results = response.json()
        assets = search_results["items"]
        if not assets:
            # Delete the tag
            delete_url = delete_tag_url.format(tag=tag)
            response = requests.delete(delete_url, auth=(username, password))
            if response.status_code == 204:
                print("Tag deleted:", tag)
            else:
                print("Error deleting tag:", tag, response.status_code)
        else:
            print("Tag has associated assets:", tag)
    else:
        print("Error searching assets for tag:", tag, response.status_code)
    time.sleep(1)  # 1-second delay between search requests
