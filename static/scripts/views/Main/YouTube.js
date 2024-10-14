/**
 * The component that is the YouTube component given that it
 * will only be rendered only when the data corresponds to it.
 */
class YouTube extends React.Component {
    /**
     * Constructing the Youtube component and also inheriting the
     * properties and states from the media
     * @param {*} props
     */
    constructor(props) {
        super(props);
        /**
         * The data for the properties of the Search component.
         * @type {{Media: {YouTube: {uniform_resource_locator: string, author: string, title: string,identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string,audio_file: string, video_file: string}}}}
         */
        this.state = {
            Media: {
                YouTube: {
                    uniform_resource_locator: "",
                    author: "",
                    title: "",
                    identifier: "",
                    author_channel: "",
                    views: 0,
                    published_at: "",
                    thumbnail: "",
                    duration: "",
                    audio_file: "",
                    video_file: ""
                },
            },
        };
    }

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setData();
        console.info(`Route: ${window.location.pathname}\nComponent: Search.Main.MainSearch.Media.YouTube\nComponent Status: Mount`);
    }

    /**
     * Setting the main state of the component.
     * @returns {void}
     */
    setData() {
        const loading_icon = document.querySelector("#loading");
        const media = JSON.parse(localStorage.getItem("media")).data.Media;
        this.setState((previous) => ({
            ...previous,
            Media: media,
        }));
        loading_icon.style.display = "none";
    }

    /**
     * Retrieving Media from the server by using its uniform
     * resource locator.
     * @param {MouseEvent} event The event that is to be handled
     * @returns {void}
     */
    retrieveMedia(event) {
        event.preventDefault();
        const loading_icon = document.querySelector("#loading");
        const delay = 200;
        const uniform_resource_locator = this.state.Media.YouTube.uniform_resource_locator;
        const platform = new URL(this.state.Media.YouTube.uniform_resource_locator).host.replaceAll("www.", "").replaceAll(".com", "");
        loading_icon.style.display = "flex";
        this.postMediaDownload(uniform_resource_locator, platform)
        .then((response) => this.manageResponse(response, delay));
    }

    /**
     * Managing the flow of the application based on the response
     * of the back-end.
     * @param {{status: number, uniform_resource_locator: string}} response The response from the back-end.
     * @param {number} delay The delay before the application.
     * @returns {void}
     */
    manageResponse(response, delay) {
        const uniform_resource_locator = (response.status == 201) ? response.uniform_resource_locator : window.location.href;
        this.redirector(delay, uniform_resource_locator);
    }

    /**
     * Sending the request to the server to download the media file
     * needed for the application.
     * @param {string} uniform_resource_locator The uniform resource locator of the content.
     * @param {string} platform The platform of the application needed.
     * @returns {Promise<{status: number, uniform_resource_locator: string}>}
     */
    async postMediaDownload(uniform_resource_locator, platform) {
        const response = await fetch("/Media/Download", {
            method: "POST",
            body: JSON.stringify({
                Media: {
                    uniform_resource_locator: uniform_resource_locator,
                    platform: platform,
                },
            }),
            headers: {
                "Content-Type": "application/json",
            },
        });
        const data = await response.json();
        const uniform_resource_locator = (response.status == 201) ? data.uniform_resource_locator : "";
        return {
            status: response.status,
            uniform_resource_locator: uniform_resource_locator,
        };
    }

    /**
     * Redirecting the user to an intended uniform resource
     * locator.
     * @param {number} delay The amount of time in milliseconds before firing the method
     * @param {string} uniform_resource_locator The route
     * @returns {void}
     */
    redirector(delay, uniform_resource_locator) {
        setTimeout(() => {
            window.location.href = uniform_resource_locator;
        }, delay);
    }

    /**
     * Rendering the component
     * @returns {React.Component}
     */
    render() {
        return (
            <div className="YouTube">
                <div>
                    <a href={this.state.Media.YouTube.uniform_resource_locator} target="__blank">
                        <img src={this.state.Media.YouTube.thumbnail} />
                    </a>
                </div>
                <div class="data">
                    <div class="metadata">
                        <div>{this.state.Media.YouTube.title}</div>
                        <div>
                            <a href={this.state.Media.YouTube.author_channel} target="__blank">{this.state.Media.YouTube.author}</a>
                        </div>
                        <div>
                            <div id="duration">
                                <div>Duration:</div>
                                <div>{this.state.Media.YouTube.duration}</div>
                            </div>
                            <div id="views">
                                <div>Views:</div>
                                <div>{this.state.Media.YouTube.views.toLocaleString("en-US")}</div>
                            </div>
                        </div>
                    </div>
                    <div>
                        <button name="mediaDownloader" value={this.state.Media.YouTube.uniform_resource_locator} onClick={this.retrieveMedia.bind(this)}>
                            <i class="fa-solid fa-download"></i>
                        </button>
                    </div>
                </div>
            </div>
        );
    }
}