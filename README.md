HackNU
HackNU is a bank analysis system for cashbacks. Python-based project for automating cashback offers identification in videos using computer vision and natural language processing techniques, also web-scraping for parsing cashbacks from banks' websites.

Table of Contents
Introduction
Features
Installation
Usage
Configuration
Contributing
License
Introduction
HackNU is designed to assist users in extracting cashback offers from videos, making it easier to identify and utilize available discounts and promotions. By leveraging computer vision algorithms and natural language processing, HackNU automates the process of scanning videos for cashback information, allowing users to quickly access relevant deals.

Features
Automated extraction of cashback offers from videos
Integration with Google Drive for video storage and retrieval
Natural language processing for identifying and parsing cashback details
Support for various video formats and resolutions
User-friendly command-line interface for easy interaction
Installation
To install HackNU, follow these steps:

Clone the repository:

bash
Copy code
git clone https://github.com/aarizona23/HackNU.git
Navigate to the project directory:

bash
Copy code
cd HackNU
Install dependencies using pip:

bash
Copy code
pip install -r requirements.txt
Usage
To use HackNU, follow these steps:

Ensure you have a valid Google Cloud Service Account JSON file with access to the necessary APIs.

Set the following environmental variables:

bash
Copy code
export GOOGLE_API_SCOPES="https://www.googleapis.com/auth/drive"
export GOOGLE_SERVICE_ACCOUNT_FILE="/path/to/your/service_account_file.json"
Run the main script with the path to the video file:

bash
Copy code
python main.py /path/to/your/video.mp4
Configuration
HackNU requires the following environmental variables for configuration:

GOOGLE_API_SCOPES: The scope of Google API access (default: https://www.googleapis.com/auth/drive).
GOOGLE_SERVICE_ACCOUNT_FILE: The path to the Google Cloud Service Account JSON file.
Ensure these variables are set correctly before running the script.

Contributing
Contributions to HackNU are welcome! To contribute, please follow these guidelines:

Fork the repository and create a new branch for your feature or bug fix.
Make your changes and ensure the code passes all tests.
Submit a pull request with a clear description of your changes.
License
HackNU is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Special thanks to the HackNU team for their contributions to the project.

This README file provides an overview of HackNU, including its features, installation instructions, usage guidelines, configuration details, and information on how to contribute. Feel free to customize this README further to suit your project's specific needs and requirements.
