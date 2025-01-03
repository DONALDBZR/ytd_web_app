/**
 * The component to be rendered for the Download page
 */
class MainDownload extends React.Component {
    /**
     * Constructing the application from React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
    }

    /**
     * Rendering the component for the download page.
     * @returns {React.Component}
     */
    render() {
        if (window.location.pathname.includes("YouTube")) {
            return <YouTubeDownloader />;
        }
    }
}