# coding:utf-8
# --author-- lanhua.zhou

""" 视频文件操作函数集合 """

import os
import shutil
import subprocess
import tempfile
import hashlib
import locale

import zfused_maya
_resource = zfused_maya.resource()


def cut_image(video, image):
    """ cut video to image

    :rtype: nool
    """

    _ffmpeg_exe = _resource.get("plugins/ffmpeg", "ffmpeg.exe")
    _pic_command = u"%s -i %s -ss 0.1 -f image2 %s"%(_ffmpeg_exe, video, image)
    _pic_command = _pic_command.encode(locale.getdefaultlocale()[1])
    _pic_process = subprocess.Popen(_pic_command, shell = True)
    _pic_process.communicate()
    if not os.path.isfile(image):
        return False
    return True


def convert_video(inVideo, outVideo):
    """ convet video 

    :rtype: bool
    """
    _ffmpeg_exe = _resource.get("plugins/ffmpeg", "ffmpeg.exe")
    _command = u'%s -i "%s" -vcodec h264 -x264opts keyint=1 -y "%s"'%(_ffmpeg_exe, inVideo,outVideo)
    _command = _command.encode(locale.getdefaultlocale()[1])
    _process = subprocess.Popen(_command, shell = True)
    _process.communicate()
    if not os.path.isfile(outVideo):
        return False
    return True


def mergeVideo(filename, fps, size, images, audio = None, offset = None, time = None):
    _ffmpeg_exe = _resource.get("plugins/ffmpeg", "ffmpeg.exe")
    if audio:
        cmd = '%s -y -r %s -f image2 -s %s -i %s %s -i %s -vcodec libx264 -crf 25 -pix_fmt yuv420p -t %s %s'%(_ffmpeg_exe, fps, size, images, offset, audio, time, filename)
    else:
        cmd = '%s -y -r %s -f image2 -s %s -i %s -vcodec libx264 -crf 25 -pix_fmt yuv420p %s'%(_ffmpeg_exe, fps, size,images, filename)

    _process = subprocess.Popen(cmd, shell = True)
    _process.communicate()
    if not os.path.isfile(filename):
        return False
    return True

if __name__ == "__main__":
    mergeVideo("D:/ep01_sc004_shot137a.0001.mov", 24, "960x540", "D://_dir/ep01_sc004_shot137a.0001.%04d.jpg", "M:\HQ _AN\sound\ep01\shot138.wav", 'filter_complex "adelay=1541.66666667|1541.66666667" 2.958333')