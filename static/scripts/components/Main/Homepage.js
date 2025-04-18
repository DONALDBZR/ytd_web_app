import React, { Component } from "react";
import Trend from "./Trend";


/**
 * The component to be rendered for the homepage
 */
class MainHomepage extends Component {
    /**
     * Constructing the Homepage component which is based on the
     * Main component.
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
    }

    /**
     * Rendering the component
     * @returns {React.JSX.Element}
     */
    render() {
        return (
            <main>
                <div id="loading">
                    <i class="fa-solid fa-spinner fa-spin"></i>
                </div>
                <p>
                    The aim of the application is that software and contents
                    must be free and it allows anyone to get content from
                    certain platforms to be obtained for free as it is an
                    application developed for people by people.
                </p>
                <div>
                    <div>
                        <i class="fa-brands fa-youtube"></i>
                    </div>
                </div>
                <Trend />
            </main>
        );
    }
}

export default MainHomepage;
