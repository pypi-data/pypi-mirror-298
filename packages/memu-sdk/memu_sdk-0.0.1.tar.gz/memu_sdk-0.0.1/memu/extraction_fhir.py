import json
import logging
import requests
import uuid
import datetime
import pytz
from openai import OpenAI

logger = logging.getLogger(__name__)

class MedicalEntityExtractorFHIR:
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

    def extract_medical_entities(self, transcript, medical_records, patient_id):
        """Extract medical entities and return a FHIR-compliant bundle."""
        minimum_required_balance = 10.00
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
        logger.info(f"Current balance before operation: ${current_balance}")
        
        if current_balance < minimum_required_balance:
            raise ValueError(f"Insufficient balance. A minimum balance of ${minimum_required_balance} is required to proceed. Current balance: ${current_balance}.")

        logger.info("Starting FHIR-compliant medical entity extraction...")

        combined_input = {
            "Transcript": transcript,
            "MedicalRecords": medical_records
        }

        entities_format_example = {
            "MedicalEntities": {
                "Medications": ["Lisinopril", "Metformin"],
                "Procedures": ["Procedure 1", "Procedure 2"],
                "Diseases": ["Hypertension", "Diabetes"],
                "Diagnoses": ["Diagnosis 1", "Diagnosis 2"]
            }
        }

        try:
            # Call to the OpenAI model
            response = self.client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a medical assistant. Extract and list all medical entity names in FHIR Observation format using this template: {json.dumps(entities_format_example, indent=2)}."
                    },
                    {
                        "role": "user",
                        "content": f"Extract medical entities based on this data: {json.dumps(combined_input, indent=2)}"
                    }
                ],
                temperature=0
            )

            # Capture and clean the output from the model
            structured_output = response.choices[0].message.content.strip().strip('```json').strip()
            total_input_tokens = response.usage.prompt_tokens
            total_output_tokens = response.usage.completion_tokens

            # Parse the structured output
            extracted_entities = json.loads(structured_output)
            logger.info(f"Extracted medical entities: {json.dumps(extracted_entities, indent=2)}")

            # Convert extracted entities into a FHIR bundle
            fhir_bundle = self.create_fhir_bundle(extracted_entities, patient_id)

            # Log usage
            self.log_usage(total_input_tokens, total_output_tokens)

            return fhir_bundle, "Extraction successful"

        except json.JSONDecodeError as e:
            error_message = f"Failed to decode JSON: {e}"
            logger.error(error_message)
            return {"error": error_message}, error_message

        except Exception as e:
            error_message = f"An error occurred during the medical entity extraction process: {str(e)}"
            logger.error(error_message)
            return {"error": error_message}, error_message

    def create_fhir_bundle(self, entities, patient_id):
        """Create a FHIR Bundle from the extracted medical entities."""
        logger.info(f"Creating FHIR bundle for patient {patient_id}...")

        now = datetime.datetime.now(pytz.utc)
        timestamp = now.isoformat()

        if timestamp.endswith('+0000'):
            timestamp = timestamp[:-5] + '+00:00'

        fhir_bundle = {
            "resourceType": "Bundle",
            "type": "collection",
            "entry": []
        }

        # Create FHIR resources for Medications
        for medication in entities.get("MedicalEntities", {}).get("Medications", []):
            try:
                rxcui = self.get_rxcui_by_string(medication)
            except ValueError:
                rxcui = "Unknown"  # Fallback if RXCUI not found or failed to fetch

            resource_id = str(uuid.uuid4())
            medication_statement = {
                "fullUrl": f"urn:uuid:{resource_id}",
                "resource": {
                    "resourceType": "MedicationStatement",
                    "id": resource_id,
                    "text": {
                        "status": "generated",
                        "div": f"<div xmlns='http://www.w3.org/1999/xhtml'>Medication Statement for {medication}</div>"
                    },
                    "status": "recorded",  # Ensure valid status from FHIR ValueSet
                    "medication": {
                        "concept": {
                            "coding": [
                                {
                                    "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                                    "code": rxcui,
                                    "display": medication
                                }
                            ]
                        }
                    },
                    "subject": {
                        "reference": f"Patient/{patient_id}"
                    },
                    "effectiveDateTime": timestamp
                }
            }
            logger.info(f"Adding medication to FHIR bundle: {medication} (RXCUI: {rxcui})")
            fhir_bundle["entry"].append(medication_statement)

        # Create FHIR resources for Procedures
        for procedure_name in entities.get("MedicalEntities", {}).get("Procedures", []):
            resource_id = str(uuid.uuid4())
            procedure = {
                "fullUrl": f"urn:uuid:{resource_id}",
                "resource": {
                    "resourceType": "Procedure",
                    "id": resource_id,
                    "text": {
                        "status": "generated",
                        "div": f"<div xmlns='http://www.w3.org/1999/xhtml'>Procedure performed: {procedure_name}</div>"
                    },
                    "status": "completed",
                    "code": {
                        "text": procedure_name
                    },
                    "subject": {
                        "reference": f"Patient/{patient_id}"
                    },
                    "performedDateTime": timestamp
                }
            }
            logger.info(f"Adding procedure to FHIR bundle: {procedure_name}")
            fhir_bundle["entry"].append(procedure)

        # Create FHIR resources for Diseases and Diagnoses as Conditions
        for condition_name in entities.get("MedicalEntities", {}).get("Diseases", []) + entities.get("MedicalEntities", {}).get("Diagnoses", []):
            resource_id = str(uuid.uuid4())
            condition = {
                "fullUrl": f"urn:uuid:{resource_id}",
                "resource": {
                    "resourceType": "Condition",
                    "id": resource_id,
                    "text": {
                        "status": "generated",
                        "div": f"<div xmlns='http://www.w3.org/1999/xhtml'>Condition diagnosed: {condition_name}</div>"
                    },
                    "clinicalStatus": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                                "code": "active"
                            }
                        ]
                    },
                    "verificationStatus": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                                "code": "confirmed"
                            }
                        ]
                    },
                    "code": {
                        "text": condition_name
                    },
                    "subject": {
                        "reference": f"Patient/{patient_id}"
                    },
                    "onsetDateTime": timestamp
                }
            }
            logger.info(f"Adding condition to FHIR bundle: {condition_name}")
            fhir_bundle["entry"].append(condition)

        logger.info(f"FHIR bundle created with {len(fhir_bundle['entry'])} entries")
        return fhir_bundle

    def get_rxcui_by_string(self, drug_name: str) -> str:
        """Finds the RXCUI for a given drug name."""
        logger.info(f"Fetching RXCUI for: {drug_name}")
        response = requests.get(f"https://rxnav.nlm.nih.gov/REST/rxcui.json?name={drug_name}")
        
        if response.status_code != 200:
            logger.error(f"Failed to fetch RXCUI for {drug_name}: {response.text}")
            raise ValueError(f"Failed to fetch RXCUI for {drug_name}")

        try:
            rxcui_data = response.json()
            rxcui = rxcui_data["idGroup"].get("rxnormId", [None])[0]
            if not rxcui:
                raise ValueError(f"RXCUI not found for {drug_name}")
            logger.info(f"RXCUI found for {drug_name}: {rxcui}")
            return rxcui
        except ValueError:
            logger.error(f"Failed to decode JSON from the response: {response.text}")
            raise ValueError("Failed to decode JSON from the response")

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

