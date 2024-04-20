
## Setup

# Python version : 3.12.1

1. Clone this repository to your local machine.

2. Install the necessary dependencies using the provided `requirements.txt` file:
   ### Install from root directory
    pip install -r requirements.txt 

3. Set up your environment variables:

   - `SEARCH_INPUT`: The search query for the NY Times website.
   - `NUMBER_OF_MONTH`: The number of months for the date range.
   - `SENDER_EMAIL`: Sender's email address for sending emails.
   - `SENDER_APP_PASSWORD`: Application-specific password for the sender's email. (Take from sender google account)
   - `RECEIVER_EMAIL`: Receiver's email address for receiving emails.

4. Download the `client_secret.json` file from the Google Cloud Console for accessing the Google Sheets API. Place it in the project directory.

5. Ensure that the `chromedriver` executable is in your system's PATH or update the path to the WebDriver in the code.

## Usage

1. Run the `main.py` file to execute the scraping, data manipulation, and email sending process.

