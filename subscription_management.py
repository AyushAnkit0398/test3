import json
import argparse
from datetime import datetime, timedelta

# To activate the subscription for 3 days: python subscription_management.py -c
# To activate the subscription for 7 days: python subscription_management.py -d
# To activate the subscription for 15 days: python subscription_management.py -e
# To activate the subscription for 30 days: python subscription_management.py -a
# To activate the subscription for 1 day: python subscription_management.py -b
# To deactivate the subscription: python subscription_management.py -f
# To check the subscription status: python subscription_management.py -s

CONFIG_FILE = 'subscription_config.json'

def load_subscription_data_IS():
    """Load subscription data_IS from JSON file."""
    try:
        with open(CONFIG_FILE, 'r') as file:
            data_IS = json.load(file)
        return data_IS
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            'subscription_status': False,
            'purchase_time': None,
            'expiry_time': None
        }

def save_subscription_data_IS(data_IS):
    """Save subscription data_IS to JSON file."""
    with open(CONFIG_FILE, 'w') as file:
        json.dump(data_IS, file, indent=4)

def is_subscription_active(expiry_time):
    """Check if the subscription is active based on expiry time."""
    return datetime.now() < datetime.fromisoformat(expiry_time)

def calculate_new_expiry_date(current_expiry, days_to_add):
    """Calculate new expiry date by adding days to the current expiry date."""
    if current_expiry:
        current_expiry_date = datetime.fromisoformat(current_expiry)
    else:
        current_expiry_date = datetime.now()
    new_expiry_date = current_expiry_date + timedelta(days=days_to_add)
    return new_expiry_date.isoformat()

def update_subscription_status():
    """Update the subscription status based on current date."""
    data_IS = load_subscription_data_IS()
    if data_IS['expiry_time'] and not is_subscription_active(data_IS['expiry_time']):
        data_IS['subscription_status'] = False
        data_IS['expiry_time'] = None
        data_IS['purchase_time'] = None
    save_subscription_data_IS(data_IS)
    return data_IS

def activate_subscription_is(days):
    data_IS = load_subscription_data_IS()
    if data_IS['subscription_status']:
        data_IS['expiry_time'] = calculate_new_expiry_date(data_IS['expiry_time'], days) # Extend existing subscription
    else:
        # Activate new subscription
        data_IS['subscription_status'] = True
        data_IS['purchase_time'] = datetime.now().isoformat()
        data_IS['expiry_time'] = (datetime.now() + timedelta(days=days)).isoformat()
    save_subscription_data_IS(data_IS)

def deactivate_subscription_is():
    """Deactivate the subscription."""
    data_IS = load_subscription_data_IS()
    data_IS['subscription_status'] = False
    data_IS['purchase_time'] = None
    data_IS['expiry_time'] = None
    save_subscription_data_IS(data_IS)

def main():
    parser = argparse.ArgumentParser(description="Manage subscription status.")
    parser.add_argument(
        "-a", "--activate30", action="store_true", help="Activate the subscription for 30 days."
    )
    parser.add_argument(
        "-b", "--activate1", action="store_true", help="Activate the subscription for 1 day."
    )
    parser.add_argument(
        "-c", "--activate3", action="store_true", help="Activate the subscription for 3 days."
    )
    parser.add_argument(
        "-d", "--activate7", action="store_true", help="Activate the subscription for 7 days."
    )
    parser.add_argument(
        "-e", "--activate15", action="store_true", help="Activate the subscription for 15 days."
    )
    parser.add_argument(
        "-f", "--deactivate", action="store_true", help="Deactivate the subscription."
    )
    parser.add_argument(
        "-s", "--status", action="store_true", help="Check the current subscription status."
    )
    args = parser.parse_args()
    
    # Load and update subscription status
    data_IS = update_subscription_status()

    if args.activate30:
        activate_subscription_is(days=30)
        print("Subscription activated for 30 days.")
    elif args.activate1:
        activate_subscription_is(days=1)
        print("Subscription activated for 1 day.")
    elif args.activate3:
        activate_subscription_is(days=3)
        print("Subscription activated for 3 days.")
    elif args.activate7:
        activate_subscription_is(days=7)
        print("Subscription activated for 7 days.")
    elif args.activate15:
        activate_subscription_is(days=15)
        print("Subscription activated for 15 days.")
    elif args.deactivate:
        deactivate_subscription_is()
        print("Subscription deactivated.")
    elif args.status:
        print(f"Subscription active: {data_IS['subscription_status']}")
    else:
        print("Error: You must specify either -a (activate 30 days), -b (activate 1 day), -c (activate 3 days), -d (activate 7 days), -e (activate 15 days), -f (deactivate), or -s (status).")

if __name__ == "__main__":
    main()