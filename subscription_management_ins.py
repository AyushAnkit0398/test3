import json
import argparse
from datetime import datetime, timedelta

# To activate the subscription for 3 days: python subscription_management_ins.py -c
# To activate the subscription for 7 days: python subscription_management_ins.py -d
# To activate the subscription for 15 days: python subscription_management_ins.py -e
# To activate the subscription for 30 days: python subscription_management_ins.py -a
# To activate the subscription for 1 day: python subscription_management_ins.py -b
# To deactivate the subscription: python subscription_management_ins.py -f
# To check the subscription status: python subscription_management_ins.py -s

CONFIG_FILE = 'ins_subscription_config.json'

def load_subscription_data_ins():
    """Load subscription data from JSON file."""
    try:
        with open(CONFIG_FILE, 'r') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            'subscription_status_ins': False,
            'purchase_time_ins': None,
            'expiry_time_ins': None
        }

def save_subscription_data_ins(data):
    """Save subscription data to JSON file."""
    with open(CONFIG_FILE, 'w') as file:
        json.dump(data, file, indent=4)
    return data

def is_subscription_active(expiry_time_ins):
    """Check if the subscription is active based on expiry time."""
    return datetime.now() < datetime.fromisoformat(expiry_time_ins)

def calculate_new_expiry_date(current_expiry, days_to_add):
    """Calculate new expiry date by adding days to the current expiry date."""
    if current_expiry:
        current_expiry_date = datetime.fromisoformat(current_expiry)
    else:
        current_expiry_date = datetime.now()
    new_expiry_date = current_expiry_date + timedelta(days=days_to_add)
    return new_expiry_date.isoformat()

def update_subscription_status_ins():
    """Update the subscription status based on current date."""
    data = load_subscription_data_ins()
    if data['expiry_time_ins'] and not is_subscription_active(data['expiry_time_ins']):
        data['subscription_status_ins'] = False
        data['expiry_time_ins'] = None
        data['purchase_time_ins'] = None
    save_subscription_data_ins(data)
    return data

def activate_subscription(days):
    data = load_subscription_data_ins()
    if data['subscription_status_ins']:
        data['expiry_time_ins'] = calculate_new_expiry_date(data['expiry_time_ins'], days) # Extend existing subscription
    else:
        # Activate new subscription
        data['subscription_status_ins'] = True
        data['purchase_time_ins'] = datetime.now().isoformat()
        data['expiry_time_ins'] = (datetime.now() + timedelta(days=days)).isoformat()
    save_subscription_data_ins(data)

def deactivate_subscription():
    """Deactivate the subscription."""
    data = load_subscription_data_ins()
    data['subscription_status_ins'] = False
    data['purchase_time_ins'] = None
    data['expiry_time_ins'] = None
    save_subscription_data_ins(data)

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
    data = update_subscription_status_ins()

    if args.activate30:
        activate_subscription(days=30)
        print("Subscription activated for 30 days.")
    elif args.activate1:
        activate_subscription(days=1)
        print("Subscription activated for 1 day.")
    elif args.activate3:
        activate_subscription(days=3)
        print("Subscription activated for 3 days.")
    elif args.activate7:
        activate_subscription(days=7)
        print("Subscription activated for 7 days.")
    elif args.activate15:
        activate_subscription(days=15)
        print("Subscription activated for 15 days.")
    elif args.deactivate:
        deactivate_subscription()
        print("Subscription deactivated.")
    elif args.status:
        print(f"Subscription active: {data['subscription_status_ins']}")
    else:
        print("Error: You must specify either -a (activate 30 days), -b (activate 1 day), -c (activate 3 days), -d (activate 7 days), -e (activate 15 days), -f (deactivate), or -s (status).")

if __name__ == "__main__":
    main()
