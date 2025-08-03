import requests

def fetch_exchange_rates(base="USD", symbols=["BDT"]):
    url = f"https://open.er-api.com/v6/latest/{base}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("result") != "success":
            print("API returned error:", data)
            return

        rates = data.get("rates")
        if not rates:
            print("Unexpected API response structure:", data)
            return

        print(f"Exchange rates (base {base}):")
        for currency in symbols:
            rate = rates.get(currency)
            if rate:
                print(f"{currency}: {rate}")
            else:
                print(f"{currency} rate not found")

        balance_usd = 10
        bdt_rate = rates.get("BDT")
        if bdt_rate:
            balance_bdt = balance_usd * bdt_rate
            print(f"\n{balance_usd} USD is equal to {balance_bdt:.2f} BDT")
        else:
            print("BDT rate not found.")

    except requests.RequestException as e:
        print("Network error:", e)
    except Exception as e:
        print("Unexpected error:", e)


if __name__ == "__main__":
    fetch_exchange_rates()
