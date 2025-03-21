/**
 * The component to be rendered for the header of the search
 * page.
 */
class HeaderSearch extends React.Component {
    /**
     * Constructing the header of the search page.
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        /**
         * The states of the component.
         * @type {{Session: {Client: {timestamp: number, color_scheme: string}}, Media: {search: string, YouTube: {uniform_resource_locator: string, identifier: string}}, System: {view_route: string, data_loaded: boolean}}}
         */
        this.state = {
            Session: {
                Client: {
                    timestamp: "",
                    color_scheme: "",
                },
            },
            Media: {
                search: "",
                YouTube: {
                    uniform_resource_locator: "",
                    identifier: "",
                },
            },
            System: {
                data_loaded: false,
            },
        };
        /**
         * The tracker class which will track the user's activity on
         * the application.
         * @type {Tracker}
         */
        this.tracker = window.Tracker;
    }

    /**
     * * Sanitizing a string by escaping special HTML characters.
     * * This function replaces the following characters with their HTML entity equivalents:
     * - `&` → `&amp;`
     * - `<` → `&lt;`
     * - `>` → `&gt;`
     * - `"` → `&quot;`
     * - `'` → `&#039;`
     * - `/` → `&#x2F;`
     * @param {string} data The input string to be sanitized.
     * @returns {string}
     */
    sanitize(data) {
        return data.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#039;").replaceAll("/", "&#x2F;");
    }

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setData();
        console.info("Component: Search.Header.HeaderSearch\nStatus: Mount");
    }

    /**
     * Running the methods needed whenever the component is updated.
     * @returns {void}
     */
    componentDidUpdate() {
        if (!this.state.System.data_loaded) {
            setTimeout(() => {
                this.setData();
                console.info("Component: Search.Header.HeaderSearch\nStatus: Update");
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
        const root = document.querySelector(":root");
        const color_1 = (session != null) ? ((session.Client.color_scheme == "light") ? "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))" : "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))") : "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))";
        const color_2 = (session != null) ? ((session.Client.color_scheme == "dark") ? "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))" : "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))") : "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))";
        const color_3 = "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (69 / 255)), calc(var(--percentage) * (65 / 255)))";
        const color_5 = (session != null) ? ((session.Client.color_scheme == "light") ? "rgba(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)), calc(var(--percentage) / 2))" : "rgba(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)), calc(var(--percentage) / 2))") : "rgba(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)), calc(var(--percentage) / 2))";
        this.setState((previous) => ({
            ...previous,
            Session: (data_loaded) ? session : this.state.Session,
            System: {
                ...previous.System,
                data_loaded: data_loaded,
            },
        }));
        root.style.setProperty("--color1", color_1);
        root.style.setProperty("--color2", color_2);
        root.style.setProperty("--color3", color_3);
        root.style.setProperty("--color5", color_5);
    }

    /**
     * Handling the form submission which target the Search API of Extractio.
     * @param {SubmitEvent} event An event which takes place in the DOM.
     * @returns {void}
     */
    handleSubmit(event) {
        const loading_icon = document.querySelector("main #loading");
        const delay = 200;
        const uniform_resource_locator = new URL(this.state.Media.search);
        const platform = uniform_resource_locator.host.replaceAll("www.", "").replaceAll(".com", "");
        loading_icon.style.display = "flex";
        loading_icon.style.height = "-webkit-fill-available";
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
        this.tracker.sendEvent("search_submitted", {
            search_term: search,
        })
        .then(() => {
            return this.setRoute(platform, search);
        })
        .then((status) => {
            console.log(`Request Method: GET\nRoute: /Media/Search?platform=${platform}&search=${search}\nStatus: ${status}\nEvent Listener: onSubmit\nView Route: ${window.location.href}\nComponent: Search.Header.HeaderSearch\nDelay: ${delay} ms`);
            setTimeout(() => {
                window.location.href = this.state.System.view_route;
            }, delay);
        })
        .catch((error) => {
            console.error("An error occurred while sending the event or setting the route!\nError: ", error);
            setTimeout(() => {
                window.location.href = window.location.href;
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
        try {
            const status = await this.setMediaYouTubeIdentifier(platform, search);
            this.setState((previous) => ({
                ...previous,
                System: {
                    ...previous.System,
                    view_route: (status == 200) ? `/Search/${this.state.Media.YouTube.identifier}` : "/",
                },
            }));
            return status;
        } catch (error) {
            console.error("An error occurred while setting the route!\nError: ", error);
            throw new Error(error);
        }
    }

    /**
     * Setting the identifier of a specific YouTube content.
     * @param {string} platform The platform to be searched on.
     * @param {string} search The search data to be searched.
     * @returns {Promise<number>}
     */
    async setMediaYouTubeIdentifier(platform, search) {
        try {
            const status = await this.setMediaYouTubeUniformResourceLocator(platform, search);
            const identifier = this.extractYouTubeIdentifier(this.state.Media.YouTube.uniform_resource_locator);
            this.setState((previous) => ({
                ...previous,
                Media: {
                    ...previous.Media,
                    YouTube: {
                        ...previous.Media.YouTube,
                        identifier: identifier,
                    },
                },
            }));
            return status;
        } catch (error) {
            console.error("An error occurred while setting the YouTube identifier.\nError: ", error);
            throw new Error(error);
        }
    }

    /**
     * Extracting the YouTube Identifier from the uniform resource locator.
     * @param {string} uniform_resource_locator The uniform resource locator
     * @returns {string}
     */
    extractYouTubeIdentifier(uniform_resource_locator) {
        try {
            const parsed_uniform_resource_locator = new URL(uniform_resource_locator);
            this.__checkNotAllowedDomains(parsed_uniform_resource_locator);
            return String(this.sanitize(this.getYouTubeIdentifier(parsed_uniform_resource_locator)));
        } catch (error) {
            console.error("There is an error while extracting the YouTube identifier.\nError: ", error);
            throw new Error(error);
        }
    }

    /**
     * Retrieving the identifier of YouTube from its uniform resource locator.
     * @param {URL} uniform_resource_locator The uniform resource locator
     * @returns {string}
     */
    getYouTubeIdentifier(uniform_resource_locator) {
        if ((uniform_resource_locator.hostname === "youtube.com" && uniform_resource_locator.pathname === "/watch") || (uniform_resource_locator.hostname === "www.youtube.com" && uniform_resource_locator.pathname === "/watch")) {
            return this.sanitize(uniform_resource_locator.searchParams.get("v"));
        }
        if (uniform_resource_locator.hostname === "youtu.be") {
            return this.sanitize(uniform_resource_locator.pathname.slice(1));
        }
        throw new Error(`Error while retrieving the YouTube identifier!\nHost Name: ${uniform_resource_locator.hostname}`);
    }

    /**
     * Checking domains that are not allowed.
     * @param {URL} uniform_resource_locator The parsed uniform resource locator
     * @returns {void}
     */
    __checkNotAllowedDomains(uniform_resource_locator) {
        const allowed_domains = ["www.youtube.com", "youtu.be"];
        if (allowed_domains.includes(uniform_resource_locator.hostname)) {
            return;
        }
        throw new Error(`The domain is not allowed!\nHost Name: ${uniform_resource_locator.hostname}`);
    }

    /**
     * Setting the uniform resource locator for a specific YouTube content.
     * @param {string} platform The platform to be searched on.
     * @param {string} search The search data to be searched.
     * @returns {Promise<number>}
     */
    async setMediaYouTubeUniformResourceLocator(platform, search) {
        const response = await this.getSearchMedia(platform, search);
        try {
            const uniform_resource_locator = this.sanitizeUniformResourceLocator(decodeURIComponent(response.data.uniform_resource_locator));
            this.setState((previous) => ({
                ...previous,
                Media: {
                    ...previous.Media,
                    YouTube: {
                        ...previous.Media.YouTube,
                        uniform_resource_locator: uniform_resource_locator,
                    },
                },
            }));
            return response.status;
        } catch (error) {
            console.error("Failed to set the uniform resource locator.\nError: ", error);
            throw new Error(error);
        }
    }

    /**
     * Sanitizing the given uniform resource locator by ensuring that it belongs to an allowed domain.
     * @param {string} uniform_resource_locator The uniform resource locator
     * @returns {string}
     */
    sanitizeUniformResourceLocator(uniform_resource_locator) {
        const youtube_regular_expression = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/(watch\?v=|embed\/|shorts\/|)([a-zA-Z0-9_-]{11})(&.*)?$/;
        const parsed_uniform_resource_locator = new URL(uniform_resource_locator);
        try {
            this.__checkNotAllowedDomains(parsed_uniform_resource_locator);
            this.__checkInvalidUniformResourceLocator(youtube_regular_expression, parsed_uniform_resource_locator);
            return parsed_uniform_resource_locator.href;
        } catch (error) {
            console.error(`Invalid uniform resource locator!\nUniform Resource Locator: ${parsed_uniform_resource_locator}\nError: `, error);
            throw new Error(error);
        }
    }

    /**
     * Checking the uniform resource locator against the regular expression.
     * @param {RegExp} regular_expression The regular expression
     * @param {string} uniform_resource_locator The uniform resource locator
     * @return {void}
     */
    __checkInvalidUniformResourceLocator(regular_expression, uniform_resource_locator) {
        if (regular_expression.test(uniform_resource_locator.href)) {
            return;
        }
        throw new Error(`Invalid YouTube uniform resource locator format!\nUniform Resource Locator: ${uniform_resource_locator.href}`);
    }

    /**
     * Retrieving the response of the Media API for the search
     * data.
     * @param {string} platform The platform to be searched on.
     * @param {string} search The search data to be searched.
     * @returns {Promise<{status: number, data: {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string | null, thumbnail: string, duration: string, audio_file: string | null, video_file: string | null}}>}
     */
    async getSearchMedia(platform, search) {
        const response = await fetch(`/Media/Search?platform=${platform}&search=${search}`, {
            method: "GET",
        });
        const data = await response.json();
        return {
            status: response.status,
            data: data.data,
        };
    }

    /**
     * Handling the change of the data form the search form of the
     * User-Interface of Extractio.
     * @param {InputEvent} event An event which takes place in the DOM.
     * @returns {void}
     */
    handleChange(event) {
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
     * Changing the color scheme according to the user's taste.
     * @param {MouseEvent} event An event which takes place in the DOM.
     * @returns {void}
     */
    setColorScheme(event) {
        const delay = 200;
        const color_scheme = (String(event.target.parentElement.parentElement.value) == "light") ? "dark" : "light";
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
        this.tracker.sendEvent("color_scheme_updated", {
            color_scheme: color_scheme,
        })
        .then(() => {
            return this.updateSession(color_scheme);
        })
        .then((status) => {
            console.log(`Request: PUT /Session\nStatus: ${status}`);
            setTimeout(() => {
                window.location.href = window.location.href;
            }, delay);
        })
        .catch((error) => {
            console.error("An error occurred while sending the event or setting the route!\nError: ", error);
            setTimeout(() => {
                window.location.href = window.location.href;
            }, delay);
        });
    }

    /**
     * Checking the response of the server to handle it correctly.
     * @param {string} color_scheme The color scheme of the application.
     * @returns {Promise<number>}
     */
    async updateSession(color_scheme) {
        const response = await fetch("/Session/", {
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
        if (response.status == 202) {
            localStorage.removeItem("session");
        }
        return response.status;
    }

    /**
     * Rendering the component
     * @returns {React.Component}
     */
    render() {
        return (
            <header>
                <nav>
                    <div>
                        <a href="/">Extractio</a>
                    </div>
                    <div>
                        <form method="GET" onSubmit={this.handleSubmit.bind(this)}>
                            <button class="active">
                                <i class="fa fa-search"></i>
                            </button>
                            <input
                                type="search"
                                placeholder="Search..."
                                name="search"
                                value={this.state.Media.search}
                                onChange={this.handleChange.bind(this)}
                                required
                            />
                        </form>
                        <div>
                            <button
                                name="colorSchemeChanger"
                                value={this.state.Session.Client.color_scheme}
                                onClick={this.setColorScheme.bind(this)}
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