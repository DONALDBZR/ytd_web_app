/**
 * The component that is the homepage of the application.
 */
class Homepage extends React.Component {
    /**
     * Constructing that application from the React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
    }

    /**
     * Rendering the component which will be the body of the
     * application.
     * @returns {HTMLBodyElement}
     */
    render() {
        return [<Header />, <Main />, <Footer />];
    }
}

/**
 * The header of the page.
 */
class Header extends Homepage {
    /**
     * Constructing that application from the React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        /**
         * The states of the header.
         * @type {{Media: {search: string, YouTube: {uniform_resource_locator: string, identifier: string}}, System: {color_scheme: string, view_route: string}}}
         */
        this.state = {
            Media: {
                search: "",
                YouTube: {
                    uniform_resource_locator: "",
                    identifier: "",
                },
            },
            System: {
                color_scheme: "",
                view_route: "",
            },
        };
    }

    /**
     * Changing the color scheme according to the user's taste.
     * @param {Event} event An event which takes place in the DOM.
     * @returns {void}
     */
    setColorScheme(event) {
        const delay = 200;
        let color_scheme = (String(event.target.parentElement.parentElement.value) == "light") ? "dark" : "light";
        event.preventDefault();
        this.updateColorScheme(color_scheme, delay);
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
     * Checking the response of the server to handle it correctly.
     * @param {string} color_scheme The color scheme of the application.
     * @returns {Promise<number>}
     */
    async updateSession(color_scheme) {
        const response = await this.sendUpdateSessionRequest(color_scheme);
        return response.status;
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
        });
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
        });
    }

    /**
     * Rendering the component
     * @returns {HTMLHeaderElement}
     */
    render() {
        const application_data = {
            System: {
                color_scheme: this.state.System.color_scheme,
            },
        };
        return (
            <header>
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
            </header>
        );
    }
}

/**
 * It allows the component to be changed on the intereaction of
 * the user to change its color scheme.
 */
class ColorScheme extends Header {
    /**
     * Constructing the color scheme's component from the header.
     * @param {{data: {System: {color_scheme: string}}}} props The properties of the component.
     */
    constructor(props) {
        super(props);
        this.props = props.data;
        /**
         * The states of the component.
         * @type {{System: {color_scheme: string}}}
         */
        this.state = {
            System: {
                color_scheme: this.props.System.color_scheme,
            },
        }
    }

    /**
     * Updating the component as soon as the states are different.
     * @param {{data: {System: {color_scheme: string}}}} previous_properties The properties of the component.
     * @returns {void}
     */
    componentDidUpdate(previous_properties) {
        this.setData(previous_properties);
    }

    /**
     * Setting the data for the component.
     * @param {{data: {System: {color_scheme: string}}}} properties The properties of the component.
     * @returns {void}
     */
    setData(properties) {
        if (this.props != properties.data) {
            this.setState(() => ({
                System: {
                    color_scheme: this.props.System.color_scheme,
                },
            }));
        }
    }

    /**
     * Rendering the component which will allow the user to change
     * the color scheme.
     * @returns {HTMLElement}
     */
    render() {
        return (this.state.System.color_scheme == "dark") ? (<i class="fa-solid fa-toggle-on"></i>) : (<i class="fa-solid fa-toggle-off"></i>);
    }
}

/**
 * The component that the main of the page.
 */
