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
        this.setData();
        console.log("Component: Header.HeaderHomepage.ColorScheme\nStatus: Mount");
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
        svg.setAttribute("class", (this.state.Session.Client.color_scheme == "dark") ? "svg-inline--fa fa-toggle-on" : "svg-inline--fa fa-toggle-off");
        svg.setAttribute("data-icon", (this.state.Session.Client.color_scheme == "dark") ? "toggle-on" : "toggle-off");
    }

    /**
     * Setting the SVG Element.
     * @returns {void}
     */
    setSvg() {
        const dom_element = document.querySelector("header nav div div button").children[0];
        if (typeof dom_element != null) {
            (String(dom_element).includes("HTMLElement")) ? ((this.state.Session.Client.color_scheme == "dark") ? dom_element.setAttribute("class", "fa-solid fa-toggle-on") : dom_element.setAttribute("class", "fa-solid fa-toggle-off")) : this.setSvgSvgElement(dom_element);
        }
    }

    /**
     * Rendering the component which allows the user to change the
     * color scheme.
     * @returns {React.Component}
     */
    render() {
        return (this.state.Session.Client.color_scheme == "dark") ? <i class="fa-solid fa-toggle-on"></i> : <i class="fa-solid fa-toggle-off"></i>;
    }
}