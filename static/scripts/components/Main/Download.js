import React, { Component } from "react";
import Downloader from "./Downloader";


/**
 * The component to be rendered for the Download page
 */
class MainDownload extends Component {
    /**
     * Constructing the application from React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
    }

    /**
     * Rendering the component for the download page.
     * @returns {React.JSX.Element}
     */
    render() {
        return (
            <main>
                <div id="loading">
                    <i class="fa-solid fa-spinner fa-spin"></i>
                </div>
                <Downloader />
            </main>
        );
    }
}

export default MainDownload;
