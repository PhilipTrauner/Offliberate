# Offliberate

<img align="right" src="https://cloud.githubusercontent.com/assets/9287847/22620779/6918a678-eb13-11e6-9f98-95eb90db133e.png">

![Python version support: 3](https://img.shields.io/badge/python-3-green.svg)
![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)

**Offliberate** allows you to harness the power of [Offliberty](http://offliberty.com/) right from your terminal.  

> If the Internet bus visits your village only once a week or your grandma doesn't let you use Internet   
more than 1 hour a day - Offliberty is for you.

[Offliberty](http://offliberty.com/) can scrape media from sites such as [YouTube](https://www.youtube.com), [SoundCloud](https://soundcloud.com) and [bandcamp](https://bandcamp.com/).

### Installation
```bash
pip3 install offliberate
```

### Usage
<p align="center">
	<img src="https://cloud.githubusercontent.com/assets/9287847/22621335/887e73e0-eb21-11e6-81a4-cc92f6a464eb.gif">
	Piping into <strong>Offliberate</strong>
</p>

|Parameter|Short|Description|      |
|---------|-----|-----------|------|
|--audio|-a|Download audio|🎵|
|--video|-v|Download video|🎬|
|--pretty|-p|Make **Offliberate** bland and boring|💤|
|--download-location||Where should stuff go?|⬇|
|--no-download||Only resolve download links |🔗|

#### Examples  
Download a very special song (already escaped for your convenience):  
```
offliberate https://www.youtube.com/watch\?v\=dQw4w9WgXcQ
```
Download the video of said song:  
```
offliberate -v https://www.youtube.com/watch\?v\=dQw4w9WgXcQ
```
Download the audio and video of this absolute masterpiece:  
```
offliberate -v -a https://www.youtube.com/watch\?v\=dQw4w9WgXcQ
```

### Tidbits
**Offliberate** can also be used as a library.  

`request(url, callback=None, audio=True, video=False)`

* `url`: The url that should be resolved.
* `callback`: Run asynchronously if a callback method is provided.
* `audio`: Should audio be resolved?
* `video`: Should video be resolved?

#### Examples
Synchronous:
```python
from Offliberate import request
container = request("https://www.youtube.com/watch?v=le0BLAEO93g", audio=True, 
	video=True)

print(container.audio)
print(container.video)
print(container.url)
```

Asynchronous:
```python
from Offliberate import request

def callback(container):
	print(container.audio)
	print(container.video)
	print(container.url)

request("https://www.youtube.com/watch?v=le0BLAEO93g", audio=True, 
	video=True, callback=callback)
```

### To-Do
* Windows support  
    Windows works if '-p' is specified.  
    (Basically all fancy output has to be disabled)
