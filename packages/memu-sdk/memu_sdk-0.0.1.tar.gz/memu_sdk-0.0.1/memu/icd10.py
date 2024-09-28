import json
import logging
import requests
from openai import OpenAI

logger = logging.getLogger(__name__)

class ICD10CodeOrchestrator:
    BASE_URL = "https://memu-sdk-backend.herokuapp.com"  # Replace with actual backend API URL
    ICD10_API_URL = "https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search"  # External ICD-10-CM API

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

    def fetch_icd10_codes(self, disease: str) -> list:
        """Fetch ICD-10 codes from the external Clinical Tables API for a given disease or diagnosis."""
        minimum_required_balance = 10.00
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
        logger.info(f"Current balance before operation: ${current_balance}")
        
        if current_balance < minimum_required_balance:
            raise ValueError(f"Insufficient balance. A minimum balance of ${minimum_required_balance} is required to proceed. Current balance: ${current_balance}.")

        logger.info(f"Fetching ICD-10 codes for: {disease}")

        params = {
            'terms': disease,
            'sf': 'code,name',
            'df': 'code,name',
            'maxList': 10
        }

        try:
            response = requests.get(self.ICD10_API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            codes = data[1]
            descriptions = data[3]
            icd10_codes = [{'code': code, 'description': descriptions[index]} for index, code in enumerate(codes)]
            logger.info(f"Fetched ICD-10 codes for {disease}: {icd10_codes}")
            return icd10_codes

        except Exception as e:
            logger.error(f"Error fetching ICD-10 codes for {disease}: {str(e)}")
            return []

    def suggest_icd10_code(self, disease: str, consultation_summary: str, patient_summary: dict) -> dict:
        """Use GPT-4 to suggest the most appropriate ICD-10 code based on the disease, consultation summary, and patient context."""
        logger.info(f"Starting AI-assisted suggestion for ICD-10 code for disease: {disease}")

        # Fetch ICD-10 codes for the given disease
        icd10_codes = self.fetch_icd10_codes(disease)

        if not icd10_codes:
            logger.error(f"No ICD-10 codes found for the disease/diagnosis: {disease}")
            return {"error": f"No ICD-10 codes found for the disease/diagnosis: {disease}"}

        # Prepare context with disease, consultation summary, and patient summary
        context = {
            "disease": disease,
            "consultation_summary": consultation_summary,
            "patient_summary": patient_summary,
            "fetched_codes": icd10_codes
        }

        # Define the expected output template
        output_template = {
            "fetched_codes": [],
            "suggested_code": {
                "code": "string",
                "description": "string",
                "reason": "string"  # This field explains why the code was suggested
            }
        }

        try:
            # Call OpenAI to suggest the most appropriate ICD-10 code
            response = self.client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert in medical coding. Based on the provided disease, consultation summary, "
                            "and patient summary, suggest the most appropriate ICD-10 code from the fetched list. "
                            "Return your answer in the following JSON format:\n"
                            f"{json.dumps(output_template, indent=2)}"
                        )
                    },
                    {
                        "role": "user",
                        "content": json.dumps(context)
                    }
                ],
                temperature=0,
                response_format={"type": "json_object"}  # Ensure the response is JSON
            )

            suggested_code = json.loads(response.choices[0].message.content)
            logger.info(f"Suggested ICD-10 Code: {json.dumps(suggested_code, indent=2)}")

            # Log token usage
            self.total_input_tokens += response.usage.prompt_tokens
            self.total_output_tokens += response.usage.completion_tokens
            self.log_usage(self.total_input_tokens, self.total_output_tokens)

            return {
                "fetched_codes": icd10_codes,
                "suggested_code": suggested_code
            }

        except json.JSONDecodeError as e:
            error_message = f"Failed to decode JSON: {e}"
            logger.error(error_message)
            return {"error": error_message}

        except Exception as e:
            error_message = f"An error occurred during the ICD-10 code suggestion process: {str(e)}"
            logger.error(error_message)
            return {"error": error_message}

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
