import json
import logging
import requests
from openai import OpenAI

logger = logging.getLogger(__name__)

class MedicalEntityExtractor:
    BASE_URL = "https://memu-sdk-backend.herokuapp.com"  # Replace with actual backend API URL

    def __init__(self, memu_api_key: str):
        self.memu_api_key = memu_api_key
        self.client_name = self.validate_api_key()
        self.openai_api_key = self.get_openai_api_key()
        self.client = OpenAI(api_key=self.openai_api_key)
        self.total_input_tokens = 0
        self.total_output_tokens = 0

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

    def extract_medical_entities(self, transcript, medical_records):
        """Extract medical entities from the transcript and medical records."""
        
        minimum_required_balance = 10.00
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
        logger.info(f"Current balance before operation: ${current_balance}")
        
        if current_balance < minimum_required_balance:
            raise ValueError(f"Insufficient balance. A minimum balance of ${minimum_required_balance} is required to proceed. Current balance: ${current_balance}.")

        logger.info("Starting medical entity extraction...")

        # Combine transcript with medical records
        combined_input = {
            "Transcript": transcript,
            "MedicalRecords": medical_records
        }

        # Define the structured format example for extracted entities
        entities_format_example = {
            "MedicalEntities": {
                "Medications": ["Lisinopril", "Metformin"],
                "Procedures": ["Procedure 1", "Procedure 2"],
                "Diseases": ["Hypertension", "Diabetes"],
                "Diagnoses": ["Diagnosis 1", "Diagnosis 2"]
            }
        }

        try:
            # Call to the OpenAI model with a structured prompt
            response = self.client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a medical assistant. Extract and list all medical entity names in JSON format using this template: {json.dumps(entities_format_example, indent=2)}."
                    },
                    {
                        "role": "user",
                        "content": f"Extract medical entities based on this data: {json.dumps(combined_input, indent=2)}"
                    }
                ],
                temperature=0
            )

            # Capture the structured output from the model
            structured_output = response.choices[0].message.content.strip().strip('```json').strip()
            total_input_tokens = response.usage.prompt_tokens
            total_output_tokens = response.usage.completion_tokens
            token_count = response.usage.total_tokens  # Capture total token count

            # Parse the JSON output
            extracted_entities = json.loads(structured_output)
            logger.info(f"Extracted medical entities: {json.dumps(extracted_entities, indent=2)}")

            # Log the usage after successful extraction
            self.log_usage(total_input_tokens, total_output_tokens)

            return extracted_entities, "Extraction successful"

        except json.JSONDecodeError as e:
            error_message = f"Failed to decode JSON: {e}"
            logger.error(error_message)
            return {"error": error_message}, error_message

        except Exception as e:
            error_message = f"An error occurred during the medical entity extraction process: {str(e)}"
            logger.error(error_message)
            return {"error": error_message}, error_message

    def log_usage(self, total_input_tokens, total_output_tokens):
        """Log the usage of tokens for billing purposes."""
        log_payload = {
            "input_tokens": total_input_tokens,
            "output_tokens": total_output_tokens,
            "duration_minutes": 0  # Since interaction checks don't involve audio
        }

        logger.info(f"Logging interaction usage with payload: {log_payload}")

        try:
            self.make_request("POST", "/log_transcription_usage", params={"api_key": self.memu_api_key}, json=log_payload)
            logger.info("Successfully logged usage for drug interaction checking.")
        except Exception as e:
            logger.error(f"Failed to log usage: {e}")
        
        total_cost = self.make_request("POST", "/calculate_cost", json={
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
                "duration_minutes": 0
            }).get("total_cost")

            # Step 6: Deduct the cost from the client's balance
        self.deduct_client_balance(total_cost)
        logger.info(f"Deducted cost: ${total_cost}.")
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
        logger.info(f"Current balance after operation: ${current_balance}")
