import pytest
class Password():
    def __init__(self,password):
        self.password = password

    def validate_password(self):
        special_char = "!@#$%^&*"
        if " " in self.password:
            raise ValueError("Password must not contain space")
        if len(self.password) <8:
            raise ValueError("Password must not be less than 8 characters")
        if not any(char.isdigit() for char in self.password):
            raise ValueError("Password must contain an integer")
        if not any(char.isupper() for char in self.password):
            raise(ValueError("Password must contain uppercase letters"))
        if not any (char in special_char for char in self.password):
            raise(ValueError("Password must contain special characters"))
        return self.password

@pytest.fixture()
def haslo(request):
    password = request.param
    return Password(password)

@pytest.mark.parametrize("haslo,expected,expected_error",[
    (" ", ValueError, "Password must not contain space"),
    ("p olska1", ValueError, "Password must not contain space"),
    (" p olska1", ValueError, "Password must not contain space"),
    (" p olska123456!@", ValueError, "Password must not contain space"),
],indirect=["haslo"])


def test_validate_password(haslo,expected,expected_error):
    with pytest.raises(expected,match=expected_error):
        haslo.validate_password()

@pytest.mark.parametrize("haslo, expected, expected_error",[
    ("polskah", ValueError,"Password must not be less than 8 characters"),
    ("p", ValueError,"Password must not be less than 8 characters"),
    ("polskad", ValueError,"Password must not be less than 8 characters"),
    ("p!1P", ValueError,"Password must not be less than 8 characters"),
],indirect=["haslo"])

def test_validate_password_len(haslo, expected,expected_error):
    with pytest.raises(expected,match=expected_error):
        haslo.validate_password()

@pytest.mark.parametrize("haslo, expected, expected_error",[
    ("Polska@#$", ValueError,"Password must contain an integer"),
    ("p!YYedhsdfP", ValueError,"Password must contain an integer"),
    ("polskAa^", ValueError,"Password must contain an integer"),
    ("p!fhdfhsGsdg", ValueError,"Password must contain an integer"),
],indirect=["haslo"])

def test_validate_password_intiger(haslo, expected,expected_error):
    with pytest.raises(expected,match=expected_error):
        haslo.validate_password()

@pytest.mark.parametrize("haslo, expected, expected_error",[
    ("p7olska@#$", ValueError,"Password must contain uppercase letters"),
    ("p!yyedhs7dfp", ValueError,"Password must contain uppercase letters"),
    ("polska5a^", ValueError,"Password must contain uppercase letters"),
    ("p!fhdf7shhsdg", ValueError,"Password must contain uppercase letters"),
],indirect=["haslo"])

def test_validate_password_upper(haslo, expected,expected_error):
    with pytest.raises(expected,match=expected_error):
        haslo.validate_password()

@pytest.mark.parametrize("haslo, expected, expected_error",[
    ("p7oijlSka", ValueError,"Password must contain special characters"),
    ("pyyeDhs7dfp", ValueError,"Password must contain special characters"),
    ("polSka5adsg", ValueError,"Password must contain special characters"),
    ("pfHdf7shhsdg", ValueError,"Password must contain special characters"),
],indirect=["haslo"])

def test_validate_password_spec_char(haslo, expected,expected_error):
    with pytest.raises(expected,match=expected_error):
        haslo.validate_password()

@pytest.mark.parametrize("haslo",[
    ("p7oi@jlSka"),
    ("pyyeDh!s7dfp"),
    ("polSk@a5adsg"),
    ("pfHdf7s%hhsdg"),
],indirect=["haslo"])

def test_validate_password_accept(haslo):
    assert haslo.validate_password() == haslo.password