import React, { Component } from "react";
import Media from "./Media";


/**
 * The component to be rendered for the search page
 */
class MainSearch extends Component {
    /**
     * Constructing the Search component of the application.
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
                <Media />
            </main>
        );
    }
}

export default MainSearch;
