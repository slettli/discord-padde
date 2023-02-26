# discord-padde
Small Discord-bot for future of fintech spring 2023

## Features

* Show live offers from providers
  * (Except not really. It's not implemented yet.)
* Show electricity prices for yesterday, today and tomorrow 
  * Provided by [Hva koster strømmen](https://www.hvakosterstrommen.no)
* Show personal electricity consumption
  * Not fully implemented. Missing options to restrict to a period of time, as well as a way to authenticate a user.

## Comments
The idea behind this bot is to have convenient access to info about electricity. Features that should be added are a way to authenticate with your provider, so that the bot can track power usage. It could then monitor prices from different providers and ping you through Discord whenever you should switch providers.

It also needs a system for caching power prices, for the sake of hvakosterstrommen.no. 
  * This applies to the power chart it generates as well.

I was short on time though, so this is what I pulled together.


## How to run
Sorry, no docker or auto-setup proivded. Instead of doing all this, you can check it out in the Discord server provided over email.

Requires Python 3.11. The easiest way to run it is to clone the repository, make a virtual environment, and install the required packages through `pip install -r requirements.txt'. 
* Requires a discord bot and token to run.
* You also need to create a local `.env` file, see `example.env`.

### 1. Clone this repo

### 2. Log in to Discord's developer console
  - Create an application, and then a bot for that application
  - Enable all intents in the 'bot' page
  - This is also where you can generate an invite and add the bot to your server. It needs general permissions like viewing and posting messages, attaching embeds, attachments/files etc.

### 3. Set up the bot's token 
- Create a `.env` file in the root directory with the bot's token from the Discord developer console.
- See `example.env` for what the contents should look like. The file should just be called `.env`

### 3.5 (optional) Create a python venv to run the bot in

### 4. Install the required modules
- Open a terminal in the bot's folder and enter:
  - `pip install -r requirements.txt`

### 5. Start the bot
- The bot should now be ready to go. In a terminal:
  - `python3 -OO -m main.py`
