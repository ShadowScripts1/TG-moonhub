import requests
import json
import time
import datetime
import os
from colorama import Fore, Style, init

init(autoreset=True)

def print_welcome_message():
    print(Fore.WHITE + r"""
 ____  _   _    _    ____   _____        __   ____   ____ ____  ___ ____ _____ ____  
/ ___|| | | |  / \  |  _ \ / _ \ \      / /  / ___| / ___|  _ \|_ _|  _ \_   _/ ___| 
\___ \| |_| | / _ \ | | | | | | \ \ /\ / /   \___ \| |   | |_) || || |_) || | \___ \ 
 ___) |  _  |/ ___ \| |_| | |_| |\ V  V /     ___) | |___|  _ < | ||  __/ | |  ___) |
|____/|_| |_/_/   \_\____/ \___/  \_/\_/     |____/ \____|_| \_\___|_|    |_| |____/ 
          """)
    print(Fore.GREEN + Style.BRIGHT + "Moonhub Airdrop Searcher by Shadow Scripts")
    print(Fore.YELLOW + Style.BRIGHT + "Telegram: https://t.me/shadowscripters")

def load_accounts():
    with open('data.txt', 'r') as file:
        return [line.strip() for line in file if line.strip()]

def process_account(auth):
    headers = {
        'authorization': auth,
        'accept': 'application/json, text/plain, */*',
        'origin': 'https://tg.moongate.app',
        'referer': 'https://tg.moongate.app/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
    }

    # Profile
    response = requests.get('https://tg-api.moongate.app/api/v1/user/profile?refBy=', headers=headers)
    if response.status_code == 200:
        profile = response.json()
        print(Fore.CYAN + f"Profile: {profile['username']} ({profile['first_name']})")
        print(Fore.CYAN + f"Level: {profile['user_level']}")
        print(Fore.CYAN + f"Current points: {profile['current_point']}")
        print(Fore.CYAN + f"Total points: {profile['total_point']}")
        print(Fore.CYAN + f"Points per hour: {profile['point_per_hour']}")
        print(Fore.CYAN + f"Max mining hours: {profile['max_mine_hour']}")
        print(Fore.CYAN + f"Referral code: {profile['ref_code']}")
        print(Fore.CYAN + f"Total referrals: {profile['total_ref_count']}")
        print(Fore.CYAN + f"Total referral points: {profile['total_ref_point']}")
        print(Fore.CYAN + f"Check-in streak: {profile['checkin_streak']}")
        print(Fore.CYAN + f"Total check-ins: {profile['total_checkin']}")
        
        # Optimize based on profile
        optimize_mining(headers, profile)
        optimize_referrals(headers, profile)
    else:
        print(Fore.RED + "Failed to retrieve profile")
        return

    # Daily check-in
    daily_check_in(headers)

    # Task list and process tasks
    process_tasks(headers)

def optimize_mining(headers, profile):
    current_time = datetime.datetime.now()
    if profile['last_synced_point']:
        last_synced = profile['last_synced_point'].replace('Z', '')  # Remove 'Z'
        last_synced = datetime.datetime.fromisoformat(last_synced)  # Convert to datetime
    else:
        last_synced = None

    if not last_synced or (current_time - last_synced).total_seconds() / 3600 >= profile['max_mine_hour']:
        # Claim points if it's time
        payload = {"pointClaimed": 0, "updateTime": int(current_time.timestamp() * 1000)}
        response = requests.post('https://tg-api.moongate.app/api/v1/user/claim', headers=headers, json=payload)
        if response.status_code == 201:
            claimed_points = profile['point_per_hour'] * profile['max_mine_hour']
            print(Fore.GREEN + f"Claim successful. Points earned: {claimed_points}")
        else:
            print(Fore.RED + "Failed to claim")
    else:
        time_left = profile['max_mine_hour'] - (current_time - last_synced).total_seconds() / 3600
        print(Fore.YELLOW + f"Not time to claim yet. Time remaining: {time_left:.2f} hours")


def optimize_referrals(headers, profile):
    if profile['ref_claimable'] > 0:
        response = requests.post('https://tg-api.moongate.app/api/v1/user/claim-ref', headers=headers)
        if response.status_code == 200:
            print(Fore.GREEN + f"Referral claim successful. Points earned: {profile['ref_claimable']}")
        else:
            print(Fore.RED + "Failed to claim referral")
    else:
        print(Fore.YELLOW + "No referral points to claim")


def process_tasks(headers):
    response = requests.get('https://tg-api.moongate.app/api/v1/task/list', headers=headers)
    if response.status_code == 200:
        tasks = response.json()

        # Ensure 'tasks' is not None and is a list
        if tasks and isinstance(tasks, list):
            print(Fore.YELLOW + f"Number of tasks: {len(tasks)}")
            for task in tasks:
                # Check if 'task_user' exists or is None
                task_user = task.get('task_user')
                if task_user is None:
                    # If 'task_user' is None, the task hasn't been processed (assume not completed)
                    print(Fore.YELLOW + f"Task not processed: {task['name']}. Starting task process...")
                    process_task(headers, task)
                elif 'status' in task_user and task_user['status'] == "DONE":
                    # If 'task_user' exists and status is 'DONE', task is completed
                    print(Fore.CYAN + f"Task already completed: {task['name']}. Reward: {task_user['reward_amount']}")
                else:
                    # If 'task_user' exists but not 'DONE', process task
                    process_task(headers, task)
        else:
            print(Fore.RED + "Task list is empty or invalid.")
    else:
        print(Fore.RED + "Failed to retrieve task list")


