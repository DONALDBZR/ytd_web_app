/**
 * The component to be rendered for the search page
 */
class Search extends React.Component {
    /**
     * Constructing the Search component of the application.
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        /**
         * The data for the properties of the Search component.
         * @type {{}}
         */
        this.state = {};
    }

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setData();
        console.info(`Route: ${window.location.pathname}\nComponent: Main.Search\nComponent Status: Mount`);
    }

    /**
     * Updating the component as soon as the states are different.
     * @param {{data: {System: {view_route: string, dom_element: HTMLElement}}}} previous_props The properties of the component
     * @returns {void}
     */
    componentDidUpdate(previous_props) {
        if (this.props != previous_props) {
            this.setData();
        }
        console.info(`Route: ${window.location.pathname}\nComponent: Main.Search\nComponent Status: Update`);
    }

    /**
     * Setting the main state of the component.
     * @returns {void}
     */
    setData() {
        this.setState((previous) => ({
            ...previous,
            System: this.props.data.System,
        }));
    }

    /**
     * Rendering the component
     * @returns {React.Component}
     */
    render() {
        /**
         * The properties of the Media component.
         * @type {{System: {dom_element: HTMLElement}}}
         */
        const media = {
            System: {
                dom_element: this.state.System.dom_element,
            },
        };
        return (
            <>
                <div id="loading">
                    <i class="fa-solid fa-spinner fa-spin"></i>
                </div>
                <Media data={media} />
            </>
        );
    }
}