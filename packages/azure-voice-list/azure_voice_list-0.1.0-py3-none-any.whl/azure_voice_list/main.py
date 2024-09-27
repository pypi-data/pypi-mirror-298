"""Module for Azure Cognitive Services Speech SDK integration."""

import os
import datetime
from pathlib import Path
import logging
from dotenv import load_dotenv, find_dotenv
import azure.cognitiveservices.speech as speechsdk  # type: ignore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


def get_available_voices(speech_key: str, service_region: str) -> list:
    """Get available voices from Azure Cognitive Services Speech SDK."""
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=None
    )

    result = speech_synthesizer.get_voices_async().get()

    if result.reason == speechsdk.ResultReason.VoicesListRetrieved:
        logging.info("Successfully retrieved voices.")
        return result.voices
    else:
        logging.error("Error retrieving voices: %s", result.error_details)
        return []


def main():
    """Main function to demonstrate voice retrieval."""
    load_dotenv(find_dotenv())

    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")

    if not speech_key or not service_region:
        logging.error(
            "Error: AZURE_SPEECH_KEY or AZURE_SPEECH_REGION environment variables are not set."
        )
        return

    voices = get_available_voices(speech_key, service_region)
    if voices:
        # Define output directory relative to project root
        project_root = Path(__file__).resolve().parents[2]
        output_dir = project_root / "output"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename with current date and time
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"voice_attributes_{current_time}.txt"
        filepath = output_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("Available attributes:\n")
            for voice in voices:
                for attr in dir(voice):
                    if not attr.startswith("_"):  # Skip private attributes
                        value = getattr(voice, attr)
                        f.write(f"{attr}: {value}\n")
                f.write("-" * 60 + "\n")
        logging.info("Voice attributes have been saved to '%s'", filepath)
    else:
        logging.error("Failed to retrieve voices.")


if __name__ == "__main__":
    main()
