from pytube import YouTube

obj = YouTube("https://www.youtube.com/watch?v=ZrdQSAX2kyw")

strs = obj.streams.get_by_resolution(resolution="720p")
print(strs.mime_type)

# strm_all = obj.streams.filter(mime_type="video/mp4")
# l = {}
# l = {video for video in strm_all if video.resolution not in l.fromkeys("resolution")}
# for li in l:
#     print(li)
# print(l)