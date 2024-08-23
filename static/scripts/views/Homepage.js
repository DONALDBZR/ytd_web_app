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
         * @type {{Media: {search: string}, System: {color_scheme: string}}}
         */
        this.state = {
            Media: {
                search: "",
            },
            System: {
                color_scheme: "",
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
            <>
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
            </>
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

// Rendering the page
ReactDOM.render(<Homepage />, document.body);