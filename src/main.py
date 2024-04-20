from src.scrape import ScrapeBase
from src.put_data import ScrapeData
from src.smtp_send_email import SMTPSendEmail

def main():
    """
    Main function to orchestrate the scraping, data processing, and email sending process.
    """
    try:

        # Initialize objects
        scrape_obj = ScrapeBase()
        scrape_data_obj = ScrapeData()
        smtp_obj = SMTPSendEmail()

        # URL to scrape
        url = "https://www.nytimes.com/"

        # Perform scraping
        try:
            scrape_obj.request_to_url(url)
        except Exception as e:
            print(f"Error during URL request: {str(e)}")
            return
        
        try:
            scrape_obj.find_search_field()
        except Exception as e:
            print(f"Error during finding search field: {str(e)}")
            return
        
        try:
            scrape_obj.input_search_field()
        except Exception as e:
            print(f"Error during inputting search field: {str(e)}")
            return

        try:
            scrape_obj.input_date_range()
        except Exception as e:
            print(f"Error during inputting date range: {str(e)}")
            return
        
        try:
            items = scrape_obj.load_full_content()
        except Exception as e:
            print(f"Error during loading full content: {str(e)}")
            return

        try:
            data = scrape_obj.extract_data(items)
        except Exception as e:
            print(f"Error during extracting data: {str(e)}")
            return

        # Write data to Google Sheet
        try:
            scrape_data_obj.write_in_google_sheet(data)
        except Exception as e:
            print(f"Error during writing data to Google Sheet: {str(e)}")
            return

        # Send email
        try:
            smtp_obj.send_email()
        except Exception as e:
            print(f"Error during sending email: {str(e)}")
            return

        print("## Done")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
