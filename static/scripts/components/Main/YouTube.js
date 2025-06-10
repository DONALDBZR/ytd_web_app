import React, { Component } from "react";
import MainUtilities from "../utilities/Main";


/**
 * The component that is the YouTube component given that it will only be rendered only when the data corresponds to it.
 */
class YouTube extends Component {
    /**
     * Constructing the YouTube component which will render the data of the video from YouTube.
     * @param {*} props
     */
    constructor(props) {
        super(props);
        /**
         * The data for the properties of the Search component.
         * @type {{Media: {YouTube: {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}}, System: {data_loaded: boolean}}}
         */
        this.state = {
            Media: {
                YouTube: {
                    uniform_resource_locator: "",
                    author: "",
                    title: "",
                    identifier: "",
                    author_channel: "",
                    views: 0,
                    published_at: "",
                    thumbnail: "",
                    duration: "",
                    audio_file: "",
                    video_file: ""
                },
            },
            System: {
                data_loaded: false,
            },
        };
        /**
         * The tracker class which will track the user's activity on the application.
         * @type {Tracker}
         */
        this.tracker = null;
        /**
         * The utility class of the Main component.
         * @type {MainUtilities}
         */
        this.main_utilities = new MainUtilities();
    }

    /**
     * Running the methods needed as soon as the component has been successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setData();
    }

    /**
     * The methods to be executed when the component has been updated.
     * @returns {void}
     */
    componentDidUpdate() {
        if (!this.state.System.data_loaded) {
            setTimeout(() => this.setData(), 1000);
        }
    }

    /**
     * Setting the main state of the component with media metadata from `localStorage`.
     * 
     * This method retrieves media metadata using `main_utilities.getMedia()`.  If the data is fully loaded, it updates the component's state with the media under `Media.YouTube`, updates the system's `data_loaded` flag, initializes the `tracker`, hides the loading icon, and logs the load status to the console.
     * @returns {void}
     */
    setData() {
        const loading_icon = document.querySelector("#loading");
        const {media, data_loaded} = this.main_utilities.getMedia();
        if (!data_loaded) {
            return;
        }
        this.setState((previous) => ({
            ...previous,
            Media: {
                ...previous.Media,
                YouTube: media,
            },
            System: {
                ...previous.System,
                data_loaded: data_loaded,
            },
        }));
        this.tracker = window.Tracker;
        loading_icon.style.display = "none";
        console.info(`Route: ${window.location.pathname}\nComponent: YouTube\nData Status: Loaded`);
    }

    /**
     * Clearing specific `localStorage` entries if the HTTP status indicates a successful response.
     * 
     * This function removes the `media` and `related_content` keys from `localStorage` only if the provided status is exactly 200.  If the status differs, no action is taken.
     * @param {number} status - The HTTP status code returned from the server.
     * @returns {void}
     */
    clearLocalStorage(status) {
        if (status == 201) {
            localStorage.removeItem("media");
            localStorage.removeItem("related_content");
        }
    }

    /**
     * Handling application flow based on the server's response.
     * 
     * Clears local storage if applicable, then redirects the user after a specified delay.  If the response status is `201`, the user is redirected to the provided download uniform resource locator.  For any other status, the user is redirected to the current page. If an error occurs during processing, it logs the error and rethrows it.
     * @param {{status: number, uniform_resource_locator: string}} response - The response object from the backend, including HTTP status and redirect uniform resource locator.
     * @param {number} delay - The delay (in milliseconds) before redirecting the user.
     * @returns {void}
     * @throws {Error} Throws an error if the application fails to process the response.
     */
    manageResponse(response, delay) {
        try {
            this.clearLocalStorage(response.status);
            const uniform_resource_locator = (response.status == 201) ? response.uniform_resource_locator : window.location.href;
            this.redirector(delay, uniform_resource_locator);
        } catch (error) {
            console.error(`There is an error while processing the response.\nError: ${error.message}`);
            throw new Error(error.message);
        }
    }

