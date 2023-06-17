"""
First of all, make vk-playlist.txt file. You can do it like this:
1. Go to vk page of you playlist
2. Click F12
3. Paste this code and click Enter:

(async () => {
  const scroll = (top) => window.scrollTo({ top });
  const delay = (ms) => new Promise((r) => setTimeout(r, ms));

  async function scrollPlaylist() {
    const spinner = document.querySelector('.CatalogBlock__autoListLoader');
    let pageHeight = 0;
    do {
      pageHeight = document.body.clientHeight;
      scroll(pageHeight);
      await delay(400);
    } while (
      pageHeight < document.body.clientHeight ||
      spinner?.style.display === ''
    );
  }

  function parsePlaylist() {
    return [...document.querySelectorAll('.audio_row__performer_title')].map(
      (row) => {
        const [artist, title] = ['.audio_row__performers', '.audio_row__title']
          .map(selector => row.querySelector(selector)?.textContent || '')
          .map((v) => v.replace(/[\s\n ]+/g, ' ').trim());

        return [artist, title].join(' - ');
      },
    );
  }

  function saveToFile(filename, content) {
    const data = content.replace(/\n/g, '\r\n');
    const blob = new Blob([data], { type: 'text/plain' });
    const link = document.createElement('a');
    link.download = filename;
    link.href = URL.createObjectURL(blob);
    link.target = '_blank';
    link.style.display = 'none';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  // Main
  await scrollPlaylist();
  const list = parsePlaylist();
  saveToFile('vk-playlist.txt', list.join('\n'));
})();

4. Past vk-playlist.txt to same directory
p.s Thanks https://github.com/fivemru for parse code!
"""

from youtubesearchpython import VideosSearch
from pytube import YouTube
from moviepy.editor import *


def make_song_massive():
    music_massive = []
    music_list = open("vk-playlist.txt", encoding = "UTF-8")
    for line in music_list:
        music_massive.append(line.replace('\n', ' instrumental karaoke')) # I think, if you need download another version of music, like covers mb, just change this string
    return music_massive


def fiend_song(music_massive):
    video_titles = music_massive
    video_links = []

    for title in video_titles:
        search = VideosSearch(title)
        results = search.result()['result']

        if len(results) > 0:
            video_links.append(results[0]['link'])
    return video_links


music_massive = make_song_massive()
video_urls = fiend_song(music_massive)
# I recommend you copy video_urls list, because if it crashed, you can just past this list like constant and dont need to fiend songs again
print(video_urls)
# Delete fiend_song fuction if you need it

for url in video_urls:
    # Music are download at same directory
    try:
        yt = YouTube(url)
        title = yt.title.replace(" ", "_").replace(".", "")  # Remove spaces and dots from the title
        audio_stream = yt.streams.filter(only_audio = True).first()
        audio_file = audio_stream.download(filename = f"{title}_temp")
        audio = AudioFileClip(audio_file)
        audio.write_audiofile(f"{title}.mp3")
        os.remove(audio_file)  # Remove temporary audio file
        print(f"Downloaded and converted: {title}.mp3")
    except Exception as e:
        print(f"Error downloading and converting audio: {e}")
