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

}

// Rendering the page
ReactDOM.render(<Homepage />, document.body);