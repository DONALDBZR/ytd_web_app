/**
 * The component to be rendered for the header of the homepage.
 */
class HeaderHomepage extends React.Component {
    /**
     * Constructing the header of the homepage.
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        /**
         * The states of the component.
         * @type {{Session: {Client: {timestamp: number, color_scheme: string}}, Media: {search: string, YouTube: {uniform_resource_locator: string, identifier: string}}}}
         */
        this.state = {
            Session: {
                Client: {
                    timestamp: 0,
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
        };
    }

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setData();
        this.getSession();
        console.log("Component: Header.Homepage\nStatus: Mount");
    }

    /**
     * Updating the component as soon as the states are different.
     * @param {{data: {System: {view_route: string, dom_element: HTMLElement}}}} previous_props The properties of the component.
     * @returns {void}
     */
    componentDidUpdate(previous_props) {
        this.setData(previous_props);
        console.log("Component: Header.Homepage\nStatus: Updated");
    }

    /**
     * Setting the data for the component.
     * @param {{data: {System: {view_route: string, dom_element: HTMLElement}}}} properties The properties of the component.
     * @returns {void}
     */
    setData(properties) {
        if (this.props != properties) {
            this.setState(() => ({
                System: {
                    view_route: this.props.data.System.view_route,
                    dom_element: this.props.data.System.dom_element,
                },
            }));
        }
    }

    /**
     * Rendering the component
     * @returns {React.Component}
     */
    render() {
        return (
            <header>
                <nav>
                    <div class="active">
                        <a href="/">Extractio</a>
                    </div>
                    <div>
                        <form method="GET" onSubmit={this.handleSearchSubmit.bind(this)}>
                            <button>
                                <i class="fa fa-search"></i>
                            </button>
                            <input
                                type="search"
                                placeholder="Search..."
                                name="search"
                                value={this.state.Media.search}
                                onChange={this.handleSearchChange.bind(this)}
                                required
                            />
                        </form>
                        <div>
                            <button
                                name="colorSchemeChanger"
                                value={this.state.System.color_scheme}
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