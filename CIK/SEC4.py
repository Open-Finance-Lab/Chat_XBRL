''' cik_number;
print(f"CIK Number for {cik_number}")
cik_number = '0001326801'
urls = load_10k_xbrl(cik_number)
print(f"URLs for {company_name}: {urls}") '''

input_file_path = '/content/3_test.txt'

''' print(f"CIK Number for {cik_number}")
cik_number = '0001326801'
urls = load_10k_xbrl(cik_number)
print(f"URLs for {company_name}: {urls}")

#download_dir = '.'  # Current working directory
download_dir = '/content'
for url in (urls):
  folder, xbrl_file = download_sec_files(url, download_dir)
  print(f"Folder: {folder}, XBRL File: {xbrl_file}") '''

try:
    with open(input_file_path, 'r') as file:
        # Loop through each line in the file
        for line in file:
            cik_number = line.strip()  # Remove any leading/trailing whitespace
            print("CIK NUMBER CHANGED TO {}".format(cik_number))
            print(f"CIK Number for {cik_number}")
            urls = load_10k_xbrl(cik_number)
            print(f"URLs for {company_name}: {urls}")

            sub_dir = cik_number
            parent_dir = "/content"

            full_path = os.path.join(parent_dir, sub_dir)

            # Create the subdirectory
            os.mkdir(full_path)

            #download_dir = '.'  # Current working directory
            download_dir = full_path
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