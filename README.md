A simple Python script to measure **upload and download speed** with Telegram.

---

## Features

- Upload and download test files to **Saved Messages** in Telegram.
- Live progress display with upload/download arrows (⬆ / ⬇).
- Reports speed in **MB/s** and **Mbps**.
- Configurable test file size.
- Uses `.env` for `API_ID` and `API_HASH`.

---

## Requirements

- [Python 3.13+](http://python.org/)
- [UV](https://docs.astral.sh/uv/getting-started/installation/) 
---

## Setup

Create a `.env` file in the project root:

```
API_ID=your_api_id
API_HASH=your_api_hash
```

---

## Usage

```bash
uv run main.py -- --size 50
```

> Note: the `--` before `--size` is required for uv to pass arguments to the script.

---

## How it works

1. Generates a temporary random test file.
2. Uploads it to your **Saved Messages** in Telegram.
3. Downloads it back.
4. Prints live progress and final upload/download speed.
5. Deletes temporary files and the test message.