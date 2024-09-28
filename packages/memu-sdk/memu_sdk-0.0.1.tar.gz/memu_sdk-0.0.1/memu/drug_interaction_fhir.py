import json
import logging
import requests
import uuid
import datetime
import pytz
from openai import OpenAI

logger = logging.getLogger(__name__)

class DrugInteractionCheckerFHIR:
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

    def check_drug_interactions(self, rxcui_map: dict) -> list:
        """Checks for drug interactions between multiple medications."""
        logger.info(f"Checking drug interactions for RXCUI map: {rxcui_map}")
        drug_interactions = []
        medications = list(rxcui_map.keys())

        # Pairwise check for interactions
        for i in range(len(medications)):
            for j in range(i + 1, len(medications)):
                drug1 = medications[i]
                drug2 = medications[j]
                rxcui1 = rxcui_map[drug1]
                rxcui2 = rxcui_map[drug2]

                url = f"https://rxnav.nlm.nih.gov/REST/interaction/interaction.json?rxcuis={rxcui1}+{rxcui2}"
                response = requests.get(url)

                if response.status_code == 404:
                    logger.info(f"No known interactions found between {drug1} and {drug2}.")
                    interactions = ["No relevant interactions"]
                elif response.status_code != 200:
                    logger.error(f"API call failed with status code {response.status_code}: {response.text}")
                    raise ValueError(f"API call failed with status code {response.status_code}")
                else:
                    interaction_data = response.json()
                    interactions = [
                        pair["description"]
                        for group in interaction_data.get("interactionTypeGroup", [])
                        for type in group.get("interactionType", [])
                        for pair in type.get("interactionPair", [])
                    ] or ["No relevant interactions"]

                # Add interaction data to the list
                drug_interactions.append({
                    "drug1": drug1,
                    "rxcui1": rxcui1,
                    "drug2": drug2,
                    "rxcui2": rxcui2,
                    "interactions": interactions
                })

        return drug_interactions

    def validate_and_correct_interactions(self, drug_interactions: list) -> dict:
        """Validates and corrects drug interactions using GPT-4 with few-shot learning examples."""
        try:
            corrected_interactions = {"interactions": []}

            # Template with examples for few-shot training
            few_shot_examples = [
                {
                    "drug1": "Metformin",
                    "rxcui1": "6809",
                    "drug2": "Lisinopril",
                    "rxcui2": "29046",
                    "interactions": ["May increase the hypoglycemic activities of Lisinopril."]
                },
                {
                    "drug1": "Metformin",
                    "rxcui1": "6809",
                    "drug2": "Furosemide",
                    "rxcui2": "4603",
                    "interactions": ["May enhance the nephrotoxic effect of Furosemide."]
                },
                {
                    "drug1": "Metformin",
                    "rxcui1": "6809",
                    "drug2": "Potassium Chloride",
                    "rxcui2": "8591",
                    "interactions": ["May enhance the hyperkalemic effect of Potassium Chloride."]
                },
                {
                    "drug1": "Lisinopril",
                    "rxcui1": "29046",
                    "drug2": "Furosemide",
                    "rxcui2": "4603",
                    "interactions": ["May enhance the hypotensive effect of Furosemide."]
                },
                {
                    "drug1": "Lisinopril",
                    "rxcui1": "29046",
                    "drug2": "Potassium Chloride",
                    "rxcui2": "8591",
                    "interactions": ["May enhance the hyperkalemic effect of Potassium Chloride."]
                },
                {
                    "drug1": "Furosemide",
                    "rxcui1": "4603",
                    "drug2": "Potassium Chloride",
                    "rxcui2": "8591",
                    "interactions": ["May enhance the hyperkalemic effect of Potassium Chloride."]
                }
            ]

            # Loop through each drug pair and send them to GPT-4 for validation
            for interaction in drug_interactions:
                combined_input = json.dumps([interaction], indent=2)
                logger.info(f"Sending the following data to GPT-4 for validation: {combined_input}")

                # Use GPT-4 to validate and correct each interaction with the few-shot examples
                response = self.client.chat.completions.create(
                    model="gpt-4o-2024-08-06",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an AI that validates and corrects drug interaction data. "
                                "Respond with corrected drug interaction data in JSON format. "
                                "Here are some examples of how to format the response: "
                                f"{json.dumps(few_shot_examples, indent=2)}"
                            )
                        },
                        {
                            "role": "user",
                            "content": f"Here is the interaction data for validation: {combined_input}. Please return corrected data for this pair, ensuring the structure is the same as the provided examples. Don't just return the interaction but return the full object that includes the drug names, RXCUIs, and interactions."
                        }
                    ],
                    temperature=0,
                    response_format={"type": "json_object"}  # Ensure the response is JSON
                )

                # Capture token usage from the response
                total_input_tokens = response.usage.prompt_tokens
                total_output_tokens = response.usage.completion_tokens
                logger.info(f"Token usage for this call - Input: {total_input_tokens}, Output: {total_output_tokens}")

                # Update the total token usage
                self.total_input_tokens += total_input_tokens
                self.total_output_tokens += total_output_tokens

                corrected_output = response.choices[0].message.content.strip()
                logger.info(f"Raw output from GPT-4: {corrected_output}")

                # Parse the JSON response for each interaction
                try:
                    single_corrected_interaction = json.loads(corrected_output)
                    corrected_interactions["interactions"].append(single_corrected_interaction)  # Fixing the append issue
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to decode JSON: {e}")
                    logger.error(f"Invalid JSON content: {corrected_output}")
                    corrected_interactions["interactions"].append(interaction)  # If validation fails, use the original data

            logger.info(f"Final corrected interactions: {json.dumps(corrected_interactions, indent=2)}")

            # Log the total token usage after all interactions are processed
            self.log_usage(self.total_input_tokens, self.total_output_tokens)

            return corrected_interactions

        except Exception as e:
            logger.error(f"An error occurred during the validation process: {str(e)}")
            return {"interactions": drug_interactions}  # Return the original data if validation fails

    def create_fhir_detected_issues(self, interactions_list: list, patient_id: str) -> dict:
        """Creates a FHIR Bundle containing DetectedIssue resources for the drug interactions."""
        # Get current time in ISO 8601 format
        now = datetime.datetime.now(pytz.utc)
        timestamp = now.isoformat()

        # Ensure timezone offset includes colon (e.g., "+00:00")
        if timestamp.endswith('+0000'):
            timestamp = timestamp[:-5] + '+00:00'

        # Create a FHIR Bundle resource
        fhir_bundle = {
            "resourceType": "Bundle",
            "type": "collection",
            "entry": []
        }

        for interaction in interactions_list:
            resource_id = str(uuid.uuid4())

            # Ensure the interaction description is not empty
            interaction_detail = interaction.get('interactions', ["No interaction information available."])
            if not isinstance(interaction_detail, list) or not interaction_detail[0]:
                interaction_detail = ["No interaction information available."]

            # Build the DetectedIssue resource
            detected_issue = {
                "fullUrl": f"urn:uuid:{resource_id}",
                "resource": {
                    "resourceType": "DetectedIssue",
                    "id": resource_id,
                    "status": "final",
                    "code": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                                "code": "DRG",
                                "display": "Drug Interaction Alert"
                            }
                        ],
                        "text": "Drug Interaction Alert"
                    },
                    "severity": "high",  # Adjust severity based on the interaction if available
                    "subject": {  # Corrected from 'patient' to 'subject'
                        "reference": f"Patient/{patient_id}"
                    },
                    "identifiedDateTime": timestamp,
                    "implicated": [
                        {
                            "reference": f"Medication/{interaction['rxcui1']}",
                            "display": interaction['drug1']
                        },
                        {
                            "reference": f"Medication/{interaction['rxcui2']}",
                            "display": interaction['drug2']
                        }
                    ],
                    "detail": interaction_detail[0]  # Use the first interaction description
                }
            }

            # Add narrative text to the DetectedIssue resource for human-readable display
            detected_issue["resource"]["text"] = {
                "status": "generated",
                "div": f"<div xmlns='http://www.w3.org/1999/xhtml'>Detected interaction between {interaction['drug1']} and {interaction['drug2']}: {detected_issue['resource']['detail']}</div>"
            }

            # Add the DetectedIssue resource to the bundle
            fhir_bundle["entry"].append(detected_issue)

        # Add meta to the FHIR Bundle
        fhir_bundle["meta"] = {
            "versionId": "1",
            "lastUpdated": timestamp
        }

        return fhir_bundle

    def orchestrate_interaction_check_fhir(self, medication_list: list, patient_id: str) -> dict:
        """Orchestrates the interaction check and returns a FHIR-compliant bundle of DetectedIssue resources."""
        logger.info(f"Starting FHIR-compliant interaction check for medications: {medication_list}")
        
        minimum_required_balance = 10.00
        current_balance = self.make_request("GET", "/balance", params={"api_key": self.memu_api_key}).get("balance")
        logger.info(f"Current balance before operation: ${current_balance}")
        
        if current_balance < minimum_required_balance:
            raise ValueError(f"Insufficient balance. A minimum balance of ${minimum_required_balance} is required to proceed. Current balance: ${current_balance}.")

        # Get the RXCUIs for the given medications
        rxcui_map = {}
        for medication in medication_list:
            try:
                rxcui = self.get_rxcui_by_string(medication)
                rxcui_map[medication] = rxcui
            except Exception as e:
                logger.error(f"Failed to fetch RXCUI for {medication}: {str(e)}")

        # Check for drug interactions
        drug_interactions = self.check_drug_interactions(rxcui_map)

        # Validate and correct the drug interactions
        corrected_interactions = self.validate_and_correct_interactions(drug_interactions)

        # Create the FHIR bundle of DetectedIssue resources
        fhir_bundle = self.create_fhir_detected_issues(corrected_interactions['interactions'], patient_id)

        logger.info(f"Completed FHIR-compliant interaction check with final FHIR bundle.")
        return fhir_bundle

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

