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
     * Parsing and validating media metadata from localStorage.
     * 
     * - Attempts to parse the provided JSON string and extract the `data` property.
     * - If parsing fails, logs the error and rethrows it as a new `Error`.
     * @param {?string} local_storage_data The data from the local storage.
     * @returns {{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio: ?string, video: ?string}}
     * @throws {Error} If the JSON cannot be parsed or does not match expected structure.
     */
    getMedia(local_storage_data) {
        try {
            const parsed_data = JSON.parse(local_storage_data);
            return parsed_data.data;
        } catch (error) {
            console.error(`The application has failed to parse the data.\nError: ${error.message}`);
            throw new Error(error.message);
        }
    }

    /**
     * Initializing the component's state using media metadata stored in `localStorage`, sets up tracking, and triggers media file verification.
     * 
     * - Attempts to retrieve and parse the `media` object from localStorage via `getMedia()`.
     * - If parsing fails, logs the error and skips data initialization.
     * - If parsing succeeds:
     *    - Updates the component state with media details.
     *    - Shows the loading icon.
     *    - Sets the global `Tracker` reference if available.
     *    - Triggers file verification.
     * @returns {void}
     */
    setData() {
        try {
            const loading_icon = document.querySelector("#loading");
            const local_storage_data = localStorage.getItem("media");
            const media = (typeof local_storage_data == "string") ? this.getMedia(local_storage_data) : null;
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
            (data_loaded) ? this.verifyFile(loading_icon) : null;
        } catch (error) {
            console.error(`The application has failed to initialize the data.\nError: ${error.message}`);
        }
    }

    /**
     * Sending a request to check the availability of a video file on the server.
     * 
     * - Determines the appropriate video path based on the current uniform resource locator structure (Shorts or regular).
     * - Performs a fetch request to that path.
     * - Returns the HTTP status code to indicate the video's availability.
     * @param {string} identifier - The unique identifier of the video.
     * @returns {Promise<number>} A promise that resolves to the HTTP status code of the video resource.
     */
    async checkVideoStatus(identifier) {
        const query = (window.location.pathname.includes("/Shorts/")) ? `/Public/Video/Shorts/${identifier}.mp4` : `/Public/Video/${identifier}.mp4`;
        try {
            const response = await fetch(query);
            return response.status;
        } catch (error) {
            console.error(`There is an error while retrieving the video status.\nError: ${error.message}`);
            return 500;
        }
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
     * Verifying the existence and accessibility of the media file by checking the current uniform resource locator path.
     * 
     * - Extracts a media identifier from the uniform resource locator.
     * - Checks the video status from the server.
     * - Handles the video status to determine the correct route (file path or search redirect).
     * - Manages the result by either updating the component state or redirecting the user.
     * @param {HTMLDivElement} loading_icon - The DOM element representing the loading indicator.
     * @returns {void}
     */
    verifyFile(loading_icon) {
        const path_name = window.location.pathname;
        const identifier = (path_name.includes("/Shorts/")) ? path_name.replace("/Download/YouTube/Shorts/", "") : path_name.replace("/Download/YouTube/", "");
        this.checkVideoStatus(identifier)
        .then((status) => this.handleVideoStatus(status, loading_icon))
        .then((route) => this.manageRoute(route, loading_icon));
    }

    /**
     * Determining if the given route is a search redirect or a valid media file path, then either navigates to the search page or updates the component state with the file path.
     * 
     * - If the route contains "/Search/", the browser is redirected to that route.
     * - Otherwise, the loading icon is hidden and the state is updated with the corrected file uniform resource locator.
     * - Adjusts the route casing for Shorts uniform resource locators to maintain consistency.
     * @param {string} route - A uniform resource locator route, either a search path or a direct media file path.
     * @param {HTMLDivElement} loading_icon - The DOM element representing the loading indicator.
     * @returns {void}
     */
    manageRoute(route, loading_icon) {
        if (route.includes("/Search/")) {
            window.location.href = route;
            return;
        }
        const file_path = (window.location.pathname.includes("/Shorts/")) ? route.replace("/shorts/", "/Shorts/") : route;
        loading_icon.style.display = "none";
        this.setState((previous) => ({
            ...previous,
            File: {
                ...previous.File,
                uniform_resource_locator: file_path,
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
     * Rendering a download button based on the media file type and current route.
     * 
     * - Determines whether the file is an Audio or Video resource from the path.
     * - If the file is Audio and the current route is a Shorts uniform resource locator, the button is not rendered.
     * - Otherwise, returns a styled download button with an appropriate icon.
     * @param {string} file_path - The full path to the downloadable media file.
     * @returns {React.JSX.Element | void} A JSX element representing the button, or nothing if suppressed.
     */
    renderButton(file_path) {
        const type = (file_path.includes("/Audio/")) ? "Audio" : "Video";
        if (window.location.pathname.includes("/Shorts/") && type == "Audio") {
            return;
        }
        return (
            <div className="button">
                <button name="file_downloader" value={file_path} onClick={this.getFile.bind(this)}>
                    {this.renderDownloadIcon(type)}
                </button>
            </div>
        );
    }

    /**
     * Returning a Font Awesome icon element based on the type of the media file.
     * 
     * - For `"Audio"` type, a music icon is rendered.
     * - For `"Video"` type, a video icon is rendered.
     * @param {string} type - The type of the media file.
     * @returns {React.JSX.Element} A JSX `<i>` element with the appropriate Font Awesome classes.
     */
    renderDownloadIcon(type) {
        const class_name = (type === "Audio") ? "fa-solid fa-music" : "fa-solid fa-video";
        return <i className={class_name}></i>;
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
                                {this.renderButton(this.state.File.audio)}
                                {this.renderButton(this.state.File.video)}
                            </div>
                        </div>
                    </div>
                </div>
            );
        }
    }
}

export default YouTubeDownloader;
