import React, { Component } from "react";
import ColorScheme from "./ColorScheme";


/**
 * The component to be rendered for the header of the homepage.
 */
class HeaderHomepage extends Component {
    /**
     * Constructing the header of the homepage.
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
                view_route: "",
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
        const lookup = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#039;",
            "/": "&#x2F;"
        };
        return data.replaceAll(/[&<>"'\/]/g, (character) => lookup[character]);
    }

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setData();
        console.log("Component: Homepage.Header.HeaderHomepage\nStatus: Mount");
    }

    /**
     * Updating the component as soon as there is an update in the
     * states.
     * @returns {void}
     */
    componentDidUpdate() {
        if (!this.state.System.data_loaded) {
            setTimeout(() => {
                this.setData();
                console.log("Component: Homepage.Header.HeaderHomepage\nStatus: Updated");
            }, 1000);
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
        const color_1 = (data_loaded) ? ((session.Client.color_scheme == "light") ? "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))" : "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))") : "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))";
        const color_2 = (data_loaded) ? ((session.Client.color_scheme == "light") ? "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))" : "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))") : "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))";
        const color_3 = "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (69 / 255)), calc(var(--percentage) * (65 / 255)))";
        const color_5 = (data_loaded) ? ((session.Client.color_scheme == "light") ? "rgba(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)), calc(var(--percentage) / 2))" : "rgba(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)), calc(var(--percentage) / 2))") : "rgba(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)), calc(var(--percentage) / 2))";
        this.setState((previous) => ({
            ...previous,
            Session: (data_loaded) ? session : this.state.Session,
            System: {
                ...previous.System,
                data_loaded: data_loaded,
                view_route: (data_loaded) ? window.location.pathname : "/",
            },
        }));
        this.tracker = (window.Tracker) ? window.Tracker : null;
        root.style.setProperty("--color1", color_1);
        root.style.setProperty("--color2", color_2);
        root.style.setProperty("--color3", color_3);
        root.style.setProperty("--color5", color_5);
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
     * Retrieving the identifier of the content based on the type of the content and from the parsed uniform resource locator.
     * 
     * This function handles three types of YouTube uniform resource locators:
     * - Shorts uniform resource locators
     * - Shortened uniform resource locators
     * - Standard video uniform resource locators with query parameters
     * @param {URL} uniform_resource_locator A parsed URL object representing the media link.
     * @param {string} type The media type.
     * @returns {string|null}
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
            console.log(`Request Method: GET\nRoute: /Media/Search?platform=${platform}&type=${type}&identifier=${identifier}\nStatus: ${status}\nEvent Listener: onSubmit\nReferrer: ${window.location.href}\nView Route: ${this.state.System.view_route}\nComponent: Homepage.Header.HeaderHomepage\nDelay: ${delay} ms`);
            setTimeout(() => {
                window.location.href = this.state.System.view_route;
            }, delay);
        })
        .catch((error) => {
            console.error(`An error occurred while sending the event or setting the route!\nError: ${error.message}`);
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
     * Generating a route URL based on the API response and media type.
     * 
     * If the response status is not `200`, the current URL is returned.  Otherwise, constructs a new route using the media type and identifier.
     * 
     * @param {{status: number, identifier: string}} response - The API response object containing status and YouTube identifier.
     * @param {string} type - The media type.
     * @returns {string} - The resulting route path or the current window location if the response is not successful.
     */
    _setRoute(response, type) {
        if (response.status !== 200) {
            return window.location.href;
        }
        return (type === "Shorts") ? `/Search/Shorts/${response.identifier}` : `/Search/${response.identifier}`;
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
                identifier: new_identifier,
            };
        } catch (error) {
            console.error(`An error occurred while setting the YouTube identifier.\nError: ${error.message}`);
            throw new Error(error.message);
        }
    }

    /**
     * Extracting the YouTube video or media identifier from a given uniform resource locator.
     * 
     * This method parses the input URL, validates its domain against a list of disallowed domains, and retrieves the YouTube identifier based on the specified media type.
     * @param {string} uniform_resource_locator - The full YouTube uniform resource locator.
    * @param {string} type - The media type used to determine how the ID is extracted.
    * @returns {Promise<string>} - A promise that resolves to the sanitized YouTube identifier string.
    * @throws {Error} Will throw an error if the URL is invalid, belongs to a disallowed domain, or the identifier cannot be extracted.
     */
    async extractYouTubeIdentifier(uniform_resource_locator, type) {
        try {
            const parsed_uniform_resource_locator = new URL(uniform_resource_locator);
            this.__checkNotAllowedDomains(parsed_uniform_resource_locator);
            const identifier = this.getYouTubeIdentifier(parsed_uniform_resource_locator, type);
            this.isIdentifierExtracted(identifier);
            return String(this.sanitize(identifier));
        } catch (error) {
            console.error(`Error extracting YouTube identifier.\nError: ${error.message}`);
            throw new Error(error.message);
        }
    }

