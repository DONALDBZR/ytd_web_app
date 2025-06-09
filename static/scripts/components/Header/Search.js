import React, { Component } from "react";
import ColorScheme from "./ColorScheme";
import HeaderUtilities from "../../utilities/Header";


/**
 * The component to be rendered for the header of the search
 * page.
 */
class HeaderSearch extends Component {
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
        /**
         * The utility class of the Header component.
         * @type {HeaderUtilities}
         */
        this.Header_Utilities = new HeaderUtilities();
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
        const response = this.Header_Utilities.setData();
        this.setState((previous) => ({
            ...previous,
            Session: (response.data_loaded) ? response.session : this.state.Session,
            System: {
                ...previous.System,
                data_loaded: response.data_loaded,
                view_route: (response.data_loaded) ? response.view_route : "/",
            },
        }));
        this.tracker = (window.Tracker) ? window.Tracker : null;
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
            const platform = this.Header_Utilities.getPlatform(uniform_resource_locator);
            const type = (uniform_resource_locator.pathname.includes("shorts")) ? "Shorts" : "Video";
            const identifier = this.Header_Utilities.getIdentifier(uniform_resource_locator, type);
            this.Header_Utilities.handleSubmitIdentifierExists(identifier);
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
            console.log(`Request Method: GET\nRoute: /Media/Search?platform=${platform}&type=${type}&identifier=${identifier}\nStatus: ${status}\nEvent Listener: onSubmit\nReferrer: ${window.location.href}\nView Route: ${this.state.System.view_route}\nComponent: Search.Header.HeaderSearch\nDelay: ${delay} ms`);
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
            return String(this.Header_Utilities.sanitize(identifier));
        } catch (error) {
            console.error(`There is an error while extracting the YouTube identifier.\nError: ${error.message}`);
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
        this.updateColorScheme(color_scheme, 200, event.target.parentElement);
    }

    /**
     * Updating the application's color scheme by sending a tracking event, updating the user session, and handling the server response.  If any step fails, the page reloads after the specified delay.
     * @param {string} color_scheme - The desired color scheme to apply.
     * @param {number} delay - The time to wait before reloading the page in milliseconds, if needed.
     * @param {HTMLButtonElement} button - The button that triggers the event.
     * @returns {void}
     */
    updateColorScheme(color_scheme, delay, button) {
        const loading_icon = document.querySelector("#loading");
        loading_icon.style.display = "flex";
        this.tracker.sendEvent("color_scheme_updated", {
            color_scheme: color_scheme,
        })
        .then(() => this.updateSession(color_scheme))
        .then((status) => this.manageResponse(status, color_scheme, button, loading_icon))
        .catch((error) => {
            console.error(`An error occurred while sending the event or setting the route!\nError: ${error.message}`);
            setTimeout(() => window.location.reload(), delay);
        });
    }

    /**
     * Handling the server response after attempting to update the session.
     * 
     * - Throws an error if the response status is not 202 or session data is invalid.
     * - On success:
     *   - Updates the local session data with a new timestamp and selected color scheme.
     *   - Applies new CSS custom properties to reflect the selected theme.
     *   - Updates the icon inside the triggering button to reflect the theme state.
     *   - Hides the loading icon once processing is complete.
     * @param {number} status - The HTTP response status code from the server.
     * @param {string} color_scheme - The color scheme to apply.
     * @param {HTMLButtonElement} button - The button that triggered the update, its icon and value are updated.
     * @param {HTMLDivElement} loading_icon - The loading indicator element to hide after completion.
     * @returns {Promise<void>} Resolves when the session data, visual theme, and UI state are successfully updated.
     * @throws {Error} If the status is not 202, session data is invalid, or the icon is missing from the button.
     */
    async manageResponse(status, color_scheme, button, loading_icon) {
        if (status !== 202) {
            throw new Error(`Status: ${status}\nError: There is an issue with the application's API and the session cannot be updated.`);
        }
        const session = JSON.parse(localStorage.getItem("session"));
        if (!session || !session.Client) {
            throw new Error("Invalid session structure in localStorage.");
        }
        session.Client.timestamp = Date.now() / 1000;
        session.Client.color_scheme = color_scheme;
        localStorage.setItem("session", JSON.stringify(session));
        const root = document.querySelector(":root");
        const icon = button.querySelector("i");
        const color_1 = (color_scheme == "light") ? "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))" : "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))";
        const color_2 = (color_scheme == "light") ? "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))" : "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))";
        const color_5 = (color_scheme == "light") ? "rgba(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)), calc(var(--percentage) / 2))" : "rgba(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)), calc(var(--percentage) / 2))";
        root.style.setProperty("--color1", color_1);
        root.style.setProperty("--color2", color_2);
        root.style.setProperty("--color5", color_5);
        button.value = color_scheme;
        if (!icon) {
            throw new Error("The icon is not present in the DOM.");
        }
        icon.className = (color_scheme == "light") ? "fa-solid fa-toggle-off" : "fa-solid fa-toggle-on";
        loading_icon.style.display = "none";
        console.info(`Route: PUT /Session/\nStatus: ${status}`);
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

export default HeaderSearch;
