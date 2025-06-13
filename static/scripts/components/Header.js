import React, { Component } from "react";
import HeaderHomepage from "./Header/Homepage";
import HeaderSearch from "./Header/Search";


/**
 * The component for the header.
 */
class Header extends Component {
    /**
     * The consturctor of the components.
     * @param {*} props 
     */
    constructor(props) {
        super(props);
    }
    
    /**
     * Rendering the component for the header.
     * @returns {React.JSX.Element}
     */
    render() {
        return (window.location.pathname == "/") ? <HeaderHomepage /> : <HeaderSearch />;
    }
}

export default Header;
