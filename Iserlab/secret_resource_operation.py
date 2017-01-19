#mcy update on 2016-12-07


#The Key Manager service allows you to create new secrets by passing
# the attributes of the Secret to the create_secret() method.
def create_secret(conn):
    print("Create a secret:")

    conn.key_manager.create_secret(name="My public key",
                                   secret_type="public",
                                   expiration="2020-02-28T23:59:59",
                                   payload="ssh rsa...",
                                   payload_content_type="text/plain")


#Once you have stored some secrets,
# they are available for you to list via the secrets() method.
# This method returns a generator, which yields each Secret.
def list_secrets(conn):
    print("List Secrets:")

    for secret in conn.key_manager.secrets():
        print(secret)


#The secrets() method can also make more advanced queries to limit the secrets that are returned.
def list_secrets_query(conn):
    print("List Secrets:")

    for secret in conn.key_manager.secrets(
            secret_type="symmetric",
            expiration="gte:2020-01-01T00:00:00"):
        print(secret)


#Once you have received a Secret, you can obtain the payload for it by
# passing the secret’s id value to the secrets() method.
# Use the secret_id attribute when making this request.
def get_secret_payload(conn):
    print("Get a secret's payload:")

    # Assuming you have an object `s` which you perhaps received from
    # a conn.key_manager.secrets() call...
    secret = conn.key_manager.get_secret(s.secret_id)
    print(secret.payload)