    /**
     * Sending a POST request to the server to initiate the download of a media file.
     * 
     * Constructs the YouTube media uniform resource locator based on the media type and sends it to the backend endpoint with metadata.  Returns a simplified object containing the HTTP status code and the uniform resource locator to which the user can be redirected to access the media.
     * @param {string} platform - The supported platform.
     * @param {string} type - The type of media.
     * @param {string} identifier - The unique media identifier.
     * @returns {Promise<{status: number, uniform_resource_locator: string}>} A promise that resolves with the server response status and download route.
     * @throws {Error} Throws an error if the request fails or JSON parsing fails.
     */
    async postMediaDownload(platform, type, identifier) {
        const query = "/Media/Download";
        const youtube_uniform_resource_locator = (type == "Shorts") ? `https://www.youtube.com/shorts/${identifier}`: `https://www.youtube.com/watch?v=${identifier}`;
        try {
            const response = await fetch(query, {
                method: "POST",
                body: JSON.stringify({
                    Media: {
                        uniform_resource_locator: youtube_uniform_resource_locator,
                        platform: platform,
                        type: type,
                        identifier: identifier,
                    },
                }),
                headers: {
                    "Content-Type": "application/json",
                },
            });
            const data = await response.json();
            const uniform_resource_locator = (response.status == 201) ? ((type == "Shorts") ? `/Download/YouTube/Shorts/${data.identifier.replaceAll("shorts/", "")}` : `/Download/YouTube/${data.identifier}`) : "/";
            return {
                status: response.status,
                uniform_resource_locator: uniform_resource_locator,
            };
        } catch (error) {
            console.error(`There is an issue while downloading the file.\nError: ${error.message}`);
            throw new Error(error.message);
        }
    }

    /**
     * Redirecting the user to an intended uniform resource locator.
     * @param {number} delay The amount of time in milliseconds before firing the method
     * @param {string} uniform_resource_locator The route
     * @returns {void}
     */
    redirector(delay, uniform_resource_locator) {
        setTimeout(() => {
            window.location.href = uniform_resource_locator;
        }, delay);
    }

    /**
     * Retrieving the height of the component for the title.
     * @param {string} title The title of the media content.
     * @returns {string}
     */
    getTitleHeight(title) {
        if (window.outerWidth < 640) {
            return this.__getTitleHeight(51, 8.98, title);
        }
        if (window.outerWidth >= 640 && window.outerWidth < 1024) {
            return this.__getTitleHeight(82, 6.495, title);
        }
        return this.__getTitleHeight(62, 8.38, title);
    }

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
        return `calc(var(--metadata-height) / ${height_coefficient})`;
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
            this.redirector(delay, window.location.href);
        });
    };

    /**
     * Decoding HTML entities in a given string.
     * 
     * This function takes a string that may contain HTML entities and returns the decoded version.  It uses a temporary `textarea` element to leverage the browser's parsing capabilities.
     * @param {string} encoded_string - The string potentially containing HTML entities.
     * @returns {string}
     */
    decodeHtmlEntities(encoded_string) {
        if (typeof encoded_string !== "string") {
            console.warn(`Component: Trend\nMessage: The data is not a string.\nData: ${encoded_string}`);
            return encoded_string;
        }
        const text_area = document.createElement("textarea");
        text_area.innerHTML = encoded_string;
        return text_area.value;
    }

    /**
     * Rendering the component
     * @returns {React.JSX.Component}
     */
    render() {
        if (this.state.System.data_loaded) {
            const title = this.decodeHtmlEntities(this.state.Media.YouTube.title);
            return (
                <div className="YouTube">
                    <div>
                        <a href={this.state.Media.YouTube.uniform_resource_locator} target="__blank" onClick={this.handleClick.bind(this)}>
                            <img src={this.state.Media.YouTube.thumbnail} />
                        </a>
                    </div>
                    <div class="data">
                        <div class="metadata">
                            <div style={{height: this.getTitleHeight(title)}}>{title}</div>
                            <div>
                                <a href={this.state.Media.YouTube.author_channel} target="__blank" onClick={this.handleClick.bind(this)}>{this.state.Media.YouTube.author}</a>
                            </div>
                            <div>
                                <div id="duration">
                                    <div>Duration:</div>
                                    <div>{this.state.Media.YouTube.duration}</div>
                                </div>
                                <div id="views">
                                    <div>Views:</div>
                                    <div>{this.state.Media.YouTube.views.toLocaleString("en-US")}</div>
                                </div>
                            </div>
                        </div>
                        <div>
                            <button name="mediaDownloader" value={this.state.Media.YouTube.uniform_resource_locator} onClick={this.retrieveMedia.bind(this)}>
                                <i class="fa-solid fa-download"></i>
                            </button>
                        </div>
                    </div>
                </div>
            );
        }
    }
}

export default YouTube;
