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
     * Initializing the component's state based on data from localStorage and sets up tracking.
     * 
     * - Retrieves the `media` object from localStorage.
     * - Updates component state with media metadata if available.
     * - Displays the loading icon.
     * - Sets up the `tracker` if available on the global `window` object.
     * - Triggers file verification if data is successfully loaded.
     * @returns {void}
     */
    setData() {
        const loading_icon = document.querySelector("#loading");
        const local_storage_data = localStorage.getItem("media");
        let media = null;
        if (typeof local_storage_data === "string") {
            try {
                media = JSON.parse(localStorage.getItem("media")).data;
            } catch (error) {
                console.error(`The application has failed to parse the data.\nError: ${error.message}`);
            }
        } else {
            media = null;
        }
        const data_loaded = (media != null && window.Tracker);
        loading_icon.style.display = "flex";
        this.setState((previous) => ({
            ...previous,
            uniform_resource_locator: (media) ? media.uniform_resource_locator : previous.uniform_resource_locator,
            author: (media) ? media.author : previous.author,
            title: (media) ? media.title : previous.title,
            identifier: (media) ? media.identifier : previous.identifier,
            author_channel: (media) ? media.author_channel : previous.author_channel,
            views: (media) ? media.views : previous.views,
            published_at: (media) ? media.published_at : previous.published_at,
            thumbnail: (media) ? media.thumbnail : previous.thumbnail,
            duration: (media) ? media.duration : previous.duration,
            File: {
                ...previous.File,
                audio: (media) ? media.audio : previous.File.audio,
                video: (media) ? media.video : previous.File.video,
            },
            data_loaded: data_loaded,
        }));
        this.tracker = (window.Tracker) ? window.Tracker : null;
        if (data_loaded) {
            this.verifyFile(loading_icon);
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
     * Processing the video status returned by the server and determines the final media file path or redirect uniform resource locator.
     * 
     * - If the status is not `200`, it returns a redirect path to the search page.
     * - If the status is `200`, it processes and returns a cleaned-up path for the video file,
     *   removing internal server paths based on known directory locations.
     * 
     * @param {number} status - HTTP status code indicating the availability of the video.
     * @returns {Promise<string>} A promise resolving to the processed video file path or search redirection URL.
     */
    async handleVideoStatus(status) {
        if (status != 200) {
            const identifier = window.location.pathname.replace("/Download/YouTube/", "");
            return `/Search/${identifier}`;
        }
        const video_path = this.state.File.video;
        return (video_path.includes("extractio")) ? video_path.replace("/home/darkness4869/Documents/extractio", "") : video_path.replace("/var/www/html/ytd_web_app", "");
    }

    /**
     * Verifying the existence and accessibility of the media file based on the uniform resource locator path, then updates the component state with the media file's location if available.
     * @param {HTMLDivElement} loading_icon - The DOM element representing the loading indicator.
     * @returns {void}
     */
    verifyFile(loading_icon) {
        const path_name = window.location.pathname;
        identifier = (path_name.includes("/Shorts/")) ? path_name.replace("/Download/YouTube/Shorts/", "") : path_name.replace("/Download/YouTube/", "");
        this.checkVideoStatus(identifier)
        .then((status) => this.handleVideoStatus(status, loading_icon))
        .then((route) => this.manageRoute(route, loading_icon));
        .then((uniform_resource_locator) => this.setState((previous) => ({
            ...previous,
            File: {
                ...previous.File,
                uniform_resource_locator: uniform_resource_locator,
            },
        })));
    }

    /**
     * Determining whether the given route is a search redirect or a valid media file path, then updates the component state or redirects accordingly.
     * 
     * - If the route is a search path, the browser navigates to that route.
     * - Otherwise, the loading icon is hidden and the state is updated with the file's uniform resource locator.
     * @param {string} route - Either a search route or a direct file path.
     * @param {HTMLDivElement} loading_icon - The DOM element representing the loading indicator.
     * @returns {void}
     */
    manageRoute(route, loading_icon) {
        if (route.includes("/Search/")) {
            window.location.href = route;
            return;
        }
        loading_icon.style.display = "none";
        this.setState((previous) => ({
            ...previous,
            File: {
                ...previous.File,
                uniform_resource_locator: route,
            },
        }));
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
