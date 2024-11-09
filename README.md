# Moonhub Bot Setup Guide

[Start Here](https://t.me/MoongateAIBot/moongate?startapp=GioxPki8FWaT0E)

---

## Key Features

- **Automatic Login & Task Automation**
- **Daily Rewards Collection**
- **Farm & Partner Task Management**
- **Twitter and Bot Task Handling**
- **Automated Gameplay**
- **Multi-Account Support**

---

## Prerequisites

Before starting, make sure you have:

- **Python** installed
- Basic **Terminal** knowledge

---

## Installation Guide

Follow these steps to install and configure the bot on Termux (for Android):

### Step 1: Install Python and Git

Use Termux to install Python and Git by running:

```shell
pkg install python git
```

### Step 2: Clone the Repository

Clone the Moonhub bot repository to your local environment:

```shell
git clone https://github.com/ShadowScripts1/TG-moonhub
```

### Step 3: Navigate to the Project Directory

Change to the project directory:

```shell
cd TG-moonhub
```

---

## Configuration

### Step 1: Set Up `data.txt`

1. Open the `data.txt` file in the root directory.
2. Add your Moonhub Coin account details, with each account on a new line in the following format:

   **Example:**
   ```plaintext
   tma user=%7B%22
   ```

---

## Running the Bot

To start the Moonhub bot, enter:

```shell
python bot.py
```

The bot will process the accounts in `data.txt`, performing tasks to earn rewards.

---

### Troubleshooting

- **Account Verification**: Double-check credentials in `data.txt`.
- **Network Issues**: Ensure a stable internet connection.
- **Server Status**: Verify that Moonhub Coin servers are online.
- **Retry**: If issues persist, wait a few moments and try again.

---

## Registering for a Moonhub Account

If you don't yet have a Moonhub Coin account, you can register here:

[Register for Moonhub](https://t.me/MoongateAIBot/moongate?startapp=GioxPki8FWaT0E)

---

## Retrieving `tgWebAppData` (query_id / user_id)

1. **Login to Telegram** on web or desktop.
2. Open **Developer Tools** (press `F12`) and go to the **Console** tab.
3. Enter the following command:

   ```javascript
   copy(Telegram.WebApp.initData)
   ```

4. Copy the output (`query_id=... / user=...`) and paste it into `data.txt`.

---

## Disclaimer

This bot is for educational purposes only. Use it at your own discretion. The authors assume no liability for its use.

---

## Contributions

We welcome improvements! Please submit pull requests for new features or fixes.

---

## Support and Donations

If you find this bot helpful, consider supporting the project:

- **Ethereum (EVM)**: `0x7BeE9994a631523e22A3aB83039c196bFc6BC513`
- **Solana**: `6mbFy6AojWo3J5ksa1SYHHyCWw5Bms4p9McKmaFkCsyW`

---

## Connect With Us

[![Join our Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/shadowscripters)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ShadowScripts1)

---