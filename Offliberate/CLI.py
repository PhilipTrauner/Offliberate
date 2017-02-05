# -*- coding: utf-8 -*-

try:
	from . import Offliberate
except (SystemError, ValueError):
	import Offliberate
try:
	from urlparse import urlparse
except ImportError:
	from urllib.parse import urlparse
try:
	from thread import start_new_thread
except ImportError:
	from _thread import start_new_thread

import argparse

from sys import stdout
from sys import version_info
from time import sleep
from time import time
from os.path import splitext
from os.path import isdir
from os.path import abspath
from requests import get
from sys import stdin


def get_terminal_width_2():
	return int(popen('stty size', 'r').read().split()[1])


def get_terminal_width_3():
	return get_terminal_size().columns


if version_info.major == 3:
	if version_info.minor >= 3:
		from shutil import get_terminal_size
		get_terminal_width = get_terminal_width_3
	else:
		from os import popen
		get_terminal_width = get_terminal_width_2
else:
	from os import popen
	get_terminal_width = get_terminal_width_2


def prettify_rate(rate):
	rate_divided_by_thousand = rate / 1000
	if (rate_divided_by_thousand) >= 1000000:
		return "%dTB/s" % (rate / 1000000000)
	elif (rate_divided_by_thousand) >= 1000:
		return "%dGB/s" % (rate / 1000000)
	elif (rate_divided_by_thousand) >= 1:
		return "%dMB/s" % (rate_divided_by_thousand)
	else:
		return "%dKB/s" % rate


def progress_bar(size, part_lenght, iterable, fill_char=u"█", 
	delimiter=u"|", ratio=3, text=""):
	"""
	size: Full size of iterable
	part_lenght: Parts fetched from generator per yield
	iterable: Generator with known length
	fill_char: Character that fills the progress bar
	delimiter: On both ends of progress bar
	ratio: Determines the progress bar width in relation with terminal width
	"""
	start_time = time()
	max_progress = size
	progress = 0
	iteration = 0
	total_iterations = int(size / part_lenght)
	last_terminal_width = get_terminal_width()
	for part in iterable:
		yield part
		iteration += 1 # Needed for speed
		progress += part_lenght # Needed to check for completion
		since_start_time = time() - start_time # Time since start of function execution
		terminal_width = get_terminal_width()
		width_progress = (terminal_width / ratio) - 19 # 19 is the lenght of all non-dynamic elements
		part_length = width_progress / 100.0 # Length of one part as float
		percise_progress = (progress / (float(max_progress) / 100)) # Progress as float
		percent_progress = int(percise_progress) # Progress as integer
		prettified_progress_rate = prettify_rate(iteration / since_start_time) # Prettified progress rate has to be known for filler to be calculated
		whitespaces_in_bar = int(width_progress) - (int(percise_progress * part_length)) # How many whitespaces the bar consists of
		filler_in_bar = int(percise_progress * part_length) # How many filler characters the bar consists of
		empty_space = terminal_width - (19 + filler_in_bar + whitespaces_in_bar)
		if terminal_width != last_terminal_width: # Clear whole line if terminal size changed since last draw
			last_terminal_width = terminal_width # Change last terminal width to current one for future comparison
			stdout.write(u"\r%s" % (" " * last_terminal_width))
			stdout.flush()
		if terminal_width > 19: # Maximum with of progress bar assuming 100MB/s
				stdout.write(u"\r%s%s%s%s (%s%d%%) [%s%s] %s" % (
				delimiter,
				fill_char * (int(percise_progress * part_length)), # Filler char for progress
				" " * whitespaces_in_bar, # Whitespaces for progress
				delimiter,
				" " * (3 - len(str(percent_progress))), # Center percent count in brackets
				percent_progress, # Percent
				" " * (7 - len(str(prettified_progress_rate))),
				prettified_progress_rate, # Progress rate
				text if len(text) < empty_space else text[:empty_space - 4] + u"..."))
		elif terminal_width > 14: # Progress bar is not shown if the terminal width is too small
			stdout.write(u"\r(%s%d) [%s%s]" % (
				" " * (3 - len(str(percent_progress))), # Center percent count in brackets
				percent_progress,
				" " * (7 - len(str(prettified_progress_rate))),
				prettified_progress_rate))
		else:
			stdout.write(u"\r(%s%d)" % (
				" " * (3 - len(str(percent_progress))), # Center percent count in brackets
				percent_progress))
		stdout.flush()
	if progress == max_progress:
		if version_info.major == 3:
			print()
		else:
			print


