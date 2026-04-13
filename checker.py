# Password Strength Checker

# Hằng số
MIN_LENGTH = 8
SPECIAL_CHARACTERS = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
COMMON_PATTERNS = ["password", "123456", "qwerty", "admin", "letmein"]

# kiểm tra độ dài password >= 8:
def check_length(password):
    length = len(password)
    if length >= MIN_LENGTH:
        return True, f"Length OK ({length} chars)"
    return False, f"Length too short ({length} chars, need {MIN_LENGTH})"

# Có ít nhất 1 chữ hoa
def check_uppercase(password):
    passed = any(c.isupper() for c in password)
    if passed:
        return True, "Has uppercase letter"
    return False, "Missing uppercase letter"

# có ít nhất 1 chữ thường
def check_lowercase(password):
    passed = any(c.islower() for c in password)
    if passed:
        return True, "Has lowercase letter"
    return False, "Missing lowercase letter"


# có ít nhất 1 chữ số
def check_digit(password):
    passed = any(c.isdigit() for c in password)
    if passed:
        return True, "Has digit"
    return False, "Missing digit"

# có ít nhất 1 ký tự đặc biệt
def check_special(password):
    passed = any(c in SPECIAL_CHARACTERS for c in password)
    if passed:
        return True, "Has special character"
    return False, "Missing special character"

# Không chứa pattern phổ biến
def check_common_patterns(password):
    pw_lower = password.lower()
    for pattern in COMMON_PATTERNS:
        if pattern in pw_lower:
            return False, f"Contains common pattern: '{pattern}'"
    return True, "No common patterns found"
            
# Không chứa khoảng trắng
def check_whitespace(password):
    if " " not in password:
        return True, "No whitespace"
    return False, "Contains white space"

def get_strength_label(score):
    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    elif score <= 6:
        return "Strong"
    else:
        return "Very Strong"


if __name__ == "__main__":
    print("=== Test 1: Strong password ===")
    print(check_common_patterns("Abc123!@"))
    
    print("\n=== Test 2: Contains 'password' ===")
    print(check_common_patterns("mypassword123"))   # phải False
    
    print("\n=== Test 3: Contains 'qwerty' ===")
    print(check_common_patterns("qwerty2024"))      # phải False
    
    print("\n=== Test 4: Too short ===")
    print(check_length("abc"))                      # phải False
    
    print("\n=== Test 5: Has whitespace ===")
    print(check_whitespace("abc 123"))              # phải False