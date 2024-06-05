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
         * @type {{System: {view_route: string, dom_element: HTMLElement}, Media: {search: string, YouTube: {uniform_resource_locator: string, identifier: string}}}}
         */
        this.state = {
            System: {
                view_route: "",
                dom_element: "",
            },
            Media: {
                search: "",
                YouTube: {
                    uniform_resource_locator: "",
                    identifier: "",
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
        this.getData();
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
     * Getting the data needed for the component of the header.
     * @returns {void}
     */
    getData() {
        const header = document.body.querySelector("header");
        this.setState((previous) => ({
            System: {
                ...previous.System,
                view_route: window.location.pathname,
                dom_element: header,
            },
        }));
        console.log(`Route: ${window.location.pathname}`);
    }

    /**
     * Sending the request to update the session data.
     * @param {string} color_scheme The color scheme of the application.
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
     * @param {string} color_scheme The color scheme of the application.
     * @returns {Promise<number>}
     */
    async updateSession(color_scheme) {
        const response = await this.sendUpdateSessionRequest(color_scheme);
        return response.status;
    }

    /**
     * Refreshing the page while updating the color scheme.
     * @param {string} color_scheme The color scheme of the application.
     * @param {number} delay The delay in terms of milliseconds
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
     * Changing the color scheme according to the user's taste.
     * @param {Event} event An event which takes place in the DOM.
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
     * Handling the form submission which target the Search API of
     * Extractio.
     * @param {Event} event An event which takes place in the DOM.
     * @returns {void}
     */
    handleSearchSubmit(event) {
        const loading_icon = document.querySelector("main #loading");
        const delay = 200;
        const uniform_resource_locator = new URL(this.state.Media.search);
        const platform = uniform_resource_locator.host.replaceAll("www.", "").replaceAll(".com", "");
        loading_icon.style.display = "flex";
        event.preventDefault();
        this.searchMediaMetadata(platform, this.state.Media.search, delay);
    }

    /**
     * Handling the change of the data form the search form of the
     * User-Interface of Extractio.
     * @param {Event} event An event which takes place in the DOM.
     * @returns {void}
     */
    handleSearchChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;
        this.setState((previous) => ({
            ...previous,
            Media: {
                ...previous.Media,
                [name]: value,
            },
        }));
    }

    /**
     * Searching for the Media content and redirecting the user to
     * the searched content.
     * @param {string} platform The platform to be searched on.
     * @param {string} search The search data to be searched.
     * @param {number} delay The amount of delay in milliseconds.
     * @returns {void}
     */
    searchMediaMetadata(platform, search, delay) {
        this.setRoute(platform, search)
        .then((status) => console.log(`Request Method: GET\nRoute: /Media/Search?platform=${platform}&search=${search}\nStatus: ${status}\nEvent Listener: onSubmit\nView Route: /\nComponent: Header.Homepage\nDelay: ${delay} ms`))
        .then(() => {
            setTimeout(() => {
                window.location.href = this.state.System.view_route;
            }, delay);
        });
    }

    /**
     * Setting the route to be redirected.
     * @param {string} platform The platform to be searched on.
     * @param {string} search The search data to be searched.
     * @returns {Promise<number>}
     */
    async setRoute(platform, search) {
        const response = await this.setMediaYouTubeIdentifier(platform, search);
        this.setState((previous) => ({
            ...previous,
            System: {
                ...previous.System,
                view_route: `/Search/${this.state.Media.YouTube.identifier}`,
            },
        }));
        return response;
    }

    /**
     * Extracting the identifier of a specific YouTube content.
     * @param {string} platform The platform to be searched on.
     * @param {string} search The search data to be searched.
     * @returns {Promise<number>}
     */
    async setMediaYouTubeIdentifier(platform, search) {
        const response = await this.setMediaYouTubeUniformResourceLocator(platform, search);
        if (this.state.Media.YouTube.uniform_resource_locator.includes("youtube")) {
            this.setState((previous) => ({
                Media: {
                    ...previous.Media,
                    YouTube: {
                        ...previous.Media.YouTube,
                        identifier: this.state.Media.YouTube.uniform_resource_locator.replace(
                            "https://www.youtube.com/watch?v=",
                            ""
                        )
                        .replace(/\?.*/, ""),
                    },
                },
            }));
        } else {
            this.setState((previous) => ({
                Media: {
                    ...previous.Media,
                    YouTube: {
                        ...previous.Media.YouTube,
                        identifier: this.state.Media.YouTube.uniform_resource_locator.replace(
                            "https://youtu.be/",
                            ""
                        )
                        .replace(/\?.*/, ""),
                    },
                },
            }));
        }
        return response;
    }

    /**
     * Setting the uniform resource locator for a specific YouTube
     * content.
     * @param {string} platform The platform to be searched on.
     * @param {string} search The search data to be searched.
     * @returns {Promise<number>}
     */
    async setMediaYouTubeUniformResourceLocator(platform, search) {
        const response = await this.getSearchMedia(platform, search);
        this.setState((previous) => ({
            Media: {
                ...previous.Media,
                YouTube: {
                    ...previous.Media.YouTube,
                    uniform_resource_locator: response.data.uniform_resource_locator,
                },
            },
        }));
        return response.status;
    }

    /**
     * Retrieving the response of the Media API for the search
     * data.
     * @param {string} platform The platform to be searched on.
     * @param {string} search The search data to be searched.
     * @returns {Promise<{status: number, data: {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string | null, thumbnail: string, duration: string, audio_file: string | null, video_file: string | null}}>}
     */
    async getSearchMedia(platform, search) {
        const response = await this.sendGetSearchMediaRequest(platform, search);
        const response_data = await response.json();
        return {
            status: response.status,
            data: response_data.data.data,
        };
    }

    /**
     * Sending a request to the server on the Media API to retrieve
     * the data needed.
     * @param {string} platform The platform to be searched on.
     * @param {string} search The search data to be searched.
     * @returns {Promise<Response>}
     */
    async sendGetSearchMediaRequest(platform, search) {
        return fetch(`/Media/Search?platform=${platform}&search=${search}`, {
            method: "GET",
        })
    }

    /**
     * Rendering the component for the header.
     * @returns {HTMLElement}
     */
    render() {
        const application_data = {
            System: {
                view_route: this.state.System.view_route,
                dom_element: this.state.System.dom_element,
            },
        };
        if (this.state.System.view_route.includes("Search")) {
            return <Search data={application_data}  />;
        } else if (this.state.System.view_route.includes("Download")) {
            return <Download />;
        } else {
            return <Homepage data={application_data} />;
        }
    }
}

/**
 * It allows the component to be change on intearction of the
 * user to change its color scheme
 */
class ColorScheme extends Header {
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
        console.log("Main Component: Header\nComponent: ColorScheme\nStatus: Mount");
    }

    /**
     * Updating the component as soon as the states are different.
     * @param {{data: {System: {color_scheme: string, timestamp: number, dom_element: HTMLElement}}}} previous_props The properties of the component.
     * @returns {void}
     */
    componentDidUpdate(previous_props) {
        this.setData(previous_props);
        console.log("Main Component: Header\nComponent: ColorScheme\nStatus: Updated");
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
     * @returns {HTMLElement}
     */
    render() {
        if (this.state.System.color_scheme == "dark") {
            return <i class="fa-solid fa-toggle-on"></i>;
        } else {
            return <i class="fa-solid fa-toggle-off"></i>;
        }
    }
}

/**
 * The component to be rendered for the header of the homepage.
 */
class Homepage extends Header {
    /**
     * Constructing the header of the homepage from the Header Component.
     * @param {{data: {System: {view_route: string, dom_element: HTMLElement}}}} props The properties of the component
     */
    constructor(props) {
        super(props);
        this.props = props;
        /**
         * The states of the component.
         * @type {{System: {color_scheme: string, view_route: string, timestamp: number, dom_element: HTMLElement}, Media: {search: string, YouTube: {uniform_resource_locator: string, identifier: string}}}}
         */
        this.state = {
            System: {
                color_scheme: "",
                view_route: this.props.data.System.view_route,
                timestamp: "",
                dom_element: this.props.data.System.dom_element,
            },
            Media: {
                search: "",
                YouTube: {
                    uniform_resource_locator: "",
                    identifier: "",
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
        this.getSession();
        console.log("Component: Header.Homepage\nStatus: Mount");
    }

    /**
     * Updating the component as soon as the states are different.
     * @param {{data: {System: {view_route: string, dom_element: HTMLElement}}}} previous_props The properties of the component.
     * @returns {void}
     */
    componentDidUpdate(previous_props) {
        this.setData(previous_props);
        console.log("Main Component: Header\nComponent: Homepage\nStatus: Updated");
    }

    /**
     * Setting the data for the component.
     * @param {{data: {System: {view_route: string, dom_element: HTMLElement}}}} properties The properties of the component.
     * @returns {void}
     */
    setData(properties) {
        if (this.props != properties) {
            this.setState(() => ({
                System: {
                    view_route: this.props.data.System.view_route,
                    dom_element: this.props.data.System.dom_element,
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
                dom_element: this.state.System.dom_element,
            },
        };
        return (
            <>
                <nav>
                    <div class="active">
                        <a href="/">Extractio</a>
                    </div>
                    <div>
                        <form method="GET" onSubmit={this.handleSearchSubmit.bind(this)}>
                            <button>
                                <i class="fa fa-search"></i>
                            </button>
                            <input type="search" placeholder="Search..." name="search" value={this.state.Media.search} onChange={this.handleSearchChange.bind(this)} required />
                        </form>
                        <div>
                            <button name="colorSchemeChanger" value={this.state.System.color_scheme} onClick={this.setColorScheme.bind(this)}>
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
     * Constructing the header of the search page from the Header Component.
     * @param {{data: {System: {view_route: string, dom_element: HTMLElement}}}} props The properties of the component
     */
    constructor(props) {
        super(props);
        this.props = props;
        /**
         * The states of the component.
         * @type {{System: {color_scheme: string, view_route: string, timestamp: number, dom_element: HTMLElement}, Media: {search: string, YouTube: {uniform_resource_locator: string, identifier: string}}}}
         */
        this.state = {
            System: {
                color_scheme: "",
                view_route: this.props.data.System.view_route,
                timestamp: "",
                dom_element: this.props.data.System.dom_element,
            },
            Media: {
                search: "",
                YouTube: {
                    uniform_resource_locator: "",
                    identifier: "",
                },
            },
        };
    }

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
