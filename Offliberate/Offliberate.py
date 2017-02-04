from requests import post
from requests import get
from requests import HTTPError
try:
	from thread import start_new_thread
except ImportError:
	from _thread import start_new_thread
try:
	from urllib import quote
except ImportError:
	from urllib.parse import quote

AUDIO = 1
VIDEO = 2
BOTH = 3

class _MediaContainer:
	"""
	Container for request results
	"""
	def __init__(self, url, audio=None, video=None):
		self.url = url
		self.audio = audio
		self.video = video


	def __repr__(self):
		return self.__str__()


	def __str__(self):
		return "Audio: %s | Video: %s" % (self.audio, self.video)


	def combine(self, media_container):
		if self.audio == None and media_container.audio != None:
			self.audio = media_container.audio
		if self.video == None and media_container.video != None:
			self.video = media_container.video
		return self


def request(url, callback=None, audio=True, video=False):
	if audio and not video:
		media_type = AUDIO
	elif video and not audio:
		media_type = VIDEO
	else:
		media_type = BOTH
	if callback:
		start_new_thread(_request, (url, media_type, callback))
	else:
		return _request(url, media_type)


def _locate_audio(body):
	audio_url_start = body.find('A HREF="h', 0) + 8
	audio_url_end = body.find('"', audio_url_start)
	return body[audio_url_start:audio_url_end]


def _locate_video(body):
	video_part_start = body.find('<b>Video</b')
	video_url_start = body.find('A HREF="h', video_part_start) + 8
	video_url_end = body.find('"', video_url_start)
	return body[video_url_start:video_url_end].rstrip()


def _request(url, media_type, callback=None):
	data = {"track" : quote(url)}
	if media_type == VIDEO:
		data.update({"video_file" : 1})
	response = post("http://offliberty.com/off03.php", data=data) 
	if response.status_code == 200 and (
		not "Something went wrong" in response.text and
		not "offliberty_giewu_bernardo_new" in response.text and
		not "Hmmm... your URL looks wrong." in response.text):
		if "mp3_file" in response.text:
			out = _MediaContainer(url, audio=_locate_audio(response.text))
		elif "vid_file" in response.text:
			if media_type == AUDIO:
				out = _MediaContainer(url, audio=_locate_audio(response.text))
			elif media_type == VIDEO:
				out = _MediaContainer(url, video=_locate_video(response.text))
		else:
			out = _MediaContainer(url, audio=_locate_audio(response.text))
		if media_type == BOTH:
			out = out.combine(_request(url, VIDEO))
		if callback:
			callback(out)
		else:
			return out
	else:
		return None