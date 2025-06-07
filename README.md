# Extractio (YouTube Downloader)

## Description
Extractio is a YouTube Downloader that allows users to download media content directly from YouTube for free. It is a web-based application designed for efficiency, ease of use, and fast downloads.

### **Features:**
- Download videos from YouTube in 1080p.
- Supports both audio and video downloads.
- Web-based: No software installation required.
- Fast and secure media retrieval.

## Installation & Setup

### **Prerequisites:**
Ensure you have the following installed on your system:
- Python (for backend)
- MySQL (for database management)

### **Setup Steps:**
1. Clone the repository:
   ```sh
   git clone https://github.com/DONALDBZR/ytd_web_app.git
   cd ytd_web_app
   ```
2. Install dependencies:
   ```sh
   pip3 install -r requirements.txt
   ```
3. Configure environment variables (e.g., API keys, database settings).
4. Start the backend server:
   ```sh
   source ./venv/bin/activate
   python3 -m flask --app index run
   ```
5. Open the application in your browser.

## Usage
1. Enter a YouTube URL in the input field.
2. Click the "Download" button to retrieve the media.

## Commit History (Latest Major Updates)
- **[UPDATE 3.7.129]** Rendered YouTube Downloader Component: to reflect latest media interaction logic.
- **[UPDATE 3.7.128]** Dynamic FontAwesome Icons are used to represent media types, improving UX.
- **[UPDATE 3.7.127]** Download Button Logic: Button display now dynamically adjusts based on route and media type.
- **[UPDATE 3.7.126]** Media Route Generation: Route URLs are dynamically built based on media types and server metadata responses.
- **[UPDATE 3.7.125]** URL Sanitization: Prevents injection and unauthorized access by escaping HTML characters and validating domain origins.
- **[UPDATE 3.7.124]** Domain Whitelist Checks: Enforces allowed YouTube domains for content extraction.
- **[UPDATE 3.7.123]** YouTube Identifier Parsing: Accurate extraction of media identifiers from input uniform resource locators.
- **[UPDATE 3.7.118]** `localStorage` Cleanup: Conditional cleanup tied to HTTP responses to avoid data corruption.
- **[UPDATE 3.7.117]** Response Validation & Error Feedback: Ensures front-end stability with clear validation checks.
- **[UPDATE 3.7.116]** YouTube Metadata Retrieval via API: GET requests fetch metadata dynamically, enabling pre-download previews.
- **[UPDATE 3.7.108]** Form Submission Rework: Forms trigger real-time metadata extraction, enhancing interaction flow.
- **[UPDATE 3.7.87]** Route-Based Media Source Generation: Media URLs are constructed from route paths and metadata.
- **[UPDATE 3.7.86]** Media Download Request Handling: Backend now supports direct POST requests for starting downloads.

## Contributing
Contributions, feedback, and testing are welcome! Please open a pull request or issue for any modifications. The main branch is reserved for production; development should be done in separate branches.

## License
This project is licensed under the CeCILL Free Software License Agreement (Version 2.1). For full details, visit: [CeCILL License](http://www.cecill.info/index.en.html).

## Contact
For inquiries or support, feel free to open an issue on GitHub.

