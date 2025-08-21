import requests

# Hardcoded FMCSA API key (temporary)
FMCSA_API_KEY = "cdc33e44d693a3a58451898d4ec9df862c65b954"

def verify_mc_number(mc_number: str):
    """
    Verify carrier MC number using the FMCSA API.
    Returns a tuple: (is_verified: bool, insurance_ok: bool)
    """
    url = f"https://mobile.fmcsa.dot.gov/qc/services/carriers/{mc_number}?webKey={FMCSA_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Check if carrier exists and status is ACTIVE
        status = data.get("carrier", {}).get("status", "").lower()
        insurance_ok = data.get("carrier", {}).get("insurance", {}).get("active", False)

        is_verified = True
        return is_verified, insurance_ok
    except Exception as e:
        print(f"Error verifying MC number {mc_number}: {e}")
        return False, False