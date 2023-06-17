# vk-music-instrumental
SImply program that takes list of songs from VK and download there instrumental version
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
p.s Thanks https://github.com/fivemru for this code!
