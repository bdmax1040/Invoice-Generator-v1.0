import os
import json
from pathlib import Path

# Platform-safe config directory (recommended for deployed apps)
def get_config_dir():
    if os.name == 'nt':
        return Path(os.getenv('APPDATA')) / "InvoiceGenerator"
    elif os.name == 'posix':
        return Path.home() / ".config" / "InvoiceGenerator"
    else:
        return Path.home() / ".invoice_generator"

CONFIG_DIR = get_config_dir()
CONFIG_PATH = CONFIG_DIR / "config.json"
ENV_PATH = CONFIG_DIR / ".env"

DEFAULT_CONFIG = {
    "setup": {
    "completed": False
    },
    "user_info": {
        "full_name": "",
        "company_name": "",
        "email_address": ""
    },
    "banking": {
        "account_name": "",
        "sort_code": "",
        "account_number": "",
        "currency": "£"
    },
    "mileage": {
        "vehicle_mpg": "",
        "fuel_price": "",
        "default_45p_per_mile": False
    },
    "preferences": {
        "due_date_offset_days": 14,
        "my_email_bcc": True,
        "company_name_in_signature": True
    },
    "pdf": {
        "save_location": ""
    },
    "theme": {
        "accent": "#FF3E3E"
    }
}

DEFAULT_ENV_VARS = {
    "PDF_API_KEY": "",
    "GOOGLE_SMTP_PASSWORD": ""
}


def ensure_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not CONFIG_PATH.exists():
        with open(CONFIG_PATH, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        print(f"[✓] Created config.json at {CONFIG_PATH}")

    if not ENV_PATH.exists():
        with open(ENV_PATH, "w") as f:
            for key, value in DEFAULT_ENV_VARS.items():
                f.write(f"{key}={value}\n")
        print(f"[✓] Created .env at {ENV_PATH}")


def load_config():
    ensure_config()
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(data: dict):
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)


def get_env():
    ensure_config()
    env_vars = {}
    if ENV_PATH.exists():
        with open(ENV_PATH, "r") as f:
            for line in f:
                if line.strip() and "=" in line:
                    key, val = line.strip().split("=", 1)
                    env_vars[key] = val
    return env_vars


if __name__ == "__main__":
    ensure_config()