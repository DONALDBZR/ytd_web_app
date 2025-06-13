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
    }

    /**
     * Setting the main state of the component.
     * @returns {void}
     */
    setData() {
        if (this.state.System.data_loaded) {
            console.info(`Route: ${window.location.pathname}\nComponent: RelatedContents\nStatus: Loaded`);
            return;
        }
        this.getData();
    }

    /**
     * Retrieving the data from the `localStorage` to be set as the states of the application.
     * @returns {void}
     */
    getData() {
        const {related_content, data_loaded} = this.main_utilities.getRelatedContents();
        const delay = 1000;
        if (!data_loaded) {
            setTimeout(() => this.setData(), delay);
            return;
        }
        this.setState((previous) => ({
            ...previous,
            Media: {
                ...previous.Media,
                RelatedContents: related_content,
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
     * Rendering the media content that are related with the main content.
     * @param {{duration: string, channel: string, title: string, uniform_resource_locator: string, author_channel: string, thumbnail: string}} media The metadata of the media content.
     * @returns {React.JSX.Component}
     */
    renderRelatedContents(media) {
        const identifier = media.uniform_resource_locator.replaceAll("https://www.youtube.com/watch?v=", "");
        return (
            <div className="card" key={identifier}>
                <div className="thumbnail">
                    <a href={media.uniform_resource_locator} target="__blank" onClick={(event) => this.main_utilities.handleClick(event, this.tracker)}>
                        <img src={media.thumbnail} loading="lazy" alt={`Thumbnail for ${media.title}`} />
                    </a>
                </div>
                <div className="metadata">
                    <div className="title">{media.title}</div>
                    <div className="author">
                        <a href={media.author_channel} target="__blank" onClick={(event) => this.main_utilities.handleClick(event, this.tracker)}>{media.channel}</a>
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
