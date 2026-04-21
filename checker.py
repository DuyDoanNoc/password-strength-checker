# Password Strength Checker.
import csv

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


def check_password(password):
    checks = [
            ("Length >= 8",     check_length),
            ("Uppercase",       check_uppercase),
            ("Lowercase",       check_lowercase),
            ("Digit",           check_digit),
            ("Special",         check_special),
            ("CommonPattern",   check_common_patterns),
            ("Whitespace",      check_whitespace)
            ]

    details = []
    score = 0

    for name, func in checks:
        passed, message = func(password)
        details.append({
            "check": name,
            "passed": passed,
            "message": message
            })
        if passed:
            score += 1
    return {
        "password": password,
        "score": score,
        "max_score": len(checks),
        "strength": get_strength_label(score),
        "details": details
    }

def print_report(result):
    password = result["password"]
    masked = password[:3] + "*" * (len(password) - 3) if len(password) > 3 else "***"
    details = result["details"]
    print(f"{'=' * 50}")
    print(f"Password: {masked}")
    print(f"Score: {result['score']}/{result['max_score']}")
    print(f"Strength: {result['strength']}")
    print(f"{'-' * 50}")
    for detail in details:
        icon = "✅" if detail["passed"] else "❌"
        print(f"{icon} {detail['check']:<20} {detail['message']}")
    print(f"{'=' * 50}")

def read_passwords(filepath):
    password = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    password.append(line.strip())
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    return password

def write_results(results, filepath):
    fieldnames = ["password", "score", "strength",
                  "length", "uppercase", "lowercase",
                  "digit", "special", "common_pattern", "whitespace"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        check_keys = ["length", "uppercase", "lowercase",
              "digit", "special", "common_pattern", "whitespace"]
        
        for result in results:
            pw = result["password"]
            masked = pw[:3] + "*" * (len(pw) - 3) if len(pw) > 3 else "***"
            row = {
                "password": masked,
                "score": result["score"],
                "strength": result["strength"]
            }
            
            for key, detail in zip(check_keys, result["details"]):
                row[key] = "PASS" if detail["passed"] else "FAIL"
            writer.writerow(row)

    print(f"Results written to: {filepath}")
                

if __name__ == "__main__":
    passwords = read_passwords("passwords.txt")
    print(f"Read {len(passwords)} passwords")
    
    results = []
    for pw in passwords:
        result = check_password(pw)
        print_report(result)
        results.append(result)
    
    write_results(results, "results.csv")