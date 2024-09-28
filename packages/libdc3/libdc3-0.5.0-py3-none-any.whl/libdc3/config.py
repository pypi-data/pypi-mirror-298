class Config:
    KEYTAB_USR = None
    KEYTAB_PWD = None
    AUTH_CERT = None
    AUTH_CERT_KEY = None

    def set_keytab_usr(self, value: str):
        self.KEYTAB_USR = value

    def set_keytab_pwd(self, value: str):
        self.KEYTAB_PWD = value

    def set_auth_cert_path(self, value: str):
        self.AUTH_CERT = value

    def set_auth_key_path(self, value: str):
        self.AUTH_CERT_KEY = value


dc3_config = Config()
