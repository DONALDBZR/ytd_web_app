/**
 * The component for the homepage.
 */
class Homepage extends React.Component {
    /**
     * Constructing the homepage.
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        /**
         * The flag for checking that the page is embedded or not.
         * @type {boolean}
         */
        this.embedded = false;
    }

    /**
     * Mounting the component.
     * @returns {void}
     */
    componentDidMount() {
        this.checkEmbedded();
    }

    /**
     * Rendering the component.
     * @returns {React.Component}
     */
    render() {
        return [<Header />, <Main />, <Footer />];
    }
}

ReactDOM.render(<Homepage />, document.body);