from datetime import datetime, timedelta, timezone
import jwt

from security.auth import (
    create_access_token,
    verify_token,
    SECRET_KEY,
    ALGORITHM
)

def test_valid_token():
    token = create_access_token({"sub": "testuser"})
    result = verify_token(token, expected_type="access")

    print("Valid token test:", result)
    assert result == "testuser"


def test_wrong_type():
    token = create_access_token({"sub": "testuser"})
    result = verify_token(token, expected_type="refresh")

    print("Wrong type test:", result)
    assert result is None


def test_expired_token():
    token = jwt.encode(
        {
            "sub": "testuser",
            "type": "access",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    result = verify_token(token, expected_type="access")

    print("Expired token test:", result)
    assert result is None


def test_invalid_signature():
    token = jwt.encode(
        {
            "sub": "testuser",
            "type": "access",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
        },
        "WRONG_SECRET",
        algorithm=ALGORITHM
    )

    result = verify_token(token, expected_type="access")

    print("Invalid signature test:", result)
    assert result is None


if __name__ == "__main__":
    test_valid_token()
    test_wrong_type()
    test_expired_token()
    test_invalid_signature()

    print("\nAll tests finished")