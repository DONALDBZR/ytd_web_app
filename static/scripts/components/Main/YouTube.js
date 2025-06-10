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
     * Setting the main state of the component with media metadata from `localStorage`.
     * 
     * This method retrieves media metadata using `main_utilities.getMedia()`.  If the data is fully loaded, it updates the component's state with the media under `Media.YouTube`, updates the system's `data_loaded` flag, initializes the `tracker`, hides the loading icon, and logs the load status to the console.
     * @returns {void}
     */
    setData() {
        const loading_icon = document.querySelector("#loading");
        if (this.state.System.data_loaded) {
            console.info(`Route: ${window.location.pathname}\nComponent: YouTube\nStatus: Loaded`);
            loading_icon.style.display = "none";
            return;
        }
        this.getData();
    }

    /**
     * Retrieving the data from the `localStorage` to be set as the states of the application.
     * @returns {void}
     */
    getData() {
        const {media, data_loaded} = this.main_utilities.getMedia();
        const delay = 1000;
        if (!data_loaded) {
            setTimeout(() => this.setData(), delay);
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
        setTimeout(() => this.setData(), delay);
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
     * Rendering the component
     * @returns {React.JSX.Component}
     */
    render() {
        if (this.state.System.data_loaded) {
            const title = this.main_utilities.decodeHtmlEntities(this.state.Media.YouTube.title);
            return (
                <div className="YouTube">
                    <div>
                        <a
                            href={this.state.Media.YouTube.uniform_resource_locator}
                            target="__blank"
                            onClick={(event) => this.main_utilities.handleClick(event, this.tracker)}
                        >
                            <img src={this.state.Media.YouTube.thumbnail} />
                        </a>
                    </div>
                    <div class="data">
                        <div class="metadata">
                            <div style={{height: this.getTitleHeight(title)}}>{title}</div>
                            <div>
                                <a
                                    href={this.state.Media.YouTube.author_channel}
                                    target="__blank"
                                    onClick={(event) => this.main_utilities.handleClick(event, this.tracker)}
                                >
                                    {this.state.Media.YouTube.author}
                                </a>
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
                            <button
                                name="mediaDownloader"
                                value={this.state.Media.YouTube.uniform_resource_locator}
                                onClick={(event) => this.main_utilities.retrieveMedia(event, this.state.Media.YouTube.uniform_resource_locator, this.tracker)}
                            >
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
