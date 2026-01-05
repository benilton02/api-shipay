"""Utilitários para manipulação de senhas"""

import hashlib


def hash_password(password: str) -> str:
    """
    Criptografa uma senha usando MD5.
    
    Nota: MD5 não é seguro para senhas em produção. Use apenas para casos específicos.
    
    Args:
        password: Senha em texto plano
        
    Returns:
        str: Hash MD5 da senha em hexadecimal
    """
    return hashlib.md5(password.encode('utf-8')).hexdigest()

