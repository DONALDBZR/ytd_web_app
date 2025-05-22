import React, { Component } from "react";
import YouTubeDownloader from "./YouTubeDownloader";


/**
 * The component to be rendered for the Download portal
 */
class Downloader extends Component {
    /**
     * Constructing the application from React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
    }

    /**
     * Rendering the component for the download portal.
     * @returns {React.JSX.Element | undefined}
     */
    render() {
        if (window.location.pathname.includes("YouTube")) {
            return <YouTubeDownloader />;
        }
    }
}

export default Downloader;
