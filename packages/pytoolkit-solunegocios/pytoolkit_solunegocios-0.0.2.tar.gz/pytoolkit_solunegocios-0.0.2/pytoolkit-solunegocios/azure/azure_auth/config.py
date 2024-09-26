# config.py
class AuthConfig:
    def __init__(self, client_id, client_secret, tenant_id, redirect_uri, scopes=None):
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.TENANT_ID = tenant_id
        self.AUTHORITY = f"https://login.microsoftonline.com/{self.TENANT_ID}"
        self.REDIRECT_URI = redirect_uri
        self.SCOPE = scopes if scopes else ["User.Read"]  # Permitir definir otros scopes
