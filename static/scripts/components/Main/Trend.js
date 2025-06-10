import React, { Component } from "react";
import MainUtilities from "../utilities/Main";


/**
 * The component to be rendered for the trends.
 */
class Trend extends Component {
    /**
     * Constructing the Trend component which is will render the trend list.
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        /**
         * The states of the component.
         * @type {{Trend: [{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}], System: {data_loaded: boolean}}}
         */
        this.state = {
            Trend: [],
            System: {
                data_loaded: false,
            },
        };
        /**
         * The tracker class which will track the user's activity on
         * the application.
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
     * Updating the component as soon as there is an update in the states.
     * @returns {void}
     */
    componentDidUpdate() {
        if (!this.state.System.data_loaded) {
            setTimeout(() => this.setData(), 1000);
        }
    }

    /**
     * Updating the component state with trend data retrieved from localStorage.
     * 
     * This method accesses trend data using `main_utilities.getTrends()`, and if the data is fully loaded, it updates the component state with the retrieved trend information.  Additionally, it initializes the `tracker` property with the global `window.Tracker` and hides the loading icon in the DOM.
     * @returns {void}
     */
    setData() {
        const loading_icon = document.querySelector("#loading");
        const {trend, data_loaded} = this.main_utilities.getTrends();
        if (!data_loaded) {
            return;
        }
        this.setState((previous) => ({
            ...previous,
            Trend: trend,
            System: {
                ...previous.System,
                data_loaded: data_loaded,
            },
        }));
        this.tracker = window.Tracker;
        loading_icon.style.display = "none";
        console.info("Component: Trend\nStatus: Loaded");
    }

    /**
     * Handling click events, tracking the event and opening the link in a new tab.
     *
     * This method prevents the default behavior of the event, extracts the URL from the clicked anchor (`<a>`) element or its parent, and sends a tracking event.  If the tracking event is successfully sent, the URL is opened in a new tab.  If an error occurs, it logs the error and refreshes the page after a delay.
     * @param {MouseEvent} event The click event object.
     * @returns {void}
     * @throws {Error} If an issue occurs while sending the tracking event.
     */
    handleClick(event) {
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
     * Rendering the media card.
     * @param {{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}} content
     * @return {React.JSX.Element}
     */
    renderMediaCard(content) {
        const width = (window.innerWidth < 640) ? 179 : 1280;
        const height = (window.innerWidth < 640) ? 101 : 720;
        const identifier = this.decodeHtmlEntities(content.identifier);
        const uniform_resource_locator = this.decodeHtmlEntities(content.uniform_resource_locator);
        const thumbnail = this.decodeHtmlEntities(content.thumbnail);
        const title = this.decodeHtmlEntities(content.title);
        const author_channel = this.decodeHtmlEntities(content.author_channel);
        const author = this.decodeHtmlEntities(content.author);
        const duration = this.decodeHtmlEntities(content.duration);
        return (
            <div className="card" key={identifier}>
                <div>
                    <a href={uniform_resource_locator} target="__blank" onClick={this.handleClick.bind(this)}>
                        <img src={thumbnail} loading="lazy" alt={`Thumbnail for ${title}`}  width={width} height={height} sizes="(max-width: 640px) 179px, (min-width: 641px) 1280px" />
                    </a>
                </div>
                <div>
                    <div>{title}</div>
                    <div>
                        <a href={author_channel} target="__blank" onClick={this.handleClick.bind(this)}>{author}</a>
                    </div>
                    <div>
                        <div>Duration:</div>
                        <div>{duration}</div>
                    </div>
                    <div>
                        <div>Views:</div>
                        <div>
                            {content.views.toLocaleString("en-US")}
                        </div>
                    </div>
                    <div>
                        <a href={`/Download/YouTube/${identifier}`} target="__blank" onClick={this.handleClick.bind(this)}>
                            <i className="fa-solid fa-download"></i>
                        </a>
                    </div>
                </div>
            </div>
        );
    }

    /**
     * Rendering the component
     * @returns {React.JSX.Element}
     */
    render() {
        const delay = 8;
        const width = (window.innerWidth < 640) ? `${window.innerWidth * this.state.Trend.length}px` : `${window.innerWidth}px`;
        const animation = (window.innerWidth < 640) ? `trend-scroll ${delay * this.state.Trend.length}s linear infinite` : "none";
        return (
            <div className="Trend">
                <div style={{width: width, animation: animation}} onMouseEnter={(event) => this.main_utilities.handleTrendListMouseEnter(event)} onMouseLeave={(event) => this.main_utilities.handleTrendListMouseLeave(event)}>
                    {this.state.Trend.map((content) => this.renderMediaCard(content))}
                </div>
            </div>
        );
    }
}

export default Trend;
