import React, { Component } from "react";
import Header_Utilities from "../utilities/Header";


/**
 * It allows the component to be change on interaction of the user to change its color scheme.
 */
class ColorScheme extends Component {
    /**
     * Constructing the color scheme's component from the header.
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        /**
         * The states of the component.
         * @type {{Session: {Client: {timestamp: number, color_scheme: string}}, System: {data_loaded: boolean}}}
         */
        this.state = {
            Session: {
                Client: {
                    timestamp: "",
                    color_scheme: "",
                },
            },
            System: {
                data_loaded: false,
            },
        };
        /**
         * The utility class of the Header component.
         * @type {Header_Utilities}
         */
        this.Header_Utilities = new Header_Utilities();
    }

    /**
     * Running the methods needed as soon as the component has been successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setData();
    }

    /**
     * Setting the data for the component.
     * @returns {void}
     */
    setData() {
        if (this.state.System.data_loaded) {
            console.info(`Route: ${window.location.pathname}\nComponent: ColorScheme\nStatus: Loaded`);
            return;
        }
        this.getData();
    }

    /**
     * Retrieving the data from the `localStorage` to be set as the states of the application.
     * @returns {void}
     */
    getData() {
        const {session, data_loaded, view_route} = this.Header_Utilities.getSession();
        const delay = 1000;
        if (!data_loaded) {
            setTimeout(() => this.setData(), delay);
            return
        }
        this.setState((previous) => ({
            ...previous,
            Session: session,
            System: {
                ...previous.System,
                data_loaded: data_loaded,
            },
        }));
        this.setSvg();
    }

    /**
     * Setting the data for the SVG SVG Element.
     * @param {SVGSVGElement} svg - The Element.
     * @returns {void}
     */
    setSvgSvgElement(svg) {
        const lookup = {
            "dark": "svg-inline--fa fa-toggle-on",
            "light": "svg-inline--fa fa-toggle-off"
        };
        svg.setAttribute("class", lookup[this.state.Session.Client.color_scheme]);
        svg.setAttribute("data-icon", (this.state.Session.Client.color_scheme == "dark") ? "toggle-on" : "toggle-off");
        console.info("Component: ColorScheme\nStatus: Updated");
    }

    /**
     * Setting the SVG Element.
     * @returns {void}
     */
    setSvg() {
        const dom_element = document.querySelector("header nav div div button").children[0];
        if (typeof dom_element == null) {
            return;
        }
        if (!String(dom_element).includes("HTMLElement")) {
            this.setSvgSvgElement(dom_element);
        }
        (this.state.Session.Client.color_scheme == "dark") ? dom_element.setAttribute("class", "fa-solid fa-toggle-on") : dom_element.setAttribute("class", "fa-solid fa-toggle-off");
        console.info("Component: ColorScheme\nStatus: Updated");
    }

    /**
     * Rendering the component which allows the user to change the
     * color scheme.
     * @returns {React.JSX.Element}
     */
    render() {
        return (this.state.Session.Client.color_scheme == "dark") ? <i class="fa-solid fa-toggle-on"></i> : <i class="fa-solid fa-toggle-off"></i>;
    }
}

export default ColorScheme;
