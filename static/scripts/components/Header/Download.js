import React, { Component } from "react";
import ColorScheme from "./ColorScheme";
import HeaderUtilities from "../../utilities/Header";


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
        try {
            const uniform_resource_locator = new URL(this.state.Media.search);
            const platform = this.Header_Utilities.getPlatform(uniform_resource_locator);
            const type = (uniform_resource_locator.pathname.includes("shorts")) ? "Shorts" : "Video";
            const identifier = this.Header_Utilities.getIdentifier(uniform_resource_locator, type);
            this.Header_Utilities.handleSubmitIdentifierExists(identifier);
            this.Header_Utilities.searchMediaMetadata(platform, type, identifier, 200, this.tracker);
        } catch (error) {
            console.error(`There is an error while processing the uniform resource locator for searching the media content.\nError: ${error.message}`);
        }
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
