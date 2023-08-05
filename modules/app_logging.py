import logging
import sys
from azure.identity import DefaultAzureCredential
from azure.mgmt.web import WebSiteManagementClient

# Set up logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.StreamHandler(sys.stdout)])

# Function to get Managed Identity's client_id or object_id
def get_managed_identity_info(subscription_id, resource_group_name, app_service_name):
    try:
        credential = DefaultAzureCredential()
        web_client = WebSiteManagementClient(credential, subscription_id)
        app_service = web_client.web_apps.get(resource_group_name, app_service_name)
        managed_identity = app_service.identity
        return managed_identity.principal_id, managed_identity.tenant_id
    except Exception as e:
        logging.error(f"Failed to get Managed Identity info: {e}")
        return None, None