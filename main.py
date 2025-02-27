import yt_dlp
import os
import subprocess
import logging
import re
from moviepy import AudioFileClip

# Configure logging
logging.basicConfig(
    filename="process.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)


def extract_video_id(video_url):
    """
    Extracts the YouTube video ID from a URL.
    Example: https://www.youtube.com/watch?v=m9jMKheN0iU → m9jMKheN0iU
    """
    match = re.search(r"v=([a-zA-Z0-9_-]+)", video_url)
    return match.group(1) if match else "unknown_video"


def download_video(video_url):
    """
    Downloads a YouTube video using yt-dlp.
    Returns the filename if successful, otherwise None.
    """
    output_filename = "downloaded_video.mp4"
    
    ydl_opts = {
        'format': 'bestaudio/best',  # Audio only for efficiency
        'outtmpl': output_filename
    }
    
    try:
        logging.info("Starting video download...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        logging.info(f"Video successfully downloaded as '{output_filename}'")
        return output_filename

    except Exception as e:
        logging.error(f"Failed to download video: {e}")
        return None


def convert_to_mp3(video_path):
    """
    Converts a downloaded video to an MP3 file.
    Deletes the original video file after conversion.
    """
    try:
        mp3_filename = "audio.mp3"
        logging.info(f"Starting MP3 conversion for {video_path}...")

        # Extract audio
        audio = AudioFileClip(video_path)
        audio.write_audiofile(mp3_filename)

        logging.info(f"MP3 file saved as '{mp3_filename}'")

        # Remove video after conversion
        os.remove(video_path)
        logging.info(f"Deleted temporary video file '{video_path}'")

        return mp3_filename

    except Exception as e:
        logging.error(f"Error during MP3 conversion: {e}")
        return None


def separate_stems(mp3_file, video_id):
    """
    Uses Demucs to separate the MP3 file into stems.
    Stems will be stored in 'stems_/video_id/'.
    """
    try:
        output_folder = f"stems_/{video_id}"
        os.makedirs(output_folder, exist_ok=True)  # Ensure the folder exists

        logging.info(f"Starting Demucs separation for '{mp3_file}'...")
        logging.info(f"Stems will be stored in: {output_folder}/")

        # Run Demucs command
        command = f"demucs --out={output_folder} \"{mp3_file}\""
        subprocess.run(command, shell=True, check=True)

        logging.info(f"Stems separation completed. Files saved in '{output_folder}/'.")

    except subprocess.CalledProcessError as e:
        logging.error(f"Error running Demucs: {e}")


def main(video_url):
    """
    Main process that downloads a YouTube video, converts it to MP3, and separates stems.
    """
    logging.info("========== Starting Process ==========")

    # Extract video ID
    video_id = extract_video_id(video_url)
    logging.info(f"Extracted video ID: {video_id}")

    # Step 1: Download the video
    video_path = download_video(video_url)
    
    if video_path:
        logging.info("Video download completed successfully.")

        # Step 2: Convert video to MP3
        mp3_file = convert_to_mp3(video_path)
        if mp3_file:
            logging.info(f"MP3 file '{mp3_file}' is ready.")

            # Step 3: Separate stems with Demucs
            separate_stems(mp3_file, video_id)
    
    logging.info("========== Process Finished ==========")


if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    main(video_url)
