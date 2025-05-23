import React, { Component } from "react";


/**
 * The component to be rendered for the Download page but only
 * when it is for media from YouTube.
 */
class YouTubeDownloader extends Component {
    /**
     * Constructing the downloader component for YouTube media.
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        /**
         * The states of the component.
         * @type {{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, File: {audio: string, video: string, uniform_resource_locator: string}, data_loaded: boolean}}
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
                uniform_resource_locator: "",
            },
            data_loaded: false,
        };
        /**
         * The tracker class which will track the user's activity on
         * the application.
         * @type {Tracker}
         */
        this.tracker = null;
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
     * The methods to be executed when the component has been
     * updated.
     * @returns {void}
     */
    componentDidUpdate() {
        if (!this.state.data_loaded) {
            setTimeout(() => {
                this.setData();
                console.info(`Route: ${window.location.pathname}\nComponent: Download.Main.MainDownload.YouTubeDownloader\nComponent Status: Update`);
            }, 2000);
        }
    }

    /**
     * Setting the main state of the component.
     * @returns {void}
     */
    setData() {
        const loading_icon = document.querySelector("#loading");
        const local_storage_data = localStorage.getItem("media");
        const media = (typeof local_storage_data == "string") ? JSON.parse(localStorage.getItem("media")).data : null;
        const data_loaded = (media != null && window.Tracker);
        this.setState((previous) => ({
            ...previous,
            uniform_resource_locator: (media) ? media.uniform_resource_locator : this.state.uniform_resource_locator,
            author: (media) ? media.author : this.state.author,
            title: (media) ? media.title : this.state.title,
            identifier: (media) ? media.identifier : this.state.identifier,
            author_channel: (media) ? media.author_channel : this.state.author_channel,
            views: (media) ? media.views : this.state.views,
            published_at: (media) ? media.published_at : this.state.published_at,
            thumbnail: (media) ? media.thumbnail : this.state.thumbnail,
            duration: (media) ? media.duration : this.state.duration,
            File: {
                ...previous.File,
                audio: (media) ? media.audio : this.state.File.audio,
                video: (media) ? media.video : this.state.File.video,
            },
            data_loaded: data_loaded,
        }));
        this.tracker = (window.Tracker) ? window.Tracker : null;
        if (data_loaded) {
            loading_icon.style.display = "none";
            this.verifyFile();
        }
    }

    /**
     * Checking the video status from the server.
     * @param {string} identifier The identifier of the video.
     * @returns {Promise<number>}
     */
    async checkVideoStatus(identifier) {
        const response = await fetch(`/Public/Video/${identifier}.mp4`);
        return response.status;
    }

    /**
     * Handling the status of the video that is returned by the
     * server.
     * @param {number} status The status of the video
     * @returns {Promise<string>}
     */
    async handleVideoStatus(status) {
        if (status != 200) {
            window.location.href = `/Search/${window.location.pathname.replace("/Download/YouTube/", "")}`;
            return "";
        }
        return (this.state.File.video.includes("extractio")) ? this.state.File.video.replace("/home/darkness4869/Documents/extractio", "") : this.state.File.video.replace("/var/www/html/ytd_web_app", "");
    }

    /**
     * Checking that the location of the media file needed is in
     * the state of the application.
     * @returns {string}
     */
    verifyFile() {
        this.checkVideoStatus(window.location.pathname.replace("/Download/YouTube/", ""))
        .then((status) => this.handleVideoStatus(status))
        .then((uniform_resource_locator) => this.setState((previous) => ({
            ...previous,
            File: {
                ...previous.File,
                uniform_resource_locator: uniform_resource_locator,
            },
        })));
    }

    /**
     * Sending the request to the server to download the file
     * needed.
     * @param {string} file_location The location of the file.
     * @param {string} file_name The name of the file.
     * @returns {Promise<Blob>}
     */
    async downloadFileServer(file_location, file_name) {
        try {
            const response = await fetch("/Download/", {
                method: "POST",
                body: JSON.stringify({
                    file: file_location,
                    file_name: file_name,
                }),
                headers: {
                    "Content-Type": "application/json",
                },
            });
            if (!response.ok) {
                throw new Error(`Failed to download file: ${response.statusText}`);
            }
            const reader = response.body.getReader();
            const chunks = [];
            let done = false;
            while (!done) {
                const {value, done: is_done} = await reader.read();
                done = is_done;
                if (value) {
                    chunks.push(value);
                }
            }
            const blob = new Blob(chunks);
            return blob;
        } catch (error) {
            console.error("Fetch Error: ", error);
            throw error;
        }
    }

