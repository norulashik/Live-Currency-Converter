import requests
import time

API_KEY = "07a5e4bcabcbbee17796ddb6"  # Replace with your free API key

def get_valid_currencies():
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/codes"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data['result'] == 'success':
            currencies = {code: name for code, name in data['supported_codes']}
            return currencies
        else:
            print("❌ Failed to fetch currency codes.")
            return {}
    except Exception as e:
        print("❌ Error fetching valid currencies:", e)
        return {}

def convert_currency(amount, from_currency, to_currency):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}/{amount}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code == 200 and data['result'] == 'success':
            converted = data['conversion_result']
            print(f"✅ {amount} {from_currency} = {converted:.2f} {to_currency}\n")
        else:
            print("❌ Conversion failed:", data.get("error-type", "Unknown error"))
    except Exception as e:
        print("❌ Error occurred:", e)

def start_live_converter():
    currencies = get_valid_currencies()
    if not currencies:
        print("❌ Cannot proceed without currency list.")
        return

    print("\n🌍 Supported Currency Codes:")
    for code, name in sorted(currencies.items()):
        print(f"{code} - {name}")
    print("\n🔁 Live Currency Converter (Press Ctrl+C to exit)\n")

    while True:
        try:
            amount = float(input("Enter amount: "))
            from_curr = input("From currency code (e.g., USD): ").strip().upper()
            to_curr = input("To currency code (e.g., INR): ").strip().upper()

            if from_curr not in currencies or to_curr not in currencies:
                print("❌ Invalid currency code. Please choose from the supported list.\n")
                continue

            convert_currency(amount, from_curr, to_curr)

            print("-" * 50)
            time.sleep(1)

        except KeyboardInterrupt:
            print("\n👋 Exiting live converter. Goodbye!")
            break
        except Exception as e:
            print("❌ Invalid input:", e)

# Start the program
start_live_converter()
