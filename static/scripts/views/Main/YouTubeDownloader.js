/**
 * The component to be rendered for the Download page but only
 * when it is for media from YouTube.
 */
class YouTubeDownloader extends React.Component {
    /**
     * Constructing the application from React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        /**
         * The states of the component.
         * @type {{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, File: {audio: string, video: string}}}
         */
        this.state = {
            uniform_resource_locator: "",
            author: "",
            title: "",
            identifier: "",
            author_channel: "",
            views: "",
            published_at: "",
            thumbnail: "",
            duration: "",
            File: {
                audio: "",
                video: "",
            }
        };
    }

    componentDidMount() {
        this.getRoute();
        setTimeout(() => {
            if (window.location.pathname != "/Search/") {
                this.getMedia();
            }
        }, 1);
    }

    /**
     * Checking that the location of the media file needed is in
     * the state of the application.
     * @returns {string|void}
     */
    verifyFile() {
        if (this.state.File.video != null) {
            return this.getMediaFile();
        }
        window.location.href = `/Search/${this.state.identifier}`;
    }

    /**
     * Sending the request to the server to download the file
     * needed.
     * @param {string} file_location The location of the file.
     * @param {string} file_name The name of the file.
     * @returns {Promise<Blob>}
     */
    async downloadFileServer(file_location, file_name) {
        const response = await fetch("/Download", {
            method: "POST",
            body: JSON.stringify({
                file: file_location,
                file_name: file_name,
            }),
            headers: {
                "Content-Type": "application/json",
            },
        });
        return await response.blob();
    }

    /**
     * Downloading the file retrieved from the server.
     * @param {MouseEvent} event
     * @returns {void}
     */
    getFile(event) {
        const button = event.target.parentElement.parentElement;
        const file_location = button.value;
        const file_name = (file_location.includes("/Public/Audio/")) ? `${this.state.title}.mp3` : `${this.state.title}.mp4`;
        this.downloadFileServer(file_location, file_name)
        .then((data) => {
            let a = document.createElement("a");
            a.href = window.URL.createObjectURL(data);
            a.download = file_name;
            a.click();
        });
    }

    /**
     * Rendering the component for the YouTube downloader.
     * @returns {HTMLDivElement}
     */
    render() {
        return (
            <div class="YouTube">
                <div>
                    <video src={this.verifyFile()} controls autoplay></video>
                </div>
                <div>
                    <button
                        name="file_downloader"
                        value={this.state.File.audio}
                        onClick={this.getFile.bind(this)}
                    >
                        <i class="fa-solid fa-music"></i>
                    </button>
                </div>
                <div>
                    <button
                        name="file_downloader"
                        value={this.state.File.video}
                        onClick={this.getFile.bind(this)}
                    >
                        <i class="fa-solid fa-video"></i>
                    </button>
                </div>
            </div>
        );
    }
}