class ProgressIndicator:
	def __init__(self, animation, delay):
		self.started = False
		self.animation = animation
		self.delay = delay
		self.status = ""
		self.longest_frame_length = 0
		for frame in self.animation:
			frame_length = len(frame)
			if frame_length > self.longest_frame_length:
				self.longest_frame_length = frame_length

	def start(self):
		self.started = True
		start_new_thread(self._start, ())

	def _start(self):
		while self.started:
			for frame in self.animation:
				if self.started:
					stdout.write("\r%s %s%s" % (frame, self.status, " " * 
						(get_terminal_width() - len(frame) - len(self.status) - 1)))
					stdout.flush()
					sleep(self.delay)
				

	def stop(self, flush=True):
		self.started = False
		if flush:
			stdout.write("\r%s" % (" " * get_terminal_width()))
			stdout.write("\r")
			stdout.flush()


def is_valid_url(url):
	return urlparse(url).scheme != ""


def download_file(url, path, pretty=True):
	response = get(url, stream=True)
	size = int(response.headers['Content-Length'].strip())
	with open(path, "wb") as handle:
		for data in progress_bar(size, 1024, response.iter_content(1024), 
			text=url) if pretty else response.iter_content(1024):
			handle.write(data)


def resolve_file_name(url):
	if "?" in url:
		question_mark_location = url.find("?")
		slash_location = question_mark_location
		for char in url[:question_mark_location][::-1]:
			if char != "/":
				slash_location -= 1
			else:
				break
		return url[slash_location:question_mark_location]
	if "offliberty.com" in url:
		name_start_position = len(url)
		for char in url[::-1]:
			if char != "/":
				name_start_position -= 1
			else:
				break
		return url[name_start_position:]


def is_dir(path):
	if isdir(path):
		path = abspath(path)
		return path + "/" if path[-1] != "/" else path


def entry_point():
	try:
		if version_info.major < 3:
			print("Unsupported Python version. You are on your own now...")

		parser = argparse.ArgumentParser()

		group = parser.add_argument_group("required media type parameters")
		group.add_argument("-a", "--audio", help="fetch audio urls (default)", 
			action="store_true")
		group.add_argument("-v", "--video", help="fetch video urls", 
			action="store_true")

		parser.add_argument("-p", "--pretty", 
			help="disable progress indicators", 
			action="store_false")
		parser.add_argument("--download-location", type=is_dir)
		parser.add_argument("--no-download", action="store_true")
		parser.add_argument("urls", help="url(s) you want to offliberate", 
			nargs="*")

		args = parser.parse_args()

		if not args.audio and not args.video:
			args.audio = True

		if args.download_location != None:
			if not args.download_location.endswith("/"):
				args.download_location += "/"

		if len(args.urls) == 0:
			for url in stdin.readlines():
				args.urls.append(url.rstrip("\n").replace("\\", ""))

		if args.pretty and len(args.urls) != 0:
			animation = [u"⠋", u"⠙", u"⠹", u"⠸", u"⠼", u"⠴", u"⠦", 
			u"⠧", u"⠇", u"⠏"]
			progress_indicator = ProgressIndicator(animation, 0.20)
			progress_indicator.start()
			

		results = []
		invalid_urls = []

		for url in args.urls:
			if is_valid_url(url):
				if args.pretty:
					progress_indicator.status = url
				if args.audio and args.video:
					if args.pretty:
						progress_indicator.status = u"🎵  " + url
					audio_result = Offliberate.request(url, audio=True)
					if args.pretty:
						progress_indicator.status = u"🎬  " + url
					video_result = Offliberate.request(url, audio=False, video=True)
					results.append(audio_result.combine(video_result))
				else:
					results.append(Offliberate.request(url, audio=args.audio, 
						video=args.video))
			else:
				invalid_urls.append(url)


		if args.pretty and len(args.urls) != 0:
			progress_indicator.stop()

		for url in invalid_urls:
			print("%sInvalid url: %s" % (u"❌  " if args.pretty else "", url))

		for result in results:
			if len(results) > 1:
				if result != None:
					print(result.url) 
			if result == None:
				print("%s: Something went wrong... :(" % (u"❌ " 
					if args.pretty else "Offliberty error"))
			else:		
				if args.audio:
					print("%s: %s" % (u"🎵 " if args.pretty else "Audio", result.audio))
				if args.video and result.video:
					print("%s: %s" % (u"🎬 " if args.pretty else "Video", result.video))
				if args.video and not result.video:
					print("%s: %s" % (u"❌  🎬 " if args.pretty else "Error fetching video", 
						result.url))

		if not args.no_download:
			if args.download_location == None:
				args.download_location = ""
			for result in results:
				if result != None:
					if args.audio:
						if result.audio != None:
							file_name = resolve_file_name(result.audio)
							# If file extension can't be determined by looking at the url
							# we assume it's mp3
							if splitext(file_name)[-1].lower() == "":
								file_name += ".mp3"
							download_file(result.audio, args.download_location + file_name, 
								pretty=args.pretty)
					if args.video:
						if result.video != None:
							download_file(result.video, 
								args.download_location + resolve_file_name(result.video), 
								pretty=args.pretty)
			if version_info.major == 3:
				print()
			else:
				print

	except KeyboardInterrupt:
		pass