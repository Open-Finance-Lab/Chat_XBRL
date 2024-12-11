import unittest
import os
from unittest.mock import patch, MagicMock
from evaluationfinal import validate_cik, extract_file_links, get_xbrl_links, download_file
from bs4 import BeautifulSoup

class TestEvaluation(unittest.TestCase):
    
    def test_validate_cik_valid_input(self):
        """Test that a valid CIK is properly zero-padded to 10 digits."""
        self.assertEqual(validate_cik('12345'), '0000012345')
        self.assertEqual(validate_cik('0000012345'), '0000012345')
        self.assertEqual(validate_cik('1'), '0000000001')
        
    def test_validate_cik_invalid_input(self):
        """Test that non-numeric CIKs raise a ValueError."""
        with self.assertRaises(ValueError):
            validate_cik('abcde')
        with self.assertRaises(ValueError):
            validate_cik('12ab45')
        with self.assertRaises(ValueError):
            validate_cik('1234567890123')  # More than 10 digits
    
    def test_extract_file_links(self):
        """Test that extract_file_links correctly extracts .xml and .xsd links from an HTML page."""
        html_content = '''
        <html>
            <body>
                <a href="/path/to/file1.xml">File 1</a>
                <a href="/path/to/file2.xsd">File 2</a>
                <a href="/path/to/file3.html">File 3</a>
            </body>
        </html>
        '''
        soup = BeautifulSoup(html_content, 'html.parser')
        file_links, folder_name = extract_file_links(soup, 'https://example.com')
        
        self.assertEqual(len(file_links), 2)
        self.assertIn('https://example.com/path/to/file1.xml', file_links)
        self.assertIn('https://example.com/path/to/file2.xsd', file_links)
        self.assertEqual(folder_name, 'file1')

    @patch('cik_parser.requests.get')
    def test_get_xbrl_links_successful(self, mock_get):
        """Test that get_xbrl_links returns correct file links and folder name."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = '''
        <html>
            <body>
                <table class="tableFile2">
                    <tr><td><a href="/Archives/edgar/data/file1.xml">File 1</a></td></tr>
                    <tr><td><a href="/Archives/edgar/data/file2.xsd">File 2</a></td></tr>
                    <tr><td><a href="/Archives/edgar/data/file3.html">File 3</a></td></tr>
                </table>
            </body>
        </html>
        '''
        mock_get.return_value = mock_response

        file_links, folder_name = get_xbrl_links('https://example.com')
        self.assertEqual(len(file_links), 2)
        self.assertIn('https://example.com/Archives/edgar/data/file1.xml', file_links)
        self.assertIn('https://example.com/Archives/edgar/data/file2.xsd', file_links)
    
    @patch('cik_parser.requests.get')
    def test_get_xbrl_links_failure(self, mock_get):
        """Test that get_xbrl_links handles failed requests gracefully."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        file_links, folder_name = get_xbrl_links('https://example.com')
        self.assertEqual(file_links, [])
        self.assertIsNone(folder_name)

    @patch('cik_parser.requests.get')
    def test_download_file_success(self, mock_get):
        """Test that download_file successfully downloads a file and saves it."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'This is a test file.'
        mock_get.return_value = mock_response

        file_path = download_file('https://example.com/file.xml', folder_name='./downloads')
        self.assertTrue(os.path.isfile(file_path))

        # Clean up
        os.remove(file_path)
    
    @patch('cik_parser.requests.get')
    def test_download_file_retry_logic(self, mock_get):
        """Test that download_file retries on failure and eventually raises an exception."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        file_path = download_file('https://example.com/file.xml', folder_name='./downloads', max_retries=2)
        self.assertIsNone(file_path)
    
    @patch('cik_parser.requests.get')
    def test_download_file_file_already_exists(self, mock_get):
        """Test that if a file already exists, download_file skips downloading it."""
        # Create a dummy file
        file_path = './downloads/dummy_file.xml'
        os.makedirs('./downloads', exist_ok=True)
        with open(file_path, 'w') as f:
            f.write('Test content')

        result = download_file('https://example.com/dummy_file.xml', folder_name='./downloads')
        self.assertEqual(result, file_path)

        # Clean up
        os.remove(file_path)

if __name__ == '__main__':
    unittest.main()
