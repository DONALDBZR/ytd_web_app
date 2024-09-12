import React, { Component } from "react";
import ColorScheme from "./ColorScheme";


/**
 * The header of the page.
 */
class Header extends Component {
    /**
     * Constructing that application from the React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        /**
         * The states of the header.
         * @type {{Media: {search: string, YouTube: {uniform_resource_locator: string, identifier: string}}, System: {color_scheme: string, api_call: number, api_origin: string}}}
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
                api_call: 0,
                api_origin: "",
            },
        };
    }

    /**
     * Running the methods needed as soon as the component is
     * mounted.
     * @returns {void}
     */
    componentDidMount() {
        let api_call = this.state.System.api_call;
        if (api_call < 1) {
            this.setData(api_call);
        }
        console.info(`Route: ${window.location.pathname}\nComponent: Homepage.Header\nComponent Status: Mount`);
    }

    /**
     * Updating the component as soon as the states are different.
     * @returns {void}
     */
    componentDidUpdate() {
        let api_call = this.state.System.api_call;
        if (api_call < 1) {
            this.setData(api_call);
        }
        console.info(`Route: ${window.location.pathname}\nComponent: Homepage.Header\nComponent Status: Update`);
    }

    /**
     * Setting the data for the header.
     * @param {number} api_call
     * @returns {void}
     */
    setData(api_call) {
        api_call += 1;
        this.setState((previous) => ({
            ...previous,
            System: {
                ...previous.System,
                api_call: api_call,
            },
        }));
        this.setSession()
            .then((status) => console.info(`Route: ${window.location.pathname}\nComponent: Header\nAPI: /Session\nAPI Status: ${status}`));
    }

    /**
     * Setting the session of the user.
     * @returns {Promise<number>}
     */
    async setSession() {
        const current_time = Date.now() / 1000;
        let response = (localStorage.getItem("get_session") != null && Number(JSON.parse(localStorage.getItem("get_session")).Client.timestamp) + 3600 > current_time) ? {status: 304, data: JSON.parse(localStorage.getItem("get_session"))} : await this.getSessionResponse();
        let browser_session = response.data;
        this.setState((previous) => ({
            ...previous,
            System: {
                ...previous.System,
                color_scheme: browser_session.Client.color_scheme,
            },
        }));
        localStorage.setItem("get_session", JSON.stringify(response.data));
        return response.status;
    }

    /**
     * Changing the color scheme according to the user's taste.
     * @param {Event} event An event which takes place in the DOM.
     * @returns {void}
     */
    setColorScheme(event) {
        const delay = 200;
        const color_scheme = (String(event.target.parentElement.parentElement.value) == "light") ? "dark" : "light";
        console.log(`Color Scheme: ${color_scheme}`);
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
        const uniform_resource_locator = window.location.href;
        this.updateSession(color_scheme)
            .then((status) => console.log(`Request Method: PUT\nRoute: /Session\nStatus: ${status}`));
        setTimeout(() => {
            window.location.href = uniform_resource_locator;
        }, delay);
    }

    /**
     * Checking the response of the server to handle it correctly.
     * @param {string} color_scheme The color scheme of the application.
     * @returns {Promise<number>}
     */
    async updateSession(color_scheme) {
        const response = await this.sendUpdateSessionRequest(color_scheme);
        if (response.status == 202) {
            localStorage.setItem("get_session", JSON.stringify(await response.json()));
        }
        return response.status;
    }

    /**
     * Sending the request to update the session data.
     * @param {string} color_scheme The color scheme of the application.
     * @returns {Promise<Response>}
     */
    async sendUpdateSessionRequest(color_scheme) {
        const api_origin = (Number(window.location.port) == 591) ? "https://omnitechbros.ddns.net:591" : "https://omnitechbros.ddns.net:5000";
        return fetch(`${api_origin}/Session/`, {
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
        const api_origin = (Number(window.location.port) == 591) ? "https://omnitechbros.ddns.net:591" : "https://omnitechbros.ddns.net:5000";
        return fetch(`${api_origin}/Media/Search?platform=${platform}&search=${search}`, {
            method: "GET",
        });
    }

    /**
     * Sending the request to the server to retrieve the session
     * data.
     * @returns {Promise<Response>}
     */
    async sendGetSessionRequest() {
        const api_origin = (window.location.port == 591) ? "https://omnitechbros.ddns.net:591" : "https://omnitechbros.ddns.net:5000";
        return fetch(`${api_origin}/Session/`, {
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
     * Rendering the component for desktop users.
     * @returns {HTMLElement}
     */
    renderDesktop() {
        const color_scheme = {
            System: {
                color_scheme: this.state.System.color_scheme,
                api_call: this.state.System.api_call,
            },
        }
        return (
            <header>
                <nav>
                    <div>
                        <a href="/">Extractio</a>
                    </div>
                    <div>
                        <form method="GET" onSubmit={this.handleSearchSubmit.bind(this)} className="active">
                            <button>
                                <i className="fa fa-search"></i>
                            </button>
                            <input type="search" placeholder="Search..." name="search" value={this.state.Media.search} onChange={this.handleSearchChange.bind(this)} required />
                        </form>
                        <div>
                            <button name="colorSchemeChanger" value={this.state.System.color_scheme} onClick={this.setColorScheme.bind(this)}>
                                <ColorScheme data={color_scheme} />
                            </button>
                        </div>
                    </div>
                </nav>
            </header>
        );
    }

    /**
     * Rendering the component for tablet and mobile users.
     * @returns {HTMLElement}
     */
    renderTabletMobile() {
        const color_scheme = {
            System: {
                color_scheme: this.state.System.color_scheme,
                api_call: this.state.System.api_call,
            },
        }
        return (
            <header>
                <nav>
                    <div>
                        <a href="/">Extractio</a>
                    </div>
                    <div>
                        <form method="GET" onSubmit={this.handleSearchSubmit.bind(this)} className="active">
                            <button>
                                <i className="fa fa-search"></i>
                            </button>
                            <input type="search" placeholder="Search..." name="search" value={this.state.Media.search} onChange={this.handleSearchChange.bind(this)} required />
                        </form>
                        <div>
                            <button name="colorSchemeChanger" value={this.state.System.color_scheme} onClick={this.setColorScheme.bind(this)}>
                                <ColorScheme data={color_scheme} />
                            </button>
                        </div>
                        <div>
                            <button name="relatedContents">
                                <i class="fa-solid fa-puzzle-piece"></i>
                            </button>
                        </div>
                    </div>
                </nav>
            </header>
        );
    }

    /**
     * Rendering the component
     * @returns {HTMLElement}
     */
    render() {
        const color_scheme = {
            System: {
                color_scheme: this.state.System.color_scheme,
                api_call: this.state.System.api_call,
            },
        }
        return (
            <header>
                <nav>
                    <div>
                        <a href="/">Extractio</a>
                    </div>
                    <div>
                        <form method="GET" onSubmit={this.handleSearchSubmit.bind(this)} className="active">
                            <button>
                                <i className="fa fa-search"></i>
                            </button>
                            <input type="search" placeholder="Search..." name="search" value={this.state.Media.search} onChange={this.handleSearchChange.bind(this)} required />
                        </form>
                        <div>
                            <button name="colorSchemeChanger" value={this.state.System.color_scheme} onClick={this.setColorScheme.bind(this)}>
                                <ColorScheme data={color_scheme} />
                            </button>
                        </div>
                    </div>
                </nav>
            </header>
        );
    }
}

export default Header;