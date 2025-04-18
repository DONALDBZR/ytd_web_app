import React, { Component } from "react";
import Header from "./Header";
import Main from "./Main";
import Footer from "./Footer";


/**
 * The component for the download pages.
 */
class Download extends Component {
    /**
     * The constructor of the component.
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
    }
    

    /**
     * Rendering the component.
     * @returns {React.JSX.Element}
     */
    render() {
        return [<Header />, <Main />, <Footer />];
    }
}

export default Download;
