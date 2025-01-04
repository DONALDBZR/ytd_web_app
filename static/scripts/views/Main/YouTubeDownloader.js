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

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setData();
        console.info(`Route: ${window.location.pathname}\nComponent: Download.Main.MainDownload.YouTubeDownloader\nComponent Status: Mount`);
    }

    /**
     * Setting the main state of the component.
     * @returns {void}
     */
    setData() {
        const loading_icon = document.querySelector("#loading");
        const media = JSON.parse(localStorage.getItem("media")).data;
        this.setState((previous) => ({
            ...previous,
            uniform_resource_locator: media.uniform_resource_locator,
            author: media.author,
            title: media.title,
            identifier: media.identifier,
            author_channel: media.author_channel,
            views: media.views,
            published_at: media.published_at,
            thumbnail: media.thumbnail,
            duration: media.duration,
            File: {
                audio: media.audio,
                video: media.video,
            },
        }));
        loading_icon.style.display = "none";
    }

    /**
     * Checking that the location of the media file needed is in
     * the state of the application.
     * @returns {string|void}
     */
    verifyFile() {
        if (this.state.File.video != null) {
            return (this.state.File.video.includes("extractio")) ? this.state.File.video.replace("/home/darkness4869/Documents/extractio", "") : this.state.File.video.replace("/var/www/html/ytd_web_app", "");
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
     * Creating the file needed that is generated from the blob
     * retrieved from the server to be downloaded.
     * @param {Blob} data The data in the form of a blob.
     * @param {string} file_name The name of the file.
     * @returns {void}
     */
    downloadFileClient(data, file_name) {
        const a = document.createElement("a");
        a.href = window.URL.createObjectURL(data);
        a.download = file_name;
        a.click();
    }

    /**
     * Downloading the file retrieved from the server.
     * @param {MouseEvent} event The on-click event.
     * @returns {void}
     */
    getFile(event) {
        const button = event.target.parentElement.parentElement;
        const file_location = button.value;
        const file_name = (file_location.includes("/Public/Audio/")) ? `${this.state.title}.mp3` : `${this.state.title}.mp4`;
        this.downloadFileServer(file_location, file_name)
        .then((data) => this.downloadFileClient(data, file_name));
    }

    /**
     * Rendering the component for the YouTube downloader.
     * @returns {React.Component}
     */
    render() {
        return (
            <div class="YouTube">
                <div id="video">
                    <video src={this.verifyFile()} controls autoplay></video>
                </div>
                <div>
                    <div id="title">
                        <a href={this.state.uniform_resource_locator} target="__blank">{this.state.title}</a>
                    </div>
                    <div id="author">
                        <a href={this.state.author_channel} target="__blank">{this.state.author}</a>
                    </div>
                    <div>
                        <div id="actions">
                            <div id="metrics">
                                <div id="duration">
                                    <div class="label">Duration:</div>
                                    <div class="data">{this.state.duration}</div>
                                </div>
                                <div id="views">
                                    <div class="label">Views:</div>
                                    <div class="data">{this.state.views}</div>
                                </div>
                            </div>
                            <div id="buttons">
                                <div class="button">
                                    <button name="file_downloader" value={this.state.File.audio} onClick={this.getFile.bind(this)}>
                                        <i class="fa-solid fa-music"></i>
                                    </button>
                                </div>
                                <div class="button">
                                    <button name="file_downloader" value={this.state.File.video} onClick={this.getFile.bind(this)}>
                                        <i class="fa-solid fa-video"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div></div>
                    </div>
                </div>
            </div>
        );
    }
}