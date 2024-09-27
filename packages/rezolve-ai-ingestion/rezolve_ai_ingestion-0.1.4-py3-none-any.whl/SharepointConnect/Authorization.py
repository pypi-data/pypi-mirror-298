from typing import Dict
import msal
import requests

class Certificate:
    def __init__(self, client_auth):
        self.azure_tid = client_auth.azure_tid
        self.client_id = client_auth.client_id
        self.thumbprint = client_auth.thumbprint
        self.private_key = client_auth.key
    
    def Graph(self) -> Dict[str, str]:
        # print("Class Certificate Function Graph")
        app = msal.application.ConfidentialClientApplication(
            authority=f"https://login.microsoftonline.com/{self.azure_tid}",
            client_id=self.client_id,
            client_credential={"thumbprint": self.thumbprint, "private_key": self.private_key},
        )
        
        response = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        token = response.get("access_token")

        if not token:
            raise Exception(f"Error obtaining token for Graph API: {response.get('error_description')}")
        
        return {"Authorization": f"Bearer {token}"}

    def Sharepoint(self) -> Dict[str, str]:
        # print("Class Certificate Function Sharepoint")
        app = msal.application.ConfidentialClientApplication(
            authority=f"https://login.microsoftonline.com/{self.azure_tid}",
            client_id=self.client_id,
            client_credential={"thumbprint": self.thumbprint, "private_key": self.private_key},
        )

        response = app.acquire_token_for_client(scopes=[f"https://{self.sharepoint_prefix}.sharepoint.com/.default"])
        token = response.get("access_token")

        if not token:
            raise Exception(f"Error obtaining token for Graph API: {response.get('error_description')}")

        return {"Authorization": f"Bearer {token}"}

class Secret:
    def __init__(self, client_auth):
        self.azure_tid = client_auth.azure_tid
        self.client_id = client_auth.client_id
        self.client_secret = client_auth.client_secret
        self.prefix = client_auth.sharepoint_prefix

    def Graph(self) -> Dict[str, str]:
        # print("Class Secret Function Graph")
        app = msal.ConfidentialClientApplication(
            authority=f"https://login.microsoftonline.com/{self.azure_tid}",
            client_id=self.client_id,
            client_credential=self.client_secret,
        )
        
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        graph_token = result.get("access_token")

        if not graph_token:
            raise Exception(f"Error obtaining token for Graph API: {result.get('error_description')}")
        
        return {"Authorization": f"Bearer {graph_token}"}



    def Sharepoint(self) -> Dict[str, str]:
        # print("Class Secret Function Sharepoint")
        app = msal.ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=f"https://login.microsoftonline.com/{self.azure_tid}"
        )

        result = app.acquire_token_for_client(scopes=[f"https://{self.sharepoint_prefix}.sharepoint.com/.default"])
        access_token = result.get("access_token")

        if not access_token:
            raise Exception(result.get("error_description"))

        return {"Authorization": f"Bearer {access_token}"}
    
def Authorize(authorization):
    # print("Class Authorization Function Sharepoint")
    try:
        if authorization.client_secret is not None:
            auth = Secret(authorization)
            if authorization.sharepoint_auth:
                return auth.Sharepoint()
            return auth.Graph()
        if authorization.key is not None:
            auth = Certificate(authorization)
            if authorization.sharepoint_auth:
                return auth.Sharepoint()
            return auth.Graph()
    except:
        if authorization.key is not None:
            auth = Certificate(authorization)
            if authorization.sharepoint_auth:
                return auth.Sharepoint()
            return auth.Graph()
        if authorization.client_secret is not None:
            auth = Secret(authorization)
            if authorization.sharepoint_auth:
                return auth.Sharepoint()
            return auth.Graph()

class AuthenticateCherwell:
    def __init__(self, authorization):
        self.client_id = authorization.client_id
        self.username = authorization.username
        self.password = authorization.password
        self.grant_type = authorization.grant_type
        self.token_url = authorization.token_url

    def Token(self) -> Dict[str, str]:
        token_request_body = {
            "Accept": "application/json",
            "grant_type": self.grant_type,
            "client_id": self.client_id,
            "username": self.username,
            "password": self.password,
        }
        
        result = requests.post(self.token_url, data=token_request_body)
        token = result.json().get("access_token")

        if not token:
            raise Exception(f"Error obtaining token for Cherwell API.")
        
        return {
            'Authorization': f'Bearer {token}',
            "Accept": "application/json",
        }