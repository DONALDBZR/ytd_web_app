/**
 * The component to be rendered for the Download page but only
 * when it is for media from YouTube.
 */
class YouTubeDownloader extends React.Component {
    /**
     * Constructing the application from React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
    }

    componentDidMount() {
        this.getRoute();
        setTimeout(() => {
            if (window.location.pathname != "/Search/") {
                this.getMedia();
            }
        }, 1);
    }

    /**
     * Rendering the component
     * @returns {HTMLDivElement}
     */
    render() {
        return (
            <div class="YouTube">
                <div>
                    <video src={this.verifyFile()} controls autoplay></video>
                </div>
                <div>
                    <button
                        name="file_downloader"
                        value={this.state.Media.YouTube.File.audio}
                        onClick={this.getFile.bind(this)}
                    >
                        <i class="fa-solid fa-music"></i>
                    </button>
                </div>
                <div>
                    <button
                        name="file_downloader"
                        value={this.state.Media.YouTube.File.video}
                        onClick={this.getFile.bind(this)}
                    >
                        <i class="fa-solid fa-video"></i>
                    </button>
                </div>
            </div>
        );
    }
}