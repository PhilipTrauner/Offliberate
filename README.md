# Offliberate

<img align="right" src="https://cloud.githubusercontent.com/assets/9287847/22620779/6918a678-eb13-11e6-9f98-95eb90db133e.png">


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

