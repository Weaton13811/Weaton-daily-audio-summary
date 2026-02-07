# Daily Audio Summary

A Python tool that generates daily audio summaries from text content.

## Features

- Collect and aggregate text content from configured sources
- Summarize content into concise daily briefs
- Convert summaries to audio using text-to-speech
- Output audio files in common formats (MP3)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

```bash
python -m daily_audio_summary
```

## Testing

```bash
pytest
```

## Project Structure

```
daily_audio_summary/
├── __init__.py       # Package init
├── __main__.py       # CLI entry point
├── config.py         # Configuration handling
├── summarizer.py     # Content summarization
└── audio.py          # Text-to-speech conversion
tests/
└── test_summarizer.py
```
