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
- **[UPDATE 3.6.102]** Uniform URL handling standardized across versions.
- **[UPDATE 3.6.98]** File download logic streamlined.
- **[UPDATE 3.6.96]** Dynamic title height adjustment, rendering logic improved.
- **[UPDATE 3.6.75]** Dedicated layout redesigns for mobile, tablet, and desktop.
- **[UPDATE 3.6.66]** Fine-grained route control and redirects added for media content paths.
- **[UPDATE 3.6.50]** Modular rendering of media cards, YouTube downloaders, search headers.
- **[UPDATE 3.6.43]** Trend component built with localStorage support.
- **[UPDATE 3.6.32]** Enhanced asset caching & stylesheet splitting for performance.
- **[UPDATE 3.5.1]** Changing from WSGI to ASGI for better performance.
- **[UPDATE 3.4.124]** Parsing and sanitizing URLs, extracting identifiers.
- **[UPDATE 3.4.107]** Input sanitization, CSP headers, and rate-limiting were progressively added.
- **[UPDATE 3.4.104]** Metadata scraping with `youtube-dl`.
- **[UPDATE 3.4.100]** Handling related content by author/channel
- **[UPDATE 3.4.91]** Media platform validation and response control.

## Contributing
Contributions, feedback, and testing are welcome! Please open a pull request or issue for any modifications. The main branch is reserved for production; development should be done in separate branches.

## License
This project is licensed under the CeCILL Free Software License Agreement (Version 2.1). For full details, visit: [CeCILL License](http://www.cecill.info/index.en.html).

## Contact
For inquiries or support, feel free to open an issue on GitHub.

