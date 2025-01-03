/**
 * The component for the download pages.
 */
class Download extends React.Component {
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

ReactDOM.render(<Download />, document.body);