import React, { Component } from "react";
import ColorScheme from "./ColorScheme";
import HeaderUtilities from "../../utilities/Header";


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
        /**
         * The utility class of the Header component.
         * @type {HeaderUtilities}
         */
        this.Header_Utilities = new HeaderUtilities();
    }

    /**
     * Running the methods needed as soon as the component has been successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setData();
    }

    /**
     * Updating the component as soon as there is an update in the states.
     * @returns {void}
     */
    componentDidUpdate() {
        if (!this.state.System.data_loaded) {
            setTimeout(() => this.setData(), 1000);
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
        console.info("The state of the application has been updated.");
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
