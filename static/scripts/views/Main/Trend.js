/**
 * The component to be rendered for the trends.
 */
class Trend extends React.Component {
    /**
     * Constructing the Trend component which is based on the Main
     * component of the Homepage.
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        /**
         * The states of the component.
         * @type {{Trend: [{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}]}}
         */
        this.state = {
            Trend: [],
        };
    }

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setData();
        console.info("Component: Homepage.Main.MainHomepage.Trend\nStatus: Mount");
    }

    /**
     * Setting the data for the weekly trend in the state for the
     * component.
     * @returns {void}
     */
    setData() {
        const trend = JSON.parse(localStorage.getItem("trend")).data;
        this.setState((previous) => ({
            ...previous,
            Trend: trend,
        }));
    }

    /**
     * Adding the mouse enter event handler for the trend list.
     * @returns {void}
     */
    handleTrendListMouseEnter() {
        const trend_list = document.querySelector("#Homepage main .Trend div");
        trend_list.style.animationPlayState = (window.innerWidth < 640) ? "paused" : "unset";
    }

    /**
     * Adding the mouse leave event handler for the trend list.
     * @returns {void}
     */
    handleTrendListMouseLeave() {
        const trend_list = document.querySelector("#Homepage main .Trend div");
        trend_list.style.animationPlayState = (window.innerWidth < 640) ? "running" : "unset";
    }

    /**
     * Rendering the media card.
     * @param {{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}} content
     * @return {React.Component}
     */
    renderMediaCard(content) {
        return (
            <div className="card" key={content.identifier}>
                <div>
                    <a href={content.uniform_resource_locator} target="__blank">
                        <img src={content.thumbnail} loading="lazy" alt={`Thumbnail for ${content.title}`} />
                    </a>
                </div>
                <div>
                    <div>{content.title}</div>
                    <div>
                        <a href={content.author_channel}>{content.author}</a>
                    </div>
                    <div>
                        <div>Duration:</div>
                        <div>{content.duration}</div>
                    </div>
                    <div>
                        <div>Views:</div>
                        <div>
                            {content.views.toLocaleString("en-US")}
                        </div>
                    </div>
                    <div>
                        <a href={`/Download/YouTube/${content.identifier}`}>
                            <i className="fa-solid fa-download"></i>
                        </a>
                    </div>
                </div>
            </div>
        );
    }

    /**
     * Rendering the component
     * @returns {React.Component}
     */
    render() {
        const delay = 8;
        const width = (window.innerWidth < 640) ? `${window.innerWidth * this.state.Trend.length}px` : `${window.innerWidth}px`;
        const animation = (window.innerWidth < 640) ? `trend-scroll ${delay * this.state.Trend.length}s linear infinite` : "none";
        return (
            <div className="Trend">
                <div style={{width: width, animation: animation}} onMouseEnter={this.handleTrendListMouseEnter} onMouseLeave={this.handleTrendListMouseLeave}>
                    {this.state.Trend.map((content) => this.renderMediaCard(content))}
                </div>
            </div>
        );
    }
}