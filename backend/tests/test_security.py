import jwt
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings

def test_password_hashing():
    raw_password = "SuperSecretPassword123!"
    hashed = get_password_hash(raw_password)
    
    assert hashed != raw_password
    assert verify_password(raw_password, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_token_creation_and_decoding():
    email = "admin@diia.gov.ua"
    token = create_access_token(data={"sub": email})
    
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload.get("sub") == email
    assert "exp" in payload