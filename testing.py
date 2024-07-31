import requests


r = requests.get(
    "http://localhost:7860/exec",
    params={
        "command": "wget https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_30mb.mp4"
    },
    stream=True,
)
for line in r.iter_lines():
    print(line)
