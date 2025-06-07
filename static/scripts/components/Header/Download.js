import React, { Component } from "react";
import ColorScheme from "./ColorScheme";


/**
 * The component to be rendered for the header of the download
 * page.
 */
class HeaderDownload extends Component {
    /**
     * Constructing the header of the download page.
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        /**
         * The states of the component.
         * @type {{Session: {Client: {timestamp: number, color_scheme: string}}, Media: {search: string, YouTube: {uniform_resource_locator: string, identifier: string}}, System: {data_loaded: boolean}}}
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
        this.tracker = null;
    }

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setData();
        console.info("Component: Search.Header.HeaderDownload\nStatus: Mount");
    }

    /**
     * Running the methods needed whenever the component is
     * updated.
     * @returns {void}
     */
    componentDidUpdate() {
        if (!this.state.System.data_loaded) {
            setTimeout(() => {
                this.setData();
                console.info("Component: Search.Header.HeaderDownload\nStatus: Update");
            }, 2000);
        }
    }

    /**
     * Setting the data for the component.
     * @returns {void}
     */
    setData() {
        const session = JSON.parse(localStorage.getItem("session"));
        const data_loaded = (session != null && window.Tracker);
        const root = document.querySelector(":root");
        const color_1 = (session != null) ? ((session.Client.color_scheme == "light") ? "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))" : "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))") : "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))";
        const color_2 = (session != null) ? ((session.Client.color_scheme == "dark") ? "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))" : "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))") : "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))";
        const color_3 = "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (69 / 255)), calc(var(--percentage) * (65 / 255)))";
        const color_5 = (session != null) ? ((session.Client.color_scheme == "light") ? "rgba(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)), calc(var(--percentage) / 2))" : "rgba(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)), calc(var(--percentage) / 2))") : "rgba(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)), calc(var(--percentage) / 2))";
        this.setState((previous) => ({
            ...previous,
            Session: (data_loaded) ? session : this.state.Session,
            System: {
                data_loaded: data_loaded,
            },
        }));
        this.tracker = (window.Tracker) ? window.Tracker : null;
        root.style.setProperty("--color1", color_1);
        root.style.setProperty("--color2", color_2);
        root.style.setProperty("--color3", color_3);
        root.style.setProperty("--color5", color_5);
    }

    /**
     * Retrieving the host name which will be used as the platform for the search from the parsed uniform resource locator.
     * 
     * Currently, this function only supports YouTube uniform resource locators.  If the hostname does not match a known YouTube format, it throws an error.
     * @param {URL} uniform_resource_locator The parsed uniform resource locator.
     * @returns {string} The name of the supported platform.
     * @throws {Error} If the URL does not belong to a supported platform.
     */
    getPlatform(uniform_resource_locator) {
        const hostname = uniform_resource_locator.hostname.toLowerCase();
        if (hostname == "youtu.be" || hostname.includes("youtube")) {
            return "youtube";
        }
        throw new Error("The platform is not supported by the application.");
    }

    /**
     * Retrieving the identifier of the content based on the type of the content and from the parsed uniform resource locator.
     * 
     * This function handles three types of YouTube uniform resource locators:
     * - Shorts uniform resource locators
     * - Shortened uniform resource locators
     * - Standard video uniform resource locators with query parameters
     * @param {URL} uniform_resource_locator A parsed URL object representing the media link.
     * @param {string} type The media type.
     * @returns {?string}
     */
    getIdentifier(uniform_resource_locator, type) {
        if (type == "Shorts") {
            return uniform_resource_locator.pathname.replaceAll("/shorts/", "");
        }
        if (uniform_resource_locator.hostname == "youtu.be") {
            return uniform_resource_locator.pathname.slice(1);
        }
        return uniform_resource_locator.searchParams.get("v");
    }

    /**
     * Validating the presence of a media identifier extracted from a URL.
     * 
     * This function checks if the given identifier exists.  If it does not, it throws an error indicating that the media URL is invalid due to a missing identifier.
     * @param {string|null|undefined} identifier The media identifier extracted from the URL.
     * @returns {void}
     * @throws {Error} If the identifier is null, undefined, or an empty string.
     */
    handleSubmitIdentifierExists(identifier) {
        if (identifier) {
            return;
        }
        throw new Error("The uniform resource locator is invalid as the identifier cannot be extracted.");
    }

