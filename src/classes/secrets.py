from google.cloud import secretmanager
import os

def access_secret(secret_id: str, version: str = "latest") -> str:
    """
    Access a secret from Google Secret Manager.

    Args:
        secret_id (str): ID of the secret in GSM.
        version (str): Version of the secret (default: "latest").
        project_id (str): GCP project ID. If None, uses default project.

    Returns:
        str: The secret payload as a string.
    """

    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    client = secretmanager.SecretManagerServiceClient()

    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
    response = client.access_secret_version(request={"name": name})

    # Decode secret from bytes to string
    secret_value = response.payload.data.decode("utf-8")
    return secret_value