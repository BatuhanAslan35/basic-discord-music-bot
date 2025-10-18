# 🎵 Discord Music Bot

This is a lightweight Discord music bot developed using Python and Discord.py, capable of playing music from YouTube via text commands. It uses `yt-dlp` for extracting audio stream URLs and `ffmpeg` to play the audio in voice channels.

This project was built as a personal learning experience, with help from generative AI tools like Google Gemini for structure and flow, and personal contributions made on functionality, debugging, and customization.

---

## ⚙️ Features

- ✅ Join and leave voice channels  
- ▶️ Play music from YouTube (search or direct link)  
- ⏸️ Pause and ▶️ resume music  
- ⏹️ Stop playback  
- 📶 Handles voice state updates properly  
- ❗ Error handling for invalid inputs or links  

---

## 💡 Commands

| Command         | Description                               |
|----------------|-------------------------------------------|
| `!play [search/link]`   | Searches or plays a YouTube video |
| `!pause`        | Pauses the current song                  |
| `!resume`       | Resumes the paused song                  |
| `!stop`         | Stops the current song                   |
| `!leave`        | Makes the bot leave the voice channel    |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- `ffmpeg` installed and available in system PATH
- A Discord bot token

### Dependencies

Install required packages:

```bash
pip install discord.py yt-dlp