    /**
     * Creating the file needed that is generated from the blob
     * retrieved from the server to be downloaded.
     * @param {Blob} data The data in the form of a blob.
     * @param {string} file_name The name of the file.
     * @returns {void}
     */
    downloadFileClient(data, file_name) {
        try {
            const uniform_resource_locator = URL.createObjectURL(data);
            const a = document.createElement("a");
            a.href = uniform_resource_locator;
            a.download = file_name;
            a.click();
            URL.revokeObjectURL(uniform_resource_locator);
        } catch (error) {
            console.error("Download Failed: ", error);
        }
    }

    /**
     * Downloading the file retrieved from the server.
     * @param {MouseEvent} event The on-click event.
     * @returns {void}
     */
    getFile(event) {
        const button = event.target.parentElement;
        const file_location = button.value;
        const file_name = (file_location.includes("/Public/Audio/")) ? `${this.state.title}.mp3` : `${this.state.title}.mp4`;
        const uniform_resource_locator = (file_location.includes("/Public/Audio/")) ? `/Public/Audio/${this.state.identifier}.mp3` : `/Public/Video/${this.state.identifier}.mp4`;
        this.tracker.sendEvent("click", {
            uniform_resource_locator: uniform_resource_locator,
        })
        .then(() => {
            return this.downloadFileServer(file_location, file_name);
        })
        .then((data) => this.downloadFileClient(data, file_name))
        .catch((error) => console.error("Download Failed: ", error));
    }

    /**
     * Handles the click event on a component.
     * @param {MouseEvent} event The click event.
     * @returns {void}
     */
    handleClick = (event) => {
        event.preventDefault();
        const uniform_resource_locator = (String(event.target.localName) == "a") ? String(event.target.href) : String(event.target.parentElement.href);
        this.tracker.sendEvent("click", {
            uniform_resource_locator: uniform_resource_locator,
        })
        .then(() => {
            window.open(uniform_resource_locator, "_blank");
        })
        .catch((error) => {
            console.error("An error occurred while sending the event or setting the route!\nError: ", error);
            setTimeout(() => {
                window.location.href = window.location.href;
            }, delay);
        });
    };

    /**
     * Calculating the height of the title based on its length and the height of the component.
     * @param {number} limit The amount of characters per line.
     * @param {number} component_height_coefficient The height co-efficient of the component.
     * @param {string} title The title of the component.
     * @returns {string}
     */
    __getTitleHeight(limit, component_height_coefficient, title) {
        const coefficient = (title.length <= limit) ? 1 : Math.ceil(title.length / limit);
        const height_coefficient = component_height_coefficient / coefficient;
        return `calc(var(--data-height) / ${height_coefficient})`;
    }

    /**
     * Retrieving the height of the component for the title.
     * @param {string} title The title of the media content.
     * @returns {string}
     */
    getTitleHeight(title) {
        if (window.outerWidth < 640) {
            return this.__getTitleHeight(51, 7.782, title);
        }
        if (window.outerWidth >= 640 && window.outerWidth < 1024) {
            return this.__getTitleHeight(82, 12.79, title);
        }
        return "calc(var(--data-height) / 4)";
    }

    /**
     * Rendering the component for the YouTube downloader.
     * @returns {React.JSX.Element}
     */
    render() {
        if (this.state.data_loaded) {
            return (
                <div class="YouTube">
                    <div id="video">
                        <video src={this.state.File.uniform_resource_locator} controls autoplay></video>
                    </div>
                    <div id="data">
                        <div id="title" style={{"--title-height": this.getTitleHeight(this.state.title)}}>
                            <a href={this.state.uniform_resource_locator} target="__blank" onClick={this.handleClick.bind(this)}>{this.state.title}</a>
                        </div>
                        <div id="author">
                            <a href={this.state.author_channel} target="__blank" onClick={this.handleClick.bind(this)}>{this.state.author}</a>
                        </div>
                        <div id="actions">
                            <div id="metrics">
                                <div id="duration">
                                    <div class="label">Duration:</div>
                                    <div class="data">{this.state.duration}</div>
                                </div>
                                <div id="views">
                                    <div class="label">Views:</div>
                                    <div class="data">{this.state.views.toLocaleString("en-US")}</div>
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
                    </div>
                </div>
            );
        }
    }
}

export default YouTubeDownloader;
