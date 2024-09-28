import json
import logging
import requests
import uuid
import datetime
import pytz
from openai import OpenAI
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class MedicalSummarizer:
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

    def summarize_medical_info(self, transcript: str, medical_records: list) -> dict:
        """Generate a structured summary from the transcript and medical records."""
        minimum_required_balance = 10.00
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
        logger.info(f"Current balance before operation: ${current_balance}")
        
        if current_balance < minimum_required_balance:
            raise ValueError(f"Insufficient balance. A minimum balance of ${minimum_required_balance} is required to proceed. Current balance: ${current_balance}.")

        logger.info("MeMu is starting summarization with interaction data...")

        # Example format for summarization
        format_example = {
            "PatientSummary": {
                "MedicalStatus": {
                    "ChronicConditions": [],
                    "VitalSigns": {
                        "BloodPressure": "",
                        "HeartRate": "",
                        "OxygenSaturation": "",
                        "Temperature": ""
                    }
                },
                "Medications": [],
                "TreatmentPlan": [],
                "Summary": "General medical summary of the patient.",
                "Recommendations": "Recommendations based on the patient's condition and medications."
            }
        }

        # Combine transcript and medical records
        combined_input = json.dumps({
            "Transcript": transcript,
            "MedicalRecords": medical_records
        }, indent=2)

        try:
            # Call OpenAI model
            response = self.client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {
                        "role": "system",
                        "content": f"Generate a structured json summary based on this format: {json.dumps(format_example)}."
                    },
                    {
                        "role": "user",
                        "content": f"Here is the medical data: {combined_input}"
                    }
                ],
                temperature=0,
                response_format={"type": "json_object"}  # Ensure the response is JSON
            )

            # Capture and clean the output from the model
            message_content = response.choices[0].message.content.strip().strip('```json').strip()
            total_input_tokens = response.usage.prompt_tokens
            total_output_tokens = response.usage.completion_tokens

            # Parse the output into JSON
            summary_json = json.loads(message_content)
            logger.info(f"Generated Summary: {json.dumps(summary_json, indent=2)}")

            # Log token usage
            self.total_input_tokens += total_input_tokens
            self.total_output_tokens += total_output_tokens
            self.log_usage(self.total_input_tokens, self.total_output_tokens)

            return summary_json

        except json.JSONDecodeError as e:
            error_message = f"Failed to decode JSON: {e}"
            logger.error(error_message)
            return {"error": error_message}

        except Exception as e:
            error_message = f"An error occurred during the summarization process: {str(e)}"
            logger.error(error_message)
            return {"error": error_message}

    def create_fhir_composition(self, summary_data: dict, patient_id: str) -> dict:
        """Creates a FHIR Composition resource based on the summary data."""
        # Get current time in ISO 8601 format
        now = datetime.datetime.now(pytz.utc)
        timestamp = now.isoformat()

        # Ensure timezone offset includes colon (e.g., "+00:00")
        if timestamp.endswith('+0000'):
            timestamp = timestamp[:-5] + '+00:00'

        # Generate a unique ID for the Composition
        resource_id = str(uuid.uuid4())

        # Build the Composition resource
        composition = {
            "resourceType": "Composition",
            "id": resource_id,
            "status": summary_data.get("status", "final"),
            "type": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "34133-9",
                        "display": "Summary of episode note"
                    }
                ],
                "text": "Summary of episode note"
            },
            "subject": {
                "reference": f"Patient/{patient_id}"
            },
            "date": timestamp,
            "title": summary_data.get("title", "Medical Summary"),
            "author": [
                {
                    "reference": "Practitioner/unknown",
                    "display": "Unknown Practitioner"
                }
            ],
            "section": []
        }

        # Add sections for medical status, medications, treatment plan, and recommendations
        medical_status = summary_data.get("PatientSummary", {}).get("MedicalStatus", {})
        medications = summary_data.get("PatientSummary", {}).get("Medications", [])
        treatment_plan = summary_data.get("PatientSummary", {}).get("TreatmentPlan", [])
        recommendations = summary_data.get("PatientSummary", {}).get("Recommendations", "")

        if medical_status:
            composition["section"].append({
                "title": "Medical Status",
                "text": {
                    "status": "generated",
                    "div": f"<div xmlns='http://www.w3.org/1999/xhtml'><p>{json.dumps(medical_status)}</p></div>"
                }
            })

        if medications:
            composition["section"].append({
                "title": "Medications",
                "text": {
                    "status": "generated",
                    "div": f"<div xmlns='http://www.w3.org/1999/xhtml'><p>{', '.join(medications)}</p></div>"
                }
            })

        if treatment_plan:
            composition["section"].append({
                "title": "Treatment Plan",
                "text": {
                    "status": "generated",
                    "div": f"<div xmlns='http://www.w3.org/1999/xhtml'><p>{', '.join(treatment_plan)}</p></div>"
                }
            })

        if recommendations:
            composition["section"].append({
                "title": "Recommendations",
                "text": {
                    "status": "generated",
                    "div": f"<div xmlns='http://www.w3.org/1999/xhtml'><p>{recommendations}</p></div>"
                }
            })

        # Add narrative text for the entire Composition
        composition["text"] = {
            "status": "generated",
            "div": "<div xmlns='http://www.w3.org/1999/xhtml'><p>Medical summary document.</p></div>"
        }

        return composition


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
