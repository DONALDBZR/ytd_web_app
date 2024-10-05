/**
 * The component for the search pages.
 */
class Search extends React.Component {
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
        return [<Header />, <Main />, <Footer />];
    }
}

ReactDOM.render(<Search />, document.body);