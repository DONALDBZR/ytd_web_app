/**
 * The component to be rendered for the search page
 */
class MainSearch extends React.Component {
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
     * Setting the main state of the component.
     * @returns {void}
     */
    setData() {
        
    }

    /**
     * Rendering the component
     * @returns {React.Component}
     */
    render() {
        return (
            <>
                <div id="loading">
                    <i class="fa-solid fa-spinner fa-spin"></i>
                </div>
                {/* <Media data={media} /> */}
            </>
        );
    }
}