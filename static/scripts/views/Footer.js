/**
 * The component that is the footer for all of the pages
 */
class Footer extends React.Component {
    /**
     * Constructing the application from React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        this.state = {
            System: {
                view_route: "",
            },
        };
    }
}
// Rendering the page
ReactDOM.render(<Footer />, document.querySelector("header"));
