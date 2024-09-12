import React, { Component } from "react";
import YouTube from "./YouTube";
import RelatedContents from "./RelatedContents";


/**
 * The component that the main of the page.
 */
class Main extends Component {
    /**
     * Rendering the component for the desktop users.
     * @returns {HTMLElement}
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
     * Rendering the component for the tablet and mobile users.
     * @returns {HTMLElement}
     */
    renderTabletMobile() {
        return (
            <main>
                <div id="loading">
                    <i className="fa-solid fa-spinner fa-spin"></i>
                </div>
                <div className="Media">
                    <YouTube />
                </div>
            </main>
        );
    }

    /**
     * Rendering the component
     * @returns {HTMLElement}
     */
    render() {
        const root = document.querySelector(":root");
        return (root.clientWidth >= 1024) ? this.renderDesktop() : this.renderTabletMobile();
    }
}

export default Main;