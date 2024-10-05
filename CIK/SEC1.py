import requests
from xml.etree import ElementTree

def get_cik(ticker):
    company_name = ticker
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8'
    })

    base_url = "https://www.sec.gov/cgi-bin/browse-edgar"
    params = {
        "action": "getcompany",
        "CIK": ticker,
        "output": "xml"
    }

    response = session.get(base_url, params=params)

    print(f"URL used for request: {response.url}")
    print(f"Response Status Code: {response.status_code}")

    if response.status_code == 200:
        root = ElementTree.fromstring(response.content)
        cik_element = root.find('.//CIK')
        if cik_element is not None:
            if company_name == 'shortName not found':
                company_name = root.find('.//name').text
            return cik_element.text, company_name
        else:
            return "CIK not found", company_name
    else:
        return "Request failed with status code " + str(response.status_code), company_name

# # Example usage
ticker_symbol = "META"
cik_number, company_name = get_cik(ticker_symbol)
print(f"CIK Number for {company_name}: {cik_number}")
print(f"Ticker Symbol for {company_name}: {ticker_symbol}")
import requests
from bs4 import BeautifulSoup

def load10k_xbrl(cik_num=None):
    if cik_num is None:
        print("CIK number is required.")
        return []

    url_to_all_10k = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik_num}&type=10-K&dateb=&owner=include&count=40&search_text="


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8'
    }

    try:
        response = requests.get(url_to_all_10k, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class='tableFile2')

        if table:
            full_links = []
            for row in table.find_all('tr')[1:]:  # Skipping the header row
                cols = row.find_all('td')
                if len(cols) > 3:
                    filing_type = cols[0].text.strip()
                    filing_date = cols[3].text.strip()

                    if filing_type == '10-K':
                        doc_link = cols[1].find('a', href=True)['href']
                        full_links.append(f"https://www.sec.gov{doc_link}"/)
            if full_links:
                return full_links
            else:
                print("No 10-K filings.")
                return []
        else:
            print("No table found on the SEC page.")
            return []
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return []

# # Example usage
urls = load_10k_xbrl('0000320193')
print(urls)