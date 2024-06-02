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
        /**
         * States of the application
         * @type {{System: {view_route: string}}}
         */
        this.state = {
            System: {
                view_route: "",
            },
        };
    }

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.getRoute();
    }

    /**
     * Sending the request to the server to retrieve the session
     * data.
     * @returns {Promise<Response>}
     */
    async sendGetSessionRequest() {
        return fetch("/Session/", {
            method: "GET",
        });
    }

    /**
     * Extracting the session data from the response.
     * @returns {Promise<{status: number, data: {Client: {timestamp: number, color_scheme: string}}}>}
     */
    async getSessionResponse() {
        const response = await this.sendGetSessionRequest();
        return {
            status: response.status,
            data: await response.json(),
        };
    }

    /**
     * Verifying that the color scheme does not have a value
     * @returns {Promise<number>}
     */
    async verifyColorScheme() {
        const response = await this.getSessionResponse();
        this.setState((previous) => ({
            System: {
                ...previous.System,
                color_scheme: response.data.Client.color_scheme,
                timestamp: response.data.Client.timestamp,
            },
        }));
        if (this.state.System.color_scheme == "") {
            this.setState((previous) => ({
                System: {
                    ...previous.System,
                    color_scheme: "light",
                },
            }));
        }
        return response.status;
    }

    /**
     * Adjusting the color scheme of the application
     * @returns {Promise<number>}
     */
    async adjustPage() {
        const root = document.querySelector(":root");
        const status = await this.verifyColorScheme();
        let color1;
        let color2;
        let color3;
        let color5;
        if (this.state.System.color_scheme == "light" || this.state.System.color_scheme == "") {
            color1 = "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))";
            color2 = "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))";
            color3 = "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (69 / 255)), calc(var(--percentage) * (65 / 255)))";
            color5 = "rgba(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)), calc(var(--percentage) / 2))";
        } else {
            color1 = "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))";
            color2 = "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))";
            color3 = "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (69 / 255)), calc(var(--percentage) * (65 / 255)))";
            color5 = "rgba(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)), calc(var(--percentage) / 2))";
        }
        root.style.setProperty("--color1", color1);
        root.style.setProperty("--color2", color2);
        root.style.setProperty("--color3", color3);
        root.style.setProperty("--color5", color5);
        return status;
    }

    /**
     * Retrieving the session of the application
     * @returns {void}
     */
    getSession() {
        this.adjustPage()
        .then((status) => console.log(`Request Method: GET\nRoute: /Session\nStatus: ${status}`));
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
        console.log(`Route: ${window.location.pathname}`);
    }

    /**
     * Sending the request to update the session data.
     * @param {string} color_scheme
     * @returns {Promise<Response>}
     */
    async sendUpdateSessionRequest(color_scheme) {
        return fetch("/Session/", {
            method: "PUT",
            body: JSON.stringify({
                Client: {
                    color_scheme: color_scheme,
                },
            }),
            headers: {
                "Content-Type": "application/json",
            },
        })
    }

    /**
     * Checking the response of the server to handle it correctly.
     * @param {string} color_scheme
     * @returns {Promise<number>}
     */
    async updateSession(color_scheme) {
        const response = await this.sendUpdateSessionRequest(color_scheme);
        return response.status;
    }

    /**
     * Refreshing the page while updating the color scheme
     * @param {string} color_scheme
     * @param {number} delay
     * @returns {void}
     */
    updateColorScheme(color_scheme, delay) {
        this.updateSession(color_scheme)
        .then((status) => console.log(`Request Method: PUT\nRoute: /Session\nStatus: ${status}`));
        setTimeout(() => {
            window.location.href = window.location.href;
        }, delay);
    }

    /**
     * Changing the color scheme according to the user's taste
     * @param {Event} event 
     * @returns {void}
     */
    setColorScheme(event) {
        const delay = 200;
        let color_scheme = String(event.target.parentElement.parentElement.value);
        event.preventDefault();
        if (color_scheme == "light") {
            color_scheme = "dark";
        } else {
            color_scheme = "light";
        }
        this.updateColorScheme(color_scheme, delay);
    }

    /**
     * Rendering the component
     * @returns {HTMLHeaderElement}
     */
    render() {
        const application_data = {
            System: {
                view_route: this.state.System.view_route,
            },
        };
        if (this.state.System.view_route.includes("Search")) {
            return <Search />;
        } else if (this.state.System.view_route.includes("Download")) {
            return <Download />;
        } else {
            return <Homepage data={application_data} />;
        }
    }
}

/**
 * It allows the component to be change on intearction of the user to change its color scheme
 */
class ColorScheme extends Header {
    /**
     * Constructing the color scheme's component from the header.
     * @param {{data: {System: {color_scheme: string, timestamp: number}}}} props The properties of the component
     */
    constructor(props) {
        super(props);
        this.props = props;
        /**
         * The states of the component.
         * @type {{System: {color_scheme: string, timestamp: number}}}
         */
        this.state = {
            System: {
                color_scheme: this.props.data.System.color_scheme,
                timestamp: this.props.data.System.timestamp,
            },
        };
    }

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
     * Constructing the header of the homepage from React's
     * Component
     * @param {{data: {System: {view_route: string}}}} props The properties of the component
     */
    constructor(props) {
        super(props);
        this.props = props;
        /**
         * The states of the component.
         * @type {{System: {color_scheme: string, view_route: string, timestamp: number}}}
         */
        this.state = {
            System: {
                color_scheme: "",
                view_route: this.props.data.System.view_route,
                timestamp: "",
            },
        };
    }

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.getSession();
        console.log("Main Component: Header\nComponent: Homepage\nStatus: Mount");
    }

    /**
     * Updating the component as soon as the states are different.
     * @param {{data: {System: {view_route: string}}}} previous_props The properties of the component.
     * @returns {void}
     */
    componentDidUpdate(previous_props) {
        this.setData(previous_props);
        console.log("Main Component: Header\nComponent: Homepage\nStatus: Updated");
    }

    /**
     * Setting the data for the component.
     * @param {{data: {System: {view_route: string}}}} properties The properties of the component.
     * @returns {void}
     */
    setData(properties) {
        if (this.props != properties) {
            this.setState(() => ({
                System: {
                    color_scheme: this.props.data.System.color_scheme,
                    view_route: this.props.data.System.view_route,
                },
            }));
        }
    }

    /**
     * Rendering the component
     * @returns {HTMLHeaderElement}
     */
    render() {
        const application_data = {
            System: {
                color_scheme: this.state.System.color_scheme,
                timestamp: this.state.System.timestamp,
            },
        };
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
                                onClick={this.setColorScheme.bind(this)}
                            >
                                <ColorScheme data={application_data} />
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

    componentDidMount() {
        this.getRoute();
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
/**
 * The component to be rendered for the Download page
 */
class Download extends Header {
    /**
     * Constructing the application from React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
    }

    componentDidMount() {
        this.getRoute();
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
// Rendering the page
ReactDOM.render(<Header />, document.querySelector("header"));
