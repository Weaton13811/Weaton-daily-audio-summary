# Daily Audio Summary

An AI-powered morning news briefing for the Binghamton, NY area. Gathers local headlines, uses Claude to write a polished briefing script, converts it to audio with macOS premium voices, and delivers it to your phone via iMessage — every morning at 6 AM.

## How It Works

1. **News gathering** — Pulls local headlines from RSS feeds and Google News for Binghamton NY
2. **AI summarization** — Claude writes a concise, radio-anchor-style briefing script
3. **Text-to-speech** — macOS `say` command with premium voices converts the script to audio (AAC)
4. **iMessage delivery** — AppleScript sends the audio file to your phone via Messages.app
5. **Scheduled daily** — macOS `launchd` triggers the pipeline at 6 AM every morning

## Requirements

- **macOS** (for `say`, `afconvert`, Messages.app, and `launchd`)
- **Python 3.10+**
- **Anthropic API key** (for Claude summarization)
- **iMessage** signed in on the Mac

## Setup

```bash
# Clone and install
git clone <repo-url> && cd Weaton-daily-audio-summary
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Set your API key
export ANTHROPIC_API_KEY="your-key-here"
```

## Configuration

Create a `config.json` in the project root (optional — defaults to Binghamton NY):

```json
{
    "location": "Binghamton, NY",
    "claude_model": "claude-sonnet-4-5-20250929",
    "tts_voice": "Evan (Premium)",
    "imessage_to": "+15551234567",
    "rss_feeds": [
        "https://www.wbng.com/news/local/feed/",
        "https://spectrumlocalnews.com/nys/binghamton.rss",
        "https://www.pressconnects.com/rss/news/"
    ],
    "google_news_query": "Binghamton NY local news"
}
```

Settings can also be set via environment variables:
- `ANTHROPIC_API_KEY` — your Anthropic API key
- `DAS_IMESSAGE_TO` — iMessage recipient phone number
- `DAS_CONFIG` — path to a custom config file

### Choosing a Voice

List available macOS voices:
```bash
say -v '?'
```

Some good options: `Evan (Premium)`, `Samantha (Enhanced)`, `Zoe (Premium)`. Download premium voices in **System Settings > Accessibility > Spoken Content > System Voice > Manage Voices**.

## Usage

```bash
# Run manually
python -m daily_audio_summary -v

# Run without sending iMessage (just generate audio)
python -m daily_audio_summary --no-send

# Use a custom config
python -m daily_audio_summary --config /path/to/config.json
```

## Schedule (6 AM Daily)

1. Edit `com.dailyaudiosummary.plist` — update the paths, API key, and phone number
2. Install the schedule:

```bash
cp com.dailyaudiosummary.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.dailyaudiosummary.plist
```

To unload: `launchctl unload ~/Library/LaunchAgents/com.dailyaudiosummary.plist`

## Testing

```bash
pytest
```

## Project Structure

```
daily_audio_summary/
├── __init__.py       # Package init
├── __main__.py       # CLI entry point & pipeline orchestration
├── config.py         # Configuration loading (JSON + env vars)
├── news.py           # RSS + Google News scraping
├── summarizer.py     # Claude-powered briefing script generation
├── audio.py          # macOS text-to-speech (say + afconvert)
└── imessage.py       # iMessage delivery via AppleScript
tests/
├── test_config.py
├── test_news.py
├── test_summarizer.py
└── test_imessage.py
com.dailyaudiosummary.plist  # launchd schedule (6 AM daily)
```
