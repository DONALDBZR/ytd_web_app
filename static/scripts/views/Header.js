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
        this.getRoute();
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
            this.setState((previous) => ({
                System: {
                    ...previous.System,
                    color_scheme: "light",
                },
            }));
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
     * Setting the view route of the application.
     * @returns {void}
     */
    getRoute() {
        this.setState((previous) => ({
            System: {
                ...previous.System,
                view_route: window.location.pathname,
            },
        }));
    }
    /**
     * Changing the color scheme according to the user's taste
     * @returns {void}
     */
    setColorScheme() {
        const delay = 200;
        event.preventDefault();
        let color_scheme = document.querySelector(
            "button[name='colorSchemeChanger']"
        ).value;
        if (color_scheme == "light") {
            color_scheme = "dark";
        } else {
            color_scheme = "light";
        }
        fetch("/Session/Post", {
            method: "POST",
            body: JSON.stringify({
                Client: {
                    color_scheme: color_scheme,
                },
            }),
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((response) => response.json())
            .then(() => {
                setTimeout(() => {
                    window.location.href = window.location.href;
                }, delay);
            });
    }
    /**
     * Rendering the component
     * @returns {HTMLHeaderElement}
     */
    render() {
        if (this.state.System.view_route.includes("Search")) {
            return <Search />;
        } else {
            return <Homepage />;
        }
    }
}
/**
 * It allows the component to be change on intearction of the user to change its color scheme
 */
class ColorScheme extends Header {
    /**
     * Constructing the color scheme's component and also inheriting the properties and states from the header
     * @param {*} props
     */
    constructor(props) {
        super(props);
    }
    /**
     * Running the methods needed as soon as the component has been successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.getSession();
    }
    /**
     * Rendering the component which allows the user to change the color scheme
     * @returns {HTMLButtonElement}
     */
    render() {
        if (this.state.System.color_scheme == "dark") {
            return <i class="fa-solid fa-toggle-on"></i>;
        } else if (this.state.System.color_scheme == "light") {
            return <i class="fa-solid fa-toggle-off"></i>;
        }
    }
}
/**
 * The component to be rendered for the homepage
 */
class Homepage extends Header {
    /**
     * Constructing the application from React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
    }
    /**
     * Running the methods needed as soon as the component has been successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.getSession();
    }
    /**
     * Rendering the component
     * @returns {HTMLHeaderElement}
     */
    render() {
        return (
            <>
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
            </>
        );
    }
}
/**
 * The component to be rendered for the search page
 */
class Search extends Header {
    /**
     * Constructing the application from React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
    }
    /**
     * Running the methods needed as soon as the component has been successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.getSession();
    }
    /**
     * Rendering the component
     * @returns {HTMLHeaderElement}
     */
    render() {
        return (
            <>
                <nav>
                    <div>
                        <a href="/">Extractio</a>
                    </div>
                    <div>
                        <div class="active">
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
            </>
        );
    }
}
// Rendering the page
ReactDOM.render(<Header />, document.querySelector("header"));