def process_task(headers, task):
    task_id = task['_id']
    
    # Check if 'task_user' exists and is valid before processing
    task_user = task.get('task_user')
    if task_user is None or task_user.get('status') != "DONE":
        # If 'task_user' is None or not completed, process the task
        response = requests.put(f'https://tg-api.moongate.app/api/v1/task/{task_id}', headers=headers)
        if response.status_code == 200:
            print(Fore.YELLOW + f"Processing task: {task['name']}")
        else:
            print(Fore.RED + f"Failed to process task: {task['name']}")
            return

        # Check task completion
        response = requests.post(f'https://tg-api.moongate.app/api/v1/task/check/{task_id}', headers=headers)
        if response.status_code == 201:
            result = response.json()
            print(Fore.GREEN + f"Task completed: {task['name']}. Reward: {result['reward_amount']}")
        else:
            print(Fore.RED + f"Failed to complete task: {task['name']}")
    else:
        print(Fore.YELLOW + f"Task already completed: {task['name']}. No need to process again.")


def daily_check_in(headers):
    # Get info from daily check-in endpoint
    response = requests.get('https://tg-api.moongate.app/api/v1/task/daily', headers=headers)
    if response.status_code == 200:
        daily_info = response.json()
        
        # Get the last check-in date and convert it to datetime format
        last_checkin_day = daily_info.get('last_checkin_day')
        if last_checkin_day:
            # Convert last_checkin_day to datetime
            last_checkin_date = datetime.datetime.fromisoformat(last_checkin_day.replace('Z', ''))
            today = datetime.datetime.now().date()
            
            # Check if already checked in today
            if last_checkin_date.date() == today:
                print(Fore.YELLOW + "Check-in already done today. No need to check in again.")
                return  # Exit the function if already checked in
            else:
                print(Fore.GREEN + "Haven't checked in today. Proceeding with check-in.")
        else:
            print(Fore.YELLOW + "Check-in information not found. Proceeding with check-in.")
        
        # Display total daily check-in information
        print(Fore.GREEN + f"Total check-in days: {daily_info['total_checkin_days']}")
        
        # If there are additional points from daily check-in, display them as well
        if 'reward_amount' in daily_info:
            print(Fore.GREEN + f"Reward from daily check-in: {daily_info['reward_amount']}")
        
        # Proceed with check-in process if not done today
        response = requests.get('https://tg-api.moongate.app/api/v1/task/checkin', headers=headers)
        if response.status_code == 200:
            checkin_result = response.json()
            print(Fore.GREEN + f"Check-in successful. Total check-in days now: {checkin_result['total_checkin_days']}")
        else:
            print(Fore.RED + "Failed to check in")
    else:
        print(Fore.RED + "Failed to retrieve daily check-in information")


def get_optimal_wait_time(accounts):
    min_wait_time = float('inf')
    for auth in accounts:
        headers = {
            'authorization': auth,
            'accept': 'application/json, text/plain, */*',
            'origin': 'https://tg.moongate.app',
            'referer': 'https://tg.moongate.app/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
        }
        response = requests.get('https://tg-api.moongate.app/api/v1/user/profile?refBy=', headers=headers)
        if response.status_code == 200:
            profile = response.json()
            max_mine_hour = profile['max_mine_hour']
            min_wait_time = min(min_wait_time, max_mine_hour)
    
    # Add a small buffer (e.g., 5 minutes) to ensure all accounts are ready
    return min_wait_time * 3600 + 300  # convert to seconds and add 5 minutes


def main():
    print_welcome_message()
    accounts = load_accounts()
    print(Fore.BLUE + f"Number of accounts: {len(accounts)}")

    while True:
        for i, auth in enumerate(accounts, 1):
            print(Fore.YELLOW + f"\nProcessing account {i}/{len(accounts)}")
            try:
                process_account(auth)
            except Exception as e:
                print(Fore.RED + f"Error on account {i}: {str(e)}")
            time.sleep(5)  # 5-second pause between accounts


        optimal_wait_time = get_optimal_wait_time(accounts)
        print(Fore.MAGENTA + f"\nAll accounts processed. Waiting {optimal_wait_time/3600:.2f} hours before starting again.")
        
        # Countdown for optimal wait time
        target_time = datetime.datetime.now() + datetime.timedelta(seconds=optimal_wait_time)
        while datetime.datetime.now() < target_time:
            remaining_time = target_time - datetime.datetime.now()
            hours, remainder = divmod(remaining_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            countdown = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            print(Fore.CYAN + f"\rTime remaining: {countdown}", end="", flush=True)
            time.sleep(1)
        
        print(Fore.GREEN + "\nRestarting process...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nProgram stopped by user.")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {str(e)}")
        print(Fore.YELLOW + "The program will continue with other tasks.")