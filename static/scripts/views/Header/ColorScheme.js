/**
 * It allows the component to be change on interaction of the
 * user to change its color scheme
 */
class ColorScheme extends React.Component {
    /**
     * Constructing the color scheme's component from the header.
     * @param {{data: {System: {color_scheme: string, timestamp: number, dom_element: HTMLElement}}}} props The properties of the component
     */
    constructor(props) {
        super(props);
        this.props = props;
        /**
         * The states of the component.
         * @type {{System: {color_scheme: string, timestamp: number, dom_element: HTMLElement}}}
         */
        this.state = {
            System: {
                color_scheme: this.props.data.System.color_scheme,
                timestamp: this.props.data.System.timestamp,
                dom_element: this.props.data.System.dom_element,
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
     * Updating the component as soon as the states are different.
     * @param {{data: {System: {color_scheme: string, timestamp: number, dom_element: HTMLElement}}}} previous_props The properties of the component.
     * @returns {void}
     */
    componentDidUpdate(previous_props) {
        this.setData(previous_props);
        console.log("Component: Header.ColorScheme\nStatus: Updated");
    }

    /**
     * Setting the data for the component.
     * @param {{data: {System: {color_scheme: string, timestamp: number, dom_element: HTMLElement}}}} properties The properties of the component.
     * @returns {void}
     */
    setData(properties) {
        const dom_element = document.querySelector("header nav div:nth-child(2) div:nth-child(2) button").children[0];
        if (this.props != properties) {
            this.setState(() => ({
                System: {
                    color_scheme: this.props.data.System.color_scheme,
                    timestamp: this.props.data.System.timestamp,
                    dom_element: dom_element,
                },
            }));
        }
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