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
     * Rendering the component
     * @returns {HTMLHeaderElement}
     */
    render() {
        const application_data: {System: {color_scheme: string}} = {
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

// Rendering the page
ReactDOM.render(<Homepage />, document.body);