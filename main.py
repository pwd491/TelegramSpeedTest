import os
import time
import asyncio
import tempfile
import argparse
from dotenv import load_dotenv
from telethon import TelegramClient
from FastTelethon import upload_file, download_file

# ===== Load environment variables =====
load_dotenv()

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
if not API_ID or not API_HASH:
    raise ValueError("API_ID and API_HASH must be set in the .env file")

# ===== Argument parser =====
parser = argparse.ArgumentParser(description="Telegram upload/download speed test")
parser.add_argument("--size", type=int, default=20, help="Test file size in MB")
args = parser.parse_args()
FILE_SIZE_MB = args.size

# ===== Helpers =====
def generate_test_file(size_mb: int) -> str:
    """Create a temporary file with random data and return its path"""
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(os.urandom(size_mb * 1024 * 1024))
        temp_file.flush()
    return temp_file.name

def progress_callback(transferred, total, start_time, direction="⬆"):
    elapsed = time.perf_counter() - start_time
    speed_MBps = (transferred / (1024 * 1024)) / elapsed if elapsed > 0 else 0
    percent = (transferred / total) * 100
    print(f"\r{direction} {percent:6.2f}% | {transferred / (1024*1024):.2f}/{total / (1024*1024):.2f} MB | {speed_MBps:.2f} MB/s", end="")

# ===== Main function =====
async def main():
    async with TelegramClient("speedtest.session", API_ID, API_HASH) as client:
        file_path = generate_test_file(FILE_SIZE_MB)
        print(f"\nTest file: {FILE_SIZE_MB} MB")

        # ===== Upload =====
        start = time.perf_counter()
        with open(file_path, "rb") as f:
            input_file = await upload_file(
                client,
                f,
                progress_callback=lambda sent, total: progress_callback(sent, total, start, direction="⬆")
            )

        message = await client.send_file("me", input_file, file_name=os.path.basename(file_path))
        upload_time = time.perf_counter() - start

        # ===== Download =====
        start = time.perf_counter()
        out_path = tempfile.NamedTemporaryFile(delete=False).name
        with open(out_path, "wb") as out:
            await download_file(
                client,
                message.media.document,
                out,
                progress_callback=lambda received, total: progress_callback(received, total, start, direction="⬇")
            )
        download_time = time.perf_counter() - start

        print("\n")
        print(f"⬆ Upload finished: {FILE_SIZE_MB / upload_time:.2f} MB/s ({(FILE_SIZE_MB*8)/upload_time:.2f} Mbps)")
        print(f"⬇ Download finished: {FILE_SIZE_MB / download_time:.2f} MB/s ({(FILE_SIZE_MB*8)/download_time:.2f} Mbps)")

        # ===== Cleanup =====
        await message.delete()
        os.remove(file_path)
        os.remove(out_path)

# ===== Run =====
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTest interrupted")
