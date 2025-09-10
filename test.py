import hashlib
import json
# import requests

traits = ["Craftsman", "Pragmatic", "Curious", "Methodical", "Driven", "Collaborator"]
key = "Close-11161e20"

hashes = []
for trait in traits:
    data = (trait + key).encode("utf-8")
    h = hashlib.blake2b(data, digest_size=64).hexdigest()
    hashes.append(h)

# Print the JSON array
print(json.dumps(hashes, indent=2))

# POST back to the endpoint
# response = requests.post("https://api.close.com/buildwithus/", json=hashes)
# print(response.status_code, response.text)
#adding additional comment
