/**
 * The component to be rendered for the Download portal
 */
class Downloader extends React.Component {
    /**
     * Constructing the application from React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
    }

    /**
     * Rendering the component for the download portal.
     * @returns {React.Component}
     */
    render() {
        if (window.location.pathname.includes("YouTube")) {
            return <YouTubeDownloader />;
        }
    }
}