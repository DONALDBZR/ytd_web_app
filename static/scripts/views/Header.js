/**
 * The component that is the header for all of the pages
 */
class Header extends React.Component {
    /**
     * Constructing the application from React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        this.state = {
            System: {
                color_scheme: "",
                view_route: "",
            },
        };
    }
    /**
     * Running the methods needed as soon as the component has been successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.getSession();
    }
    /**
     * Retrieving the session of the application
     * @returns {void}
     */
    getSession() {
        fetch("/Session", {
            method: "GET",
        })
            .then((response) => response.json())
            .then((data) =>
                this.setState((previous) => ({
                    System: {
                        ...previous.System,
                        color_scheme: data.Client.color_scheme,
                    },
                }))
            )
            .then(() => this.verifyColorScheme())
            .then(() => this.adjustPage());
    }
    /**
     * Verifying that the color scheme does not have a value
     * @returns {void}
     */
    verifyColorScheme() {
        if (this.state.System.color_scheme == "") {
            this.setState({
                System: {
                    color_scheme: "light",
                },
            });
        }
    }
    /**
     * Adjusting the color scheme of the application
     * @returns {string}
     */
    adjustPage() {
        const root = document.querySelector(":root");
        if (
            this.state.System.color_scheme == "light" ||
            this.state.System.color_scheme == ""
        ) {
            const color1 =
                "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))";
            const color2 =
                "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))";
            const color3 =
                "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (69 / 255)), calc(var(--percentage) * (65 / 255)))";
            root.style.setProperty("--color1", color1);
            root.style.setProperty("--color2", color2);
            root.style.setProperty("--color3", color3);
        } else {
            const color1 =
                "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))";
            const color2 =
                "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))";
            const color3 =
                "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (69 / 255)), calc(var(--percentage) * (65 / 255)))";
            root.style.setProperty("--color1", color1);
            root.style.setProperty("--color2", color2);
            root.style.setProperty("--color3", color3);
        }
    }
    /**
     * Rendering the component
     * @returns {HTMLHeaderElement}
     */
    render() {
        // Verifying the uniform resource locator of the application
        return (
            <header>
                <nav>
                    <div class="active">
                        <a href="/">Extractio</a>
                    </div>
                    <div>
                        <div>
                            <a href="/Search">
                                <i class="fa fa-search"></i>
                            </a>
                        </div>
                        <div>
                            <button
                                name="colorSchemeChanger"
                                value={this.state.System.color_scheme}
                                onClick={this.setColorScheme}
                            >
                                <ColorScheme />
                            </button>
                        </div>
                    </div>
                </nav>
            </header>
        );
    }
}
// Rendering the page
ReactDOM.render(<Application />, document.querySelector("header"));