    /**
     * Handling the form submission event to extract metadata from a media URL.
     * 
     * This function prevents the default form submission behavior, displays a loading icon, parses the user-provided media URL to determine the platform, media type (video or shorts), and identifier, and then initiates metadata fetching via `searchMediaMetadata`.
     * @param {SubmitEvent} event An event which takes place in the DOM.
     * @returns {void}
     */
    handleSubmit(event) {
        event.preventDefault();
        const loading_icon = document.querySelector("main #loading");
        loading_icon.style.display = "flex";
        loading_icon.style.height = "-webkit-fill-available";
        try {
            const uniform_resource_locator = new URL(this.state.Media.search);
            const platform = this.getPlatform(uniform_resource_locator);
            const type = (uniform_resource_locator.pathname.includes("shorts")) ? "Shorts" : "Video";
            const identifier = this.getIdentifier(uniform_resource_locator, type);
            this.handleSubmitIdentifierExists(identifier);
            this.searchMediaMetadata(platform, type, identifier, 200);
        } catch (error) {
            console.error(`There is an error while processing the uniform resource locator for searching the media content.\nError: ${error.message}`);
        }
    }

    /**
     * Searching for the Media content and redirecting the user to the searched content.
     * 
     * This function builds the search uniform resource locator based on the media type, logs the search event using a tracking service, sets the route for the selected platform and media type, and finally redirects the user to the view route.  If any step fails, the page is reloaded after the delay.
     * @param {string} platform The media platform.
     * @param {string} type The media type.
     * @param {string} identifier The unique identifier for the media.
     * @param {number} delay Delay in milliseconds before redirection.
     * @returns {void}
     */
    searchMediaMetadata(platform, type, identifier, delay) {
        const search = (type == "Shorts") ? `https://www.youtube.com/shorts/${identifier}` : `https://www.youtube.com/watch?v=${identifier}`;
        this.tracker.sendEvent("search_submitted", {
            search_term: search,
        })
        .then(() => {
            return this.setRoute(platform, type, identifier);
        })
        .then((status) => {
            console.log(`Request Method: GET\nRoute: /Media/Search?platform=${platform}&type=${type}&identifier=${identifier}\nStatus: ${status}\nEvent Listener: onSubmit\nView Route: ${window.location.href}\nComponent: Search.Header.HeaderDownload\nDelay: ${delay} ms`);
            setTimeout(() => {
                window.location.href = this.state.System.view_route;
            }, delay);
        })
        .catch((error) => {
            console.error("An error occurred while sending the event or setting the route!\nError: ", error);
            setTimeout(() => {
                window.location.reload();
            }, delay);
        });
    }

    /**
     * Setting the application's route based on the media identifier and platform.
     * 
     * This function calls an internal method to resolve the media identifier for the given platform and type.  It then updates the application state with the appropriate `view_route` depending on the response status.  If the status is 200, it redirects to a search-specific route; otherwise, it retains the current location.
     * @param {string} platform The media platform.
     * @param {string} type The media type.
     * @param {string} identifier The unique identifier for the media.
     * @returns {Promise<number>} The HTTP response status from the identifier resolution request.
     * @throws {Error} If an error occurs while resolving the media or updating the state.
     */
    async setRoute(platform, type, identifier) {
        try {
            const response = await this.setMediaYouTubeIdentifier(platform, type, identifier);
            this.setState((previous) => ({
                ...previous,
                System: {
                    ...previous.System,
                    view_route: this._setRoute(response, type),
                },
            }));
            return response.status;
        } catch (error) {
            console.error(`An error occurred while setting the route!\nError: ${error.message}`);
            throw new Error(error.message);
        }
    }

    /**
     * Resolving and setting the YouTube media identifier in the application state.
     * 
     * This function first retrieves a media uniform resource locator from the backend using the provided platform, type, and identifier.  It then extracts the canonical YouTube identifier from that uniform resource locator and updates the application state with this value under `Media.YouTube.identifier`.
     * 
     * @param {string} platform - The media platform.
     * @param {string} type - The media type.
     * @param {string} identifier - The initial identifier extracted from the user-provided uniform resource locator.
     * @returns {Promise<{status: number, identifier: string}>} The response status and the final, validated YouTube identifier.
     * @throws {Error} If an error occurs during the fetch or extraction process.
     */
    async setMediaYouTubeIdentifier(platform, type, identifier) {
        try {
            const response = await this.setMediaYouTubeUniformResourceLocator(platform, type, identifier);
            const status = response.status;
            const new_identifier = await this.extractYouTubeIdentifier(response.uniform_resource_locator, type);
            this.setState((previous) => ({
                ...previous,
                Media: {
                    ...previous.Media,
                    YouTube: {
                        ...previous.Media.YouTube,
                        identifier: new_identifier,
                    },
                },
            }));
            return {
                status: status,
                identifier: identifier,
            };
        } catch (error) {
            console.error(`An error occurred while setting the YouTube identifier.\nError: ${error.message}`);
            throw new Error(error.message);
        }
    }

