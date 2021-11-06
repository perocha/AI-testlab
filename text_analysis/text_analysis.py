'''
Example of using Azure Cognitive Services Text Analysis.
From a given text, it obtains:
    - language
    - sentiment
    - entities
    - links
The credentials are stored in Azure Key Vault.
'''
import os
from dotenv import load_dotenv

# Import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential

def get_key_from_keyvault():
    ''' Get key from keyvault'''
    try:
        # Get Configuration Settings
        key_vault_name = os.getenv('KEY_VAULT')
        app_tenant = os.getenv('TENANT_ID')
        app_id = os.getenv('APP_ID')
        app_password = os.getenv('APP_PASSWORD')

        # Get cognitive services key from keyvault using the service principal credentials
        key_vault_uri = f"https://{key_vault_name}.vault.azure.net/"
        credential = ClientSecretCredential(app_tenant, app_id, app_password)
        keyvault_client = SecretClient(key_vault_uri, credential)
        secret_key = keyvault_client.get_secret("Cognitive-Services-Key")
        cog_key = secret_key.value

        credential = AzureKeyCredential(cog_key)

        return credential

    except Exception as ex:
        print(f"get_key_from_keyvault:Exception: {ex}")
        return None


def main():
    ''' Main function'''
    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')

        # Get credentials from Azure Key Vault
        credential = get_key_from_keyvault()

        # Create client using endpoint and key
        cog_client = TextAnalyticsClient(endpoint=cog_endpoint, credential=credential)

        # Analyze each text file in the reviews folder
        reviews_folder = 'example_text'
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print(f"\n---------------------------\nFilename: {file_name}")
            with open(os.path.join(reviews_folder, file_name), encoding='utf8') as file_handle:
                text = file_handle.read()
                print(f"\n{text}")

            # Get language
            detected_language = cog_client.detect_language(documents=[text])[0]
            print(f"\nLanguage: {detected_language.primary_language.name}")

            # Get sentiment
            sentiment_analysis = cog_client.analyze_sentiment(documents=[text])[0]
            print(f"\nSentiment: {sentiment_analysis.sentiment}")

            # Get key phrases
            phrases = cog_client.extract_key_phrases(documents=[text])[0].key_phrases
            if len(phrases) > 0:
                print(f"\nKey Phrases ({len(phrases)})")
                for phrase in phrases:
                    print(f"\t{phrase}")

            # Get entities
            entities = cog_client.recognize_entities(documents=[text])[0].entities
            if len(entities) > 0:
                print(f"\nEntities ({len(entities)})")
                for entity in entities:
                    print(f"\t{entity.text} ({entity.category})")

            # Get linked entities
            entities = cog_client.recognize_linked_entities(documents=[text])[0].entities
            if len(entities) > 0:
                print(f"\nLinks ({len(entities)})")
                for linked_entity in entities:
                    print(f"\t{linked_entity.name} ({linked_entity.url})")

    except Exception as ex:
        print(f"Exception: {ex}")


if __name__ == "__main__":
    main()
