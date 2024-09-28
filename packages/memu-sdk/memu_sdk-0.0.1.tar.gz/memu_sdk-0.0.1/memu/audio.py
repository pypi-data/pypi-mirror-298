import os
import requests
from openai import OpenAI
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Audio:
    BASE_URL = "https://memu-sdk-backend.herokuapp.com"  # Replace with actual backend API URL

    def __init__(self, memu_api_key: str):
        self.memu_api_key = memu_api_key
        self.client_name = self.validate_api_key()
        self.openai_api_key = self.get_openai_api_key()
        self.client = OpenAI(api_key=self.openai_api_key)

    def validate_api_key(self) -> str:
        """Validate MeMu API key by calling the backend."""
        response = self.make_request("GET", "/validate_api_key", params={"api_key": self.memu_api_key})
        return response.get("client_name")

    def get_openai_api_key(self):
        """Fetch the OpenAI API key from the backend."""
        try:
            response = self.make_request("GET", "/openai_api_key", params={"api_key": self.memu_api_key})
            if response and "openai_api_key" in response:
                return response["openai_api_key"]
            else:
                raise ValueError("OpenAI API key not found in the response.")
        except Exception as e:
            logger.error(f"Failed to get OpenAI API key: {e}")
            raise

    def make_request(self, method: str, endpoint: str, params=None, json=None) -> dict:
        """Generic method to handle API calls to the backend."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.request(method, url, params=params, json=json)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise ValueError(f"Error in API request to {endpoint}")

    def check_balance(self, minimum_required: float) -> bool:
        """Helper method to check if the client has enough balance."""
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
        if current_balance < minimum_required:
            raise ValueError(f"Insufficient balance. A minimum balance of ${minimum_required} is required to proceed. Current balance: ${current_balance}.")
        return True

    def deduct_client_balance(self, total_cost: float):
        """Deduct the total cost from the client's balance by calling the backend API."""
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")

        # Check if there is enough balance to cover the cost
        if current_balance < total_cost:
            logger.error(f"Insufficient balance to cover the cost. Current balance: ${current_balance}, total cost: ${total_cost}")
            raise ValueError(f"Insufficient balance to cover transcription cost. Total cost: ${total_cost}, current balance: ${current_balance}")

        # Proceed with deduction if balance is sufficient
        new_balance = current_balance - total_cost
        self.make_request("POST", "/balance/update", params={"api_key": self.memu_api_key}, json={"balance": new_balance})
        logger.info(f"Deducted ${total_cost} from {self.client_name}. New balance: ${new_balance}.")

    def reencode_audio(self, input_path: str, output_path: str, target_format: str = "wav") -> str:
        """Re-encodes the audio file to a specified format."""
        logger.info(f"Re-encoding audio file: {input_path} to {output_path}")
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format=target_format, parameters=["-ar", "16000", "-ac", "1"])
        return output_path

    def split_audio(self, audio_file_path: str, chunk_length_ms: int = 600000) -> list:
        """Splits an audio file into smaller chunks and returns file paths."""
        logger.info(f"Splitting audio file: {audio_file_path}")
        audio = AudioSegment.from_file(audio_file_path)
        chunk_file_paths = []
        for i in range(0, len(audio), chunk_length_ms):
            chunk = audio[i:i + chunk_length_ms]
            chunk_file_path = f"{audio_file_path}_{i // chunk_length_ms}.wav"
            chunk.export(chunk_file_path, format="wav")
            chunk_file_paths.append(chunk_file_path)
        return chunk_file_paths

    def transcribe_audio_chunk(self, audio_file_path: str, language: str = "en", prompt: str = None) -> dict:
        """Transcribes a single audio chunk using OpenAI Whisper with verbose response."""
        try:
            with open(audio_file_path, 'rb') as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language,
                    temperature=0,
                    response_format="verbose_json",
                    prompt=prompt
                )
            logger.info(f"Verbose transcription response: {transcription}")
            return transcription
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            raise e

    def transcribe_audio_file(self, file_path: str, language: str = "en", prompt: str = None) -> str:
        """Handles the complete flow of re-encoding, splitting, transcribing, correcting, and billing."""
        
        # Step 1: Ensure the client has at least $10 balance before proceeding
        minimum_required_balance = 10.00
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
        logger.info(f"Current balance before transcription: ${current_balance}")
        
        if current_balance < minimum_required_balance:
            raise ValueError(f"Insufficient balance. A minimum balance of ${minimum_required_balance} is required to proceed. Current balance: ${current_balance}.")

        # Step 2: Re-encode the audio file
        with NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            reencoded_file_path = self.reencode_audio(file_path, f"{temp_audio_file.name}_reencoded.wav")

        # Step 3: Split the audio into chunks and transcribe
        audio_chunks = self.split_audio(reencoded_file_path)
        full_transcription = ""
        total_duration = 0

        for chunk_file_path in audio_chunks:
            transcription_data = self.transcribe_audio_chunk(chunk_file_path, language=language, prompt=prompt)
            full_transcription += transcription_data.text + "\n"
            total_duration += transcription_data.duration / 60  # Convert to minutes
            os.remove(chunk_file_path)  # Clean up chunk files

        os.remove(reencoded_file_path)

        if full_transcription.strip():
            # Step 4: Deduct the transcription cost BEFORE checking balance for correction
            total_input_tokens = len(full_transcription.split())  # Assume token count for input
            total_output_tokens = total_input_tokens  # Simplified, adjust as needed

            # Step 5: Calculate cost using backend API
            total_cost = self.make_request("POST", "/calculate_cost", json={
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
                "duration_minutes": total_duration
            }).get("total_cost")

            # Step 6: Deduct the cost from the client's balance
            self.deduct_client_balance(total_cost)
            logger.info(f"Deducted cost: ${total_cost}.")

            # Step 7: Ensure the client still has at least $10 before proceeding with correction
            current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
            logger.info(f"Balance before correction: ${current_balance}")

            if current_balance < minimum_required_balance:
                logger.warning(f"Insufficient balance for transcription correction. Current balance: ${current_balance}")
                raise ValueError(f"Insufficient balance for transcription correction. A minimum balance of ${minimum_required_balance} is required to proceed. Current balance: ${current_balance}.")

            # Step 8: Correct the transcription
            corrected_transcription, total_input_tokens, total_output_tokens = self.correct_transcription(full_transcription)

            # Step 9: Log the usage
            log_payload = {
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
                "duration_minutes": total_duration
            }
            logger.info(f"Logging transcription usage with payload: {log_payload}")

            # Make the request to log transcription usage
            try:
                self.make_request("POST", "/log_transcription_usage", params={"api_key": self.memu_api_key}, json=log_payload)
                logger.info("Successfully logged transcription usage.")
            except Exception as e:
                logger.error(f"Failed to log transcription usage: {e}")
                raise e

            return corrected_transcription
        else:
            raise ValueError("Transcription failed: no text was transcribed.")

    def correct_transcription(self, transcription_text: str, system_prompt: str = None) -> tuple:
        """Post-processes and corrects the transcription using OpenAI GPT."""
        system_prompt = (
            "You are a helpful assistant for the medical team. "
            "Correct any transcription errors, ensure medical terms are spelled correctly, "
            "and apply appropriate punctuation."
        )
        # Check if the client has enough balance before proceeding with correction
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
        minimum_required_balance = 10.00
        logger.info(f"Balance before correction: ${current_balance}")

        if current_balance < minimum_required_balance:
            logger.warning(f"Insufficient balance for correction. Current balance: ${current_balance}")
            raise ValueError(f"Insufficient balance for transcription correction. A minimum balance of ${minimum_required_balance} is required to proceed.")

        # Proceed with correction if the balance is sufficient
        response = self.client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt or "Correct any errors and apply appropriate punctuation."},
                {"role": "user", "content": transcription_text}
            ]
        )
        
        corrected_transcription = response.choices[0].message.content.strip()
        total_input_tokens = response.usage.prompt_tokens
        total_output_tokens = response.usage.completion_tokens
        logger.info(f"Total tokens used: {response.usage.total_tokens}")

        return corrected_transcription, total_input_tokens, total_output_tokens
