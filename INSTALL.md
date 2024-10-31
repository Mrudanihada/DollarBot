## Installation

### Pre-requisite Tasks

Here are some pre-requisite tasks that you'll have to take complete before starting installation:

1. In Telegram App/Desktop, search for "BotFather". Click on "Start", and enter the following command:
```
  /newbot
```
2. Follow the instructions on screen:

    * Choose a name for your bot. 
    * Select a username for your bot that ends with "bot" (this is a rule Telegram enforces).

3. BotFather will confirm the creation of your bot and provide a HTTP API access token.
4. Copy and save this token for future use.

### Actual Installation

The below instructions can be followed in order to set-up communication with the bot from your end in a span of few minutes! Let's get started:

1. Clone this repository to your local system.
2. Start a terminal session in the directory where the project has been cloned. Run the following command to install the required dependencies:
```
  pip install -r requirements.txt
```
3. In the directory where this repo has been cloned, please run the below command to execute a bash script to run the Telegram Bot:
```
   ./run.sh
```
(OR)
```
   bash run.sh
```
4. It will ask you to paste the API token you received from Telegram in pre-requisites step 4.
5. A successful run will generate a message on your terminal that says "TeleBot: Started polling." 
6. In the Telegram app, search for your newly created bot by entering the username and open the same.
  
   Now, on Telegram, enter the "/start" or "/menu" command, and you are all set to track your expenses with DollarBot!
