/**
 * The component for the homepage.
 */
class Homepage extends React.Component {
    /**
     * The constructor of the component.
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
    }
    

    /**
     * Rendering the component.
     * @returns {React.Component}
     */
    render() {
        return [<Header />, <Main />];
        // return [<Header />, <Main />, <Footer />];
    }
}

ReactDOM.render(<Homepage />, document.body);