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
     * Checking if the page is embedded or not.
     * @returns {void}
     */
    checkEmbedded() {
        if (window.top !== window.self) {
            this.isEmbedded = true;
        }
    }

    /**
     * Rendering the component.
     * @returns {React.JSX.Element[]|null}
     */
    render() {
        return (this.isEmbedded) ? null : [<Header />, <Main />, <Footer />];
    }
}

ReactDOM.render(<Homepage />, document.body);