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
        /**
         * The states of the application
         * @type {{System: {view_route: string}}}
         */
        this.state = {
            System: {
                view_route: "",
            },
        };
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

// Rendering the page
ReactDOM.render(<Homepage />, document.body);