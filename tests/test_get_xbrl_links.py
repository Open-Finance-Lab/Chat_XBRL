import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from your_module_name import get_xbrl_links  # Replace with your module name

class TestGetXbrlLinks(unittest.TestCase):

    @patch('your_module_name.requests.Session.get')
    def test_successful_request_with_links(self, mock_get):
        """Test if get_xbrl_links successfully parses valid file links."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = """
        <html>
            <body>
                <a href="https://www.sec.gov/Archives/file1.xml">File 1</a>
                <a href="https://www.sec.gov/Archives/file2.xsd">File 2</a>
                <a href="https://www.sec.gov/Archives/file3.txt">File 3 (not included)</a>
            </body>
        </html>
        """
        mock_get.return_value = mock_response
        
        file_links, folder_name = get_xbrl_links("https://example.com")

        self.assertIn("https://www.sec.gov/Archives/file1.xml", file_links)
        self.assertIn("https://www.sec.gov/Archives/file2.xsd", file_links)
        self.assertNotIn("https://www.sec.gov/Archives/file3.txt", file_links)
        self.assertEqual(len(file_links), 2)  # Only 2 links should be present
        self.assertIsNotNone(folder_name)  # Folder name should not be None

    @patch('your_module_name.requests.Session.get')
    def test_http_request_failure(self, mock_get):
        """Test if get_xbrl_links handles HTTP request failures properly."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        file_links, folder_name = get_xbrl_links("https://example.com")

        self.assertEqual(file_links, [])
        self.assertIsNone(folder_name)

    @patch('your_module_name.requests.Session.get')
    def test_html_parsing_error(self, mock_get):
        """Test if get_xbrl_links handles parsing errors gracefully."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = "INVALID HTML CONTENT"
        mock_get.return_value = mock_response

        file_links, folder_name = get_xbrl_links("https://example.com")

        self.assertEqual(file_links, [])
        self.assertIsNone(folder_name)

    @patch('your_module_name.requests.Session.get')
    def test_page_with_no_links(self, mock_get):
        """Test if get_xbrl_links handles a page with no links correctly."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = "<html><body>No file links here!</body></html>"
        mock_get.return_value = mock_response

        file_links, folder_name = get_xbrl_links("https://example.com")

        self.assertEqual(file_links, [])
        self.assertIsNone(folder_name)

    @patch('your_module_name.requests.Session.get')
    def test_retry_logic(self, mock_get):
        """Test if get_xbrl_links properly retries on failure."""
        mock_get.side_effect = [requests.exceptions.ConnectionError("Failed to connect")] * 4 + [MagicMock(status_code=200, content="""
        <html>
            <body>
                <a href="https://www.sec.gov/Archives/file1.xml">File 1</a>
            </body>
        </html>
        """)]

        file_links, folder_name = get_xbrl_links("https://example.com")

        self.assertIn("https://www.sec.gov/Archives/file1.xml", file_links)
        self.assertEqual(len(file_links), 1)  # Should only succeed after retries
        self.assertIsNotNone(folder_name)  # Folder name should not be None


if __name__ == "__main__":
    unittest.main()
