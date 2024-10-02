/**
 * It allows the component to be change on interaction of the
 * user to change its color scheme
 */
class ColorScheme extends React.Component {
    /**
     * Constructing the color scheme's component from the header.
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        /**
         * The states of the component.
         * @type {{Session: {Client: {timestamp: number, color_scheme: string}}}}
         */
        this.state = {
            Session: {
                Client: {
                    timestamp: "",
                    color_scheme: "",
                },
            },
        };
    }

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        console.log("Component: Header.ColorScheme\nStatus: Mount");
    }

    /**
     * Setting the data for the component.
     * @returns {void}
     */
    setData() {
        this.setState((previous) => ({
            ...previous,
            Session: JSON.parse(localStorage.getItem("session")),
        }));
        this.setSvg();
    }

    /**
     * Setting the data for the HTML Element.
     * @param {HTMLElement} i The HTML Element.
     * @returns {void}
     */
    setHtmlElementData(i) {
        if (this.state.System.color_scheme == "dark") {
            i.setAttribute("class", "fa-solid fa-toggle-on");
        } else {
            i.setAttribute("class", "fa-solid fa-toggle-off");
        }
    }

    /**
     * Setting the data for the SVG SVG Element.
     * @param {SVGSVGElement} svg
     * @returns {void}
     */
    setSvgSvgElement(svg) {
        if (this.state.System.color_scheme == "dark") {
            svg.setAttribute("class", "svg-inline--fa fa-toggle-on");
            svg.setAttribute("data-icon", "toggle-on");
        } else {
            svg.setAttribute("class", "svg-inline--fa fa-toggle-off");
            svg.setAttribute("data-icon", "toggle-off");
        }
    }

    /**
     * Setting the data for the DOM Element.
     * @param {SVGSVGElement | HTMLElement} element The HTML Element.
     * @returns {void}
     */
    setDomElementData(element) {
        if (String(element).includes("HTMLElement")) {
            this.setHtmlElementData(element);
        } else {
            this.setSvgSvgElement(element);
        }
    }

    /**
     * Setting the SVG Element.
     * @returns {void}
     */
    setSvg() {
        const dom_element = document.querySelector("header nav div div button").children[0];
        if (typeof dom_element != null) {
            this.setDomElementData(dom_element);
        }
    }

    /**
     * Rendering the component which allows the user to change the
     * color scheme.
     * @returns {React.Component}
     */
    render() {
        if (this.state.System.color_scheme == "dark") {
            return <i class="fa-solid fa-toggle-on"></i>;
        } else {
            return <i class="fa-solid fa-toggle-off"></i>;
        }
    }
}