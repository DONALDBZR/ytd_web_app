import React, { Component } from "react";
import YouTube from "./YouTube";
import RelatedContents from "./RelatedContents";


/**
 * The component that the main of the page.
 */
class Main extends Component {
    /**
     * Rendering the component for the desktop users.
     * @returns {HTMLMainElement}
     */
    renderDesktop() {
        return (
            <main>
                <div id="loading">
                    <i className="fa-solid fa-spinner fa-spin"></i>
                </div>
                <div className="Media">
                    <YouTube />
                    <RelatedContents />
                </div>
            </main>
        );
    }

    /**
     * Rendering the component
     * @returns {HTMLMainElement}
     */
    render() {
        return (
            <main>
                <div id="loading">
                    <i className="fa-solid fa-spinner fa-spin"></i>
                </div>
                <div className="Media">
                    <YouTube />
                    <RelatedContents />
                </div>
            </main>
        );
    }
}

export default Main;