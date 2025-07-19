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
- **[UPDATE 4.1.18]** Introduced a new class to manage a logger instance specifically for the Extractio application.  This marks a formalized separation of logging responsibilities within the system.
- **[UPDATE 4.1.16]** Added initialization logic for the Logger_Configurator class.  Allows use of default or user-defined settings for flexible logging configuration.
- **[UPDATE 4.1.12]** Defined a dedicated class to configure logging settings, promoting separation of concerns and configurability.
- **[UPDATE 4.1.10]** Established a custom logger specific to Extractio.  Sets up a standardized logging format and possibly introduces future support for log routing.
- **[UPDATE 4.0.4]** Major improvements in video retrieval and download logic.  Enhances selection of video streams based on resolution, file size, and codec compatibility.  Introduces constraints that ensure only high-quality videos are downloaded with matching audio.

## Contributing
Contributions, feedback, and testing are welcome! Please open a pull request or issue for any modifications. The main branch is reserved for production; development should be done in separate branches.

## License
This project is licensed under the CeCILL Free Software License Agreement (Version 2.1). For full details, visit: [CeCILL License](http://www.cecill.info/index.en.html).

## Contact
For inquiries or support, feel free to open an issue on GitHub.