    /**
     * Clearing specific `localStorage` entries if the HTTP status indicates a successful response.
     * 
     * This function removes the `media` and `related_content` keys from `localStorage` only if the provided status is exactly 200.  If the status differs, no action is taken.
     * 
     * @param {number} status - The HTTP status code returned from the server.
     * @returns {void}
     */
    clearLocalStorage(status) {
        if (status == 200) {
            localStorage.removeItem("media");
            localStorage.removeItem("related_content");
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
            console.error(`Invalid uniform resource locator!\nUniform Resource Locator: ${parsed_uniform_resource_locator}\nError: ${error.message}`);
            throw new Error(error.message);
        }
    }

    /**
     * Fetching and setting the sanitized YouTube media uniform resource locator in the application state.
     * 
     * This function performs a backend request to fetch media information using the provided platform, type, and identifier.  If the response is successful, it sanitizes the returned uniform resource locator, clears any related cached media from `localStorage`, and updates the application state.
     * @param {string} platform - The media platform.
     * @param {string} type - The media type.
     * @param {string} identifier - The media identifier.
     * @returns {Promise<{status: number, uniform_resource_locator: string}>} The HTTP status and sanitized uniform resource locator.
     * @throws {Error} If the uniform resource locator processing or state update fails.
     */
    async setMediaYouTubeUniformResourceLocator(platform, type, identifier) {
        const response = await this.getSearchMedia(platform, type, identifier);
        try {
            this.clearLocalStorage(response.status);
            const uniform_resource_locator = this.sanitizeUniformResourceLocator(decodeURIComponent(response.data.uniform_resource_locator));
            this.setState((previous) => ({
                Media: {
                    ...previous.Media,
                    YouTube: {
                        ...previous.Media.YouTube,
                        uniform_resource_locator: uniform_resource_locator,
                    },
                },
            }));
            return {
                status: response.status,
                uniform_resource_locator: uniform_resource_locator,
            };
        } catch (error) {
            console.error(`Failed to set the uniform resource locator.\nError: ${error.message}`);
            throw new Error(error.message);
        }
    }

    /**
     * Sending a GET request to the Media API to retrieve metadata for a specific media item.
     * 
     * This function constructs a query to the backend using the provided media platform, type, and identifier.  If the server responds with a valid data structure, it returns the parsed metadata and the HTTP status.  If the response is invalid or an error occurs during the request, it logs the issue and returns a fallback result.
     * 
     * @param {string} platform - The name of the media platform.
     * @param {string} type - The media type.
     * @param {string} identifier - The unique identifier for the media.
     * @returns {Promise<{status: number, data: {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file?: string|null, video_file?: string|null} | {}}>} A promise resolving to an object with the HTTP status and media metadata, or an empty object on failure.
     */
    async getSearchMedia(platform, type, identifier) {
        try {
            const query = `/Media/Search?platform=${encodeURIComponent(platform)}&type=${encodeURIComponent(type)}&identifier=${encodeURIComponent(identifier)}`;
            const response = await fetch(query, { method: "GET" });
            const data = await response.json();
            return this.isValidResponse(response, data);
        } catch (error) {
            console.error(`Failed to retrieve metadata of media content.\nError: ${error.message}`);
            return {
                status: 500,
                data: {},
            };
        }
    }

    /**
     * Validating the server response and returning a structured result.
     * 
     * This function checks whether the `data` object from the server contains a valid `data` property of type object.  If valid, it returns the status and the structured response data.  If not, it logs an error and returns a default 400 response with an empty data object.
     * 
     * @param {Response} response The response from the server.
     * @param {{data?: {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file?: string|null, video_file?: string|null}}} data The data of the response.
     * @returns {{status: number, data: object}} An object containing the HTTP status and the validated response data or an empty object.
     */
    isValidResponse(response, data) {
        if (data.data && typeof data.data === "object") {
            return {
                status: response.status,
                data: data.data,
            };
        }
        console.error("Invalid data received from the server.");
        return {
            status: 400,
            data: {},
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

export default HeaderDownload;
