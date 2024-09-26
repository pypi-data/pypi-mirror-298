from msal import ConfidentialClientApplication
import requests

class AzureAuth:
    def __init__(self, client_id, client_secret, tenant_id, redirect_uri):
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.TENANT_ID = tenant_id
        self.AUTHORITY = f"https://login.microsoftonline.com/{self.TENANT_ID}"
        self.REDIRECT_URI = redirect_uri
        self.SCOPE = ["User.Read"]

        self.app = ConfidentialClientApplication(
            client_id=self.CLIENT_ID,
            client_credential=self.CLIENT_SECRET,
            authority=self.AUTHORITY
        )

    def acquire_token(self, authorization_code):
        """Intercambia el código de autorización por un token de acceso."""
        result = self.app.acquire_token_by_authorization_code(
            code=authorization_code,
            scopes=self.SCOPE,
            redirect_uri=self.REDIRECT_URI
        )
        if "access_token" in result:
            return result["access_token"]
        else:
            raise Exception(f"Error al obtener el token: {result.get('error_description', 'Error desconocido')}")

    def get_user_info(self, access_token):
        """Obtiene la información del usuario usando el token de acceso."""
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
        response.raise_for_status()
        return response.json()
