import requests

def convert_usd_to_bdt(usd_amount):
    url = f"https://open.er-api.com/v6/latest/USD"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("result") != "success":
            print("API returned error:", data)
            return None

        rates = data.get("rates")
        if not rates or "BDT" not in rates:
            print("BDT rate not found in API response.")
            return None

        bdt_rate = rates["BDT"]
        bdt = bdt_rate * usd_amount
        return bdt, bdt_rate

    except requests.RequestException as e:
        print("Network error:", e)
        return None
    except Exception as e:
        print("Unexpected error:", e)
        return None
