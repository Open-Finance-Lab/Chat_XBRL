
# List of tickers and years
# Loop through each ticker and year to download XBRL files
''' cik_number; 
print(f"CIK Number for {cik_number}")
cik_number = '0001326801'
urls = load_10k_xbrl(cik_number)
print(f"URLs for {company_name}: {urls}") '''

input_file_path = '/3_test.txt'

try:
    with open(input_file_path, 'r') as file:
        # Loop through each line in the file
        for line in file:
            cik_number = line.strip()  # Remove any leading/trailing whitespace

            print(f"CIK Number for {cik_number}")
            cik_number = '0001326801'
            urls = load_10k_xbrl(cik_number)
            print(f"URLs for {company_name}: {urls}")

            download_dir = '.'  # Current working directory
            for url in (urls):
              folder, xbrl_file = download_sec_files(url, download_dir)
              print(f"Folder: {folder}, XBRL File: {xbrl_file}")


except FileNotFoundError:
    print(f'Error: The file "{input_file_path}" was not found.')
except Exception as e:
    print(f'An error occurred: {e}')

''' download_dir = '.'  # Current working directory
for url in (urls):
  folder, xbrl_file = download_sec_files(url, download_dir)
  print(f"Folder: {folder}, XBRL File: {xbrl_file}") '''
