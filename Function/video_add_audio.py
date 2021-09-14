import os


def video_add_audio(ffmpeg_path, save_path, m4s_file1_path, m4s_file2_path):
    """
    ffmpeg -i video.mp4 -i audio.m4a -c:v copy -c:a copy output.mp4
     视频添加音频
    :param ffmpeg_path: ffmpeg的安装 bin 路径
    :param save_path: 文件保存路径
    :param m4s_file1_path: 传入视频文件的路径
    :param m4s_file2_path: 传入音频文件的路径
    :return:
    """
    mp4_name = m4s_file1_path.split('/')[-1].split('.m4s')[0] + '-temp.mp4'
    mp3_name = m4s_file1_path.split('/')[-1].split('.m4s')[0] + '-temp.mp3'
    outfile_name = m4s_file1_path.split('.m4s')[0] + '.mp4'
    os.system(r'%sffmpeg -i %s %s' % (ffmpeg_path, m4s_file1_path, save_path + mp4_name))
    os.system(r'%sffmpeg -i %s %s' % (ffmpeg_path, m4s_file2_path, save_path + mp3_name))
    os.system(r'%sffmpeg -i %s -i %s -c:v copy -c:a copy %s' % (
        ffmpeg_path, save_path + mp4_name, save_path + mp3_name, outfile_name))
    os.remove(save_path + mp4_name)
    os.remove(save_path + mp3_name)
    os.remove(m4s_file1_path)
    os.remove(m4s_file2_path)
