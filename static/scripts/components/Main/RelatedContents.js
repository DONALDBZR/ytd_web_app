import React, { Component } from "react";
import MainUtilities from "../utilities/Main";


/**
 * The component that will render the contents that are related to the content that is currently being displayed where the identifier of content is related to them.
 */
class RelatedContents extends Component {
    /**
     * Constructing the component given that it will only render the related contents.
     * @param {*} props The properties of the component.
     */
    constructor(props) {
        super(props);
        /**
         * The states of the component.
         * @type {{Media: {RelatedContents: {duration: string, channel: string, title: string, uniform_resource_locator: string, author_channel: string, thumbnail: string}[]}, System: {data_loaded: boolean}}}
         */
        this.state = {
            Media: {
                RelatedContents: [],
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
        console.info(`Route: ${window.location.pathname}\nComponent: Main.Search.Media.RelatedContents\nComponent Status: Mount`);
    }

    /**
     * The methods to be executed when the component has been updated.
     * @returns {void}
     */
    componentDidUpdate() {
        if (!this.state.System.data_loaded) {
            setTimeout(() => {
                this.setData();
                console.info(`Route: ${window.location.pathname}\nComponent: Main.Search.Media.RelatedContents\nComponent Status: Update`);
            }, 2000);
        }
    }

    /**
     * Setting the main state of the component.
     * @returns {void}
     */
    setData() {
        const local_storage_data = localStorage.getItem("related_content");
        const related_content = (typeof local_storage_data == "string") ? JSON.parse(localStorage.getItem("related_content")).data : null;
        const data_loaded = (related_content != null && window.Tracker);
        this.setState((previous) => ({
            ...previous,
            Media: {
                ...previous.Media,
                RelatedContents: (data_loaded) ? related_content : this.state.Media.RelatedContents,
            },
            System: {
                ...previous.System,
                data_loaded: data_loaded,
            },
        }));
        this.tracker = (window.Tracker) ? window.Tracker : null;
    }

    /**
     * Handling the click event on a component.
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
     * Rendering the media content that are related with the main content.
     * @param {{duration: string, channel: string, title: string, uniform_resource_locator: string, author_channel: string, thumbnail: string}} media The metadata of the media content.
     * @returns {React.JSX.Component}
     */
    renderRelatedContents(media) {
        const identifier = media.uniform_resource_locator.replaceAll("https://www.youtube.com/watch?v=", "");
        return (
            <div className="card" key={identifier}>
                <div className="thumbnail">
                    <a href={media.uniform_resource_locator} target="__blank" onClick={this.handleClick.bind(this)}>
                        <img src={media.thumbnail} loading="lazy" alt={`Thumbnail for ${media.title}`} />
                    </a>
                </div>
                <div className="metadata">
                    <div className="title">{media.title}</div>
                    <div className="author">
                        <a href={media.author_channel} target="__blank" onClick={this.handleClick.bind(this)}>{media.channel}</a>
                    </div>
                    <div className="duration">
                        <div>Duration</div>
                        <div>{media.duration}</div>
                    </div>
                </div>
            </div>
        );
    }

    /**
     * Rendering the component
     * @returns {React.JSX.Component}
     */
    render() {
        return (this.state.Media.RelatedContents.length > 0) ? (
            <div className="RelatedContents">
                {this.state.Media.RelatedContents.map((media) => this.renderRelatedContents(media))}
            </div>
        ) : (<div className="RelatedContents" style={{display: "none"}}></div>);
    }
}

export default RelatedContents;
