import React, { Component } from "react";
import ColorScheme from "./ColorScheme";
import HeaderUtilities from "../utilities/Header";


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
     * Running the methods needed as soon as the component has been successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setData();
    }

    /**
     * Setting the data for the component.
     * @returns {void}
     */
    setData() {
        if (this.state.System.data_loaded) {
            console.info(`Route: ${window.location.pathname}\nComponent: Header\nStatus: Loaded`);
            return;
        }
        this.getData();
    }

    /**
     * Retrieving the data from the `localStorage` to be set as the states of the application.
     * @returns {void}
     */
    getData() {
        const {session, data_loaded, view_route} = this.Header_Utilities.getSession();
        const delay = 1000;
        if (!data_loaded) {
            setTimeout(() => this.setData(), delay);
            return;
        }
        this.setState((previous) => ({
            ...previous,
            Session: session,
            System: {
                ...previous.System,
                data_loaded: data_loaded,
                view_route: view_route,
            },
        }));
        this.tracker = window.Tracker;
        setTimeout(() => this.setData(), delay);
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
                    <div>
                        <a href="/">Extractio</a>
                    </div>
                    <div>
                        <form
                            method="GET"
                            onSubmit={(event) => this.Header_Utilities.handleSubmit(event, this.tracker, this.state.Media.search)}
                        >
                            <button>
                                <i class="fa fa-search"></i>
                            </button>
                            <input
                                type="search"
                                placeholder="Search..."
                                name="search"
                                value={this.state.Media.search}
                                onChange={(event) => this.handleChange(event)}
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

export default HeaderSearch;
