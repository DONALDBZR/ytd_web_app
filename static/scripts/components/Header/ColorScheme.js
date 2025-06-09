import React, { Component } from "react";


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
    }

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setData();
        console.log("Component: Header.HeaderHomepage.ColorScheme\nStatus: Mount");
    }

    /**
     * Updating the component as soon as there is an update in the
     * states.
     * @returns {void}
     */
    componentDidUpdate() {
        if (!this.state.System.data_loaded) {
            setTimeout(() => {
                this.setData();
                console.log("Component: Homepage.Header.HeaderHomepage\nStatus: Updated");
            }, 1000);
        }
    }

    /**
     * Setting the data for the component.
     * @returns {void}
     */
    setData() {
        const session = JSON.parse(localStorage.getItem("session"));
        const data_loaded = (session != null);
        this.setState((previous) => ({
            ...previous,
            Session: (data_loaded) ? session : this.state.Session,
            System: {
                ...previous.System,
                data_loaded: data_loaded,
            },
        }));
        this.setSvg();
    }

    /**
     * Setting the data for the SVG SVG Element.
     * @param {SVGSVGElement} svg
     * @returns {void}
     */
    setSvgSvgElement(svg) {
        const lookup = {
            "dark": "svg-inline--fa fa-toggle-on",
            "light": "svg-inline--fa fa-toggle-off"
        };
        svg.setAttribute("class", lookup[this.state.Session.Client.color_scheme]);
        svg.setAttribute("data-icon", (this.state.Session.Client.color_scheme == "dark") ? "toggle-on" : "toggle-off");
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