    /**
     * Validating that a YouTube identifier has been successfully extracted.
     * 
     * This method ensures that the provided identifier is not null, undefined, or an empty string.  It is typically called after attempting to extract an identifier from a uniform resource locator.
     * 
     * @param {?string} identifier - The extracted YouTube identifier to validate.
     * @returns {void}
     * @throws {Error} Throws an error if the identifier is missing or invalid.
     */
    isIdentifierExtracted(identifier) {
        if (typeof identifier === "string" && identifier.trim() !== "") {
            return;
        }
        throw new Error("The identifier could not be extracted or is invalid.");
    }

    /**
     * Extracting the YouTube identifier from a parsed uniform resource locator based on the media type.
     * 
     * Supports various YouTube uniform resource locator formats, including Shorts, Shortened and Standard.
     * @param {URL} uniform_resource_locator - A parsed `URL` object representing the YouTube link.
     * @param {string} type - The media type to guide the identifier extraction.
     * @returns {?string} - The extracted YouTube identifier if found, otherwise `null`.
     * @throws {Error} Throws if the uniform resource locator does not match supported YouTube formats or if extraction fails.
     */
    getYouTubeIdentifier(uniform_resource_locator, type) {
        const hostname = uniform_resource_locator.hostname.replace(/^www\./, "");
        if (type === "Shorts") {
            return uniform_resource_locator.pathname.replace("/shorts/", "").trim();
        }
        if (hostname === "youtu.be") {
            return uniform_resource_locator.pathname.slice(1).trim();
        }
        if (hostname === "youtube.com" && uniform_resource_locator.pathname.includes("/watch")) {
            return uniform_resource_locator.searchParams.get("v")?.trim() || null;
        }
        throw new Error(`Error while retrieving the YouTube identifier!\nUniform Resource Locator: ${uniform_resource_locator.href}`);
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
     * Fetching and setting the sanitized YouTube media uniform resource locator in the application state.
     * 
     * This function performs a backend request to fetch media information using the provided platform, type, and identifier.  If the response is successful, it sanitizes the returned uniform resource locator, clears any related cached media from `localStorage`, and updates the application state.
     * 
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
     * Sanitizing the given uniform resource locator by ensuring it belongs to an allowed domain.
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
     * Checking the uniform resource locator against the regular expression.
     * @param {RegExp} regular_expression Regular expression
     * @param {string} uniform_resource_locator Uniform Resource Locator
     * @returns {void}
     */
    __checkInvalidUniformResourceLocator(regular_expression, uniform_resource_locator) {
        if (regular_expression.test(uniform_resource_locator.href)) {
            return;
        }
        throw new Error(`Invalid YouTube uniform resource locator format!\nUniform Resource Locator: ${uniform_resource_locator.href}`);
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
     * Toggling the color scheme between light and dark modes based on the current value, and applies the new scheme using the `updateColorScheme` method.
     * @param {MouseEvent} event - The mouse event triggered by user interaction.  Expects the event target's parent element to contain a `value` indicating the current color scheme.
     * @returns {void}
     */
    setColorScheme(event) {
        event.preventDefault();
        const color_scheme = (String(event.target.parentElement.value.toLowerCase()) == "light") ? "dark" : "light";
        this.updateColorScheme(color_scheme, 200);
    }

    /**
     * Updating the application's color scheme by sending a tracking event, updating the user session, and handling the server response.  If any step fails, the page reloads after the specified delay.
     * @param {string} color_scheme - The desired color scheme to apply.
     * @param {number} delay - The time to wait before reloading the page in milliseconds, if needed.
     * @returns {void}
     */
    updateColorScheme(color_scheme, delay) {
        this.tracker.sendEvent("color_scheme_updated", {
            color_scheme: color_scheme,
        })
        .then(() => this.updateSession(color_scheme))
        .then((status) => this.manageResponse(status, delay))
        .catch((error) => {
            console.error(`An error occurred while sending the event or setting the route!\nError: ${error.message}`);
            setTimeout(() => window.location.reload(), delay);
        });
    }

    /**
     * Sending a PUT request to the server to update the user's session with the selected color scheme.  Validating the provided scheme before making the request.
     * @param {string} color_scheme - The desired color scheme to set.
     * @returns {Promise<number>}
     */
    async updateSession(color_scheme) {
        try {
            await this.isAllowedColorScheme(color_scheme);
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
            return response.status;
        } catch (error) {
            console.error(`The application has failed to update the session.\nError: ${error.message}`);
            throw new Error(error.message);
        }
    }

    /**
     * Validating whether the provided color scheme is allowed.
     * @param {string} color_scheme - The color scheme to validate.
     * @returns {Promise<void>} Resolves if the color scheme is valid.
     * @throws {Error} Throws an error with status 400 if the color scheme is invalid.
     */
    async isAllowedColorScheme(color_scheme) {
        const allowed_color_schemes = ["light", "dark"];
        if (allowed_color_schemes.includes(color_scheme)) {
            return;
        }
        throw new Error(`The color scheme is invalid.\nStatus: 400\nColor Scheme: ${color_scheme}`);
    }

    /**
     * Rendering the component
     * @returns {React.JSX.Element}
     */
    render() {
        return (
            <header>
                <nav>
                    <div class="active">
                        <a href="/">Extractio</a>
                    </div>
                    <div>
                        <form method="GET" onSubmit={this.handleSubmit.bind(this)}>
                            <button>
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

export default HeaderHomepage;
