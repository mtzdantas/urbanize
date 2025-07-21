import bcrypt

def hash_password(password: str) -> str:
    """
    Gera um hash seguro da senha usando bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

# def verify_password(password: str, hashed_password: str) -> bool:
#     """
#     Verifica se a senha informada corresponde ao hash armazenado.
#     """
#     return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
