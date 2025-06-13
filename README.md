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
- **[UPDATE 3.8.218]** State & Component Initialization: Initializing state from `localStorage` and triggering verification/tracking.
- **[UPDATE 3.8.225]** Rendering & UI Logic: Rendering download button, media cards, and related content.
- **[UPDATE 3.8.224]** File Download & Blob Handling: Handling file download from blob data, saving files to path.
- **[UPDATE 3.8.221]** Server Communication: Verifying file accessibility and video status.
- **[UPDATE 3.8.211]** Media Retrieval & Merging: Downloading and merging video with audio streams.
- **[UPDATE 3.8.209]** Video Stream Handling: Filtering video streams based on resolution, codec, size.
- **[UPDATE 3.8.192]** Media Retrieval & Merging: Conditional downloading based on file existence.
- **[UPDATE 3.8.187]** Media Format Selection: Determining audio format spec from format ID and protocol.
- **[UPDATE 3.8.186]** Audio Stream Handling: Validating, filtering, and saving audio streams.
- **[UPDATE 3.8.172]** Routing & Redirection: Determining file paths, updating routes, redirect handling.
- **[UPDATE 3.8.171]** Server Communication: Initiating media download via POST requests.
- **[UPDATE 3.8.132]** State & Component Initialization: State updates with trends and session data.
- **[UPDATE 3.8.105]** Rendering & UI Logic: Lifecycle method executions.
- **[UPDATE 3.8.163]** Server Communication: Extracting metadata using `yt-dlp`.
- **[UPDATE 3.8.154]** SEO & Metadata: Setting titles, descriptions, and meta tags for search engines.
- **[UPDATE 3.8.114]** Utility Functions: Utility classes for component support.
- **[UPDATE 3.8.99]** Utility Functions: HTML entity decoding.

## Contributing
Contributions, feedback, and testing are welcome! Please open a pull request or issue for any modifications. The main branch is reserved for production; development should be done in separate branches.

## License
This project is licensed under the CeCILL Free Software License Agreement (Version 2.1). For full details, visit: [CeCILL License](http://www.cecill.info/index.en.html).

## Contact
For inquiries or support, feel free to open an issue on GitHub.

