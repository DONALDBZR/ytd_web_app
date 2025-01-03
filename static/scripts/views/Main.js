/**
 * The component that is the main for all of the pages
 */
class Main extends React.Component {
    /**
     * Constructing the Main component of the application.
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
    }

    /**
     * Rendering the component for the main.
     * @returns {React.Component}
     */
    render() {
        if (window.location.pathname.includes("Search")) {
            return <MainSearch />;
        } else if (window.location.pathname.includes("Download/YouTube")) {
            return <MainDownload />;
        } else {
            return <MainHomepage />;
        }
    }
}