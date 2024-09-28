import unittest
from nlp_preprocess_toolkit_utils.preprocess import preprocess_text, read_file, generate_word_cloud
import os

class TestNLPPreprocess(unittest.TestCase):

    def test_preprocess_text(self):
        """Test the text preprocessing function."""
        sample_text = "This is a Sample text with punctuation! And some URL: https://example.com."
        processed = preprocess_text(sample_text)
        expected = "sample text punctuation"  # No need to keep 'url' as part of the expected output
        self.assertEqual(processed, expected)



    def test_read_file(self):
        """Test the file reading function for text files."""
        with open('test_sample.txt', 'w') as f:
            f.write('This is a sample file content.')

        content = read_file('test_sample.txt')
        expected = 'This is a sample file content.'
        self.assertEqual(content, expected)

        # Clean up
        os.remove('test_sample.txt')

    # You can add more tests for other functions as needed

if __name__ == '__main__':
    unittest.main()
