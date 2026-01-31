import requests
import os

def get_ripple_nav():
    # 1. Fetch live XRP Price
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ripple&vs_currencies=usd"
    price = requests.get(url).json()['ripple']['usd']

    # 2. Ripple Constants (2026 Data)
    shares = 160_000_000
    locked_xrp = 34_200_000_000
    unlocked_xrp = 7_800_000_000
    acquisitions_cost = 4_250_000_000  # GTreasury, Hidden Road, etc.
    bid_price = 100

    # 3. XRP Calculations (XRP per share)
    locked_per_share = locked_xrp / shares
    unlocked_per_share = unlocked_xrp / shares
    total_xrp_per_share = (locked_xrp + unlocked_xrp) / shares
    
    # 4. Scenario Calculations
    xrp_nav_usd = (locked_per_share + unlocked_per_share) * price
    assets_100 = acquisitions_cost / shares
    assets_50 = assets_100 * 0.5

    # 5. Grand Totals
    total_100 = xrp_nav_usd + assets_100
    total_50 = xrp_nav_usd + assets_50
    potential_return = total_100 / bid_price

    message = (
        f"XRP Price: ${price:,.2f}\n"
        f"Ripple NAV/share: ${total_100:.0f}\n"
        f"MOIC: {potential_return:.1f}x\n"
        f"1. XRP NAV per Share: ${(locked_per_share+unlocked_per_share)*price:.1f}\n"
        f"2. Strategic Assets NAV: ${assets_100:.1f}\n"
    )
    return message

def send_telegram(text):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'})

if __name__ == "__main__":
    report = get_ripple_nav()
    send_telegram(report)
