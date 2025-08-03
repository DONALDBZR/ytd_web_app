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
- **[UPDATE 4.2.145]** YouTube Download Operations: Full video/audio download pipeline, Combination of audio/video streams, Saving files and metadata to database.
- **[UPDATE 4.2.134]** Database Structure Initialization: Conditional table creation for YouTube and MediaFile.
- **[UPDATE 4.2.129]** Delete & Cleanup Operations: Deletion of media records by identifier.
- **[UPDATE 4.2.126]** Session and Security System: Session table and management, Security layer initialization and session lifecycle management.
- **[UPDATE 4.2.121]** YouTube Data Pipeline: End-to-end pipeline for storing, retrieving, and processing YouTube metadata, Support for related content search.
- **[UPDATE 4.2.113]** Media Management System: Comprehensive media management layer, Retrieval and insertion of metadata and Query capabilities by author, channel, title.
- **[UPDATE 4.2.97]** Event & Analytics Tracking: Event tracking: clicks, search submissions, color scheme changes, Device, event type, and network location models.
- **[UPDATE 4.2.73]** Media System Integration: Download and store media files, metadata persistence and retrieval and YouTube downloader initialized.
- **[UPDATE 4.2.54]** Implementation of a dynamic model system allowing CRUD operations on database tables, dynamic model class creation for any table and consistent base `Table_Model` for inheritance.
- **[UPDATE 4.2.24]** Creation of a comprehensive database handler system, including query execution, transaction management, connection handling, sanitization layer to protect against SQL injection and foundation for a table model system (like an ORM).

## Contributing
Contributions, feedback, and testing are welcome! Please open a pull request or issue for any modifications. The main branch is reserved for production; development should be done in separate branches.

## License
This project is licensed under the CeCILL Free Software License Agreement (Version 2.1). For full details, visit: [CeCILL License](http://www.cecill.info/index.en.html).

## Contact
For inquiries or support, feel free to open an issue on GitHub.