class Main extends Homepage {
    /**
     * Constructing the main component which is based on the
     * Homepage.
     * @param {*} props The properties of the component.
     */
    constructor(props) {
        super(props);
        /**
         * The states of the component.
         * @type {{Trend: [{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}]}}
         */
        this.state = {
            Trend: [],
        };
    }

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setTrend()
        .then((status) => console.info(`Route: ${window.location.pathname}\nComponent: Main.Homepage\nComponent Status: Mount\nTrend API Route: /\nTrend API Status: ${status}`));
    }

    /**
     * Setting the data of the weekly trend in the state of the
     * component.
     * @returns {Promise<number>}
     */
    async setTrend() {
        const response = await this.getTrend();
        const response_data = response.data;
        this.setState((previous) => ({
            ...previous,
            Trend: response_data,
        }));
        return response.status;
    }

    /**
     * Retrieving the response's data.
     * @returns {Promise<{status: number, data: [{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}]}>}
     */
    async getTrend() {
        const server_response = await this.sendGetTrendRequest();
        return {
            status: server_response.status,
            data: await server_response.json(),
        };
    }

    /**
     * Sending a request to the server to retrieve the weekly trend
     * based on the usage of the application.
     * @returns {Promise<Response>}
     */
    async sendGetTrendRequest() {
        return fetch("/Trend/", {
            method: "GET",
        });
    }

    /**
     * Rendering the component
     * @returns {HTMLMainElement}
     */
    render() {
        /**
         * The data to be used for the Trend component.
         * @type {{Trend: [{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}]}}
         */
        const trend = {
            Trend: this.state.Trend,
        };
        return (
            <main>
                <div id="loading">
                    <i class="fa-solid fa-spinner fa-spin"></i>
                </div>
                <p>The aim of the application is that software and contents must be free and it allows anyone to get content from certain platforms to be obtained for free as it is an application developed for people by people.</p>
                <div>
                    <div>
                        <i class="fa-brands fa-youtube"></i>
                    </div>
                </div>
                <Trend data={trend} />
            </main>
        );
    }
}

/**
 * The component to be rendered for the trends.
 */
class Trend extends Main {
    /**
     * Constructing the Trend component which is based on the Main
     * component of the Homepage.
     * @param {{data: {Trend: [{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}]}}} props The properties of the component
     */
    constructor(props) {
        super(props);
        this.props = props.data;
        /**
         * The state of the component.
         * @type {{Trend: [{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}]}}
         */
        this.state = {
            Trend: this.props.Trend,
        };
    }

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setData();
    }

    /**
     * Setting the main state of the component.
     * @returns {void}
     */
    setData() {
        this.setState((previous) => ({
            ...previous,
            Trend: this.props.Trend,
        }));
    }

    /**
     * Updating the component as soon as the states are different.
     * @param {{data: {Trend: [{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}]}}} previous_properties The properties of the component
     * @returns {void}
     */
    componentDidUpdate(previous_properties) {
        if (this.props != previous_properties.data) {
            this.setData();
        }
    }

    /**
     * Retrieving the width of the trend list's carousel.
     * @param {[{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}]} trend_list The list of media content
     * @returns {string}
     */
    getTrendListWidth(trend_list) {
        const application_width = window.innerWidth;
        let trend_list_width_pixelate = "";
        return (application_width < 640) ? `${application_width * trend_list}px` : `${application_width}px`;
    }

    /**
     * Rendering the component
     * @returns {HTMLDivElement}
     */
    render() {
        return (
            <div className="Trend">
                <div style={{width: this.getTrendListWidth(this.state.Trend), animation: this.getTrendListAnimation(this.state.Trend)}} onMouseEnter={this.handleTrendListMouseEnter} onMouseLeave={this.handleTrendListMouseLeave}>
                    {this.state.Trend.map((content) => {
                        return (
                            <div class="card">
                                <div>
                                    <a
                                        href={content.uniform_resource_locator}
                                        target="__blank"
                                    >
                                        <img src={content.thumbnail} />
                                    </a>
                                </div>
                                <div>
                                    <div>{content.title}</div>
                                    <div>
                                        <a href={content.author_channel}>
                                            {content.author}
                                        </a>
                                    </div>
                                    <div>
                                        <div>Duration:</div>
                                        <div>{content.duration}</div>
                                    </div>
                                    <div>
                                        <div>Views:</div>
                                        <div>
                                            {content.views.toLocaleString(
                                                "en-US"
                                            )}
                                        </div>
                                    </div>
                                    <div>
                                        <a
                                            href={`/Download/YouTube/${content.identifier}`}
                                        >
                                            <i class="fa-solid fa-download"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        );
    }
}

// Rendering the page
ReactDOM.render(<Homepage />, document.body);