import React, { Component } from "react";
import ColorScheme from "./ColorScheme";
import HeaderUtilities from "../utilities/Header";


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
                        <form method="GET" onSubmit={(event) => this.Header_Utilities.handleSubmit(event, this.tracker)}>
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
                                onClick={(event) => this.Header_Utilities.setColorScheme(event, this.tracker)}
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
