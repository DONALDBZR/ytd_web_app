/**
 * The component that is the YouTube component given that it
 * will only be rendered only when the data corresponds to it.
 */
class YouTube extends React.Component {
    /**
     * Constructing the YouTube component which will render the
     * data of the video from YouTube.
     * @param {*} props
     */
    constructor(props) {
        super(props);
        /**
         * The data for the properties of the Search component.
         * @type {{Media: {YouTube: {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}}, System: {data_loaded: boolean}}}
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
            System: {
                data_loaded: false,
            },
        };
        /**
         * The tracker class which will track the user's activity on
         * the application.
         * @type {Tracker}
         */
        this.tracker = window.Tracker;
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
     * The methods to be executed when the component has been
     * updated.
     * @returns {void}
     */
    componentDidUpdate() {
        if (!this.state.System.data_loaded) {
            setTimeout(() => {
                this.setData();
                console.info(`Route: ${window.location.pathname}\nComponent: Main.Search.Media.YouTube\nComponent Status: Update`);
            }, 2000);
        }
    }

    /**
     * Setting the main state of the component.
     * @returns {void}
     */
    setData() {
        const loading_icon = document.querySelector("#loading");
        const local_storage_data = localStorage.getItem("media");
        const media = (typeof local_storage_data == "string") ? JSON.parse(localStorage.getItem("media")).data : null;
        const data_loaded = (media != null);
        this.setState((previous) => ({
            ...previous,
            Media: {
                ...previous.Media,
                YouTube: (media) ? media : this.state.Media.YouTube,
            },
            System: {
                data_loaded: data_loaded,
            },
        }));
        if (data_loaded) {
            loading_icon.style.display = "none";
        }
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
        const response_uniform_resource_locator = (response.status == 201) ? `/Download/YouTube/${data.identifier}` : "";
        return {
            status: response.status,
            uniform_resource_locator: response_uniform_resource_locator,
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
     * Retrieving the height of the component for the title.
     * @param {string} title The title of the media content.
     * @returns {string}
     */
    getTitleHeight(title) {
        const limit = 56;
        const component_height_coefficient = 8.8;
        const coefficient = (title.length <= limit) ? 1 : Math.ceil(title.length / limit);
        const height_coefficient = component_height_coefficient / coefficient;
        if (window.outerWidth >= 1024) {
            return "calc(var(--youtube-data-height) / 4)";
        }
        if (window.outerWidth >= 640 && window.outerWidth < 1024) {
            return "calc(var(--data-height) / 4)";
        }
        return `calc(var(--metadata-height) / ${height_coefficient})`;
    }

    /**
     * Retrieving the font size of the title.
     * @param {string} title The title of the media content.
     * @returns {string}
     */
    getTitleFontSize(title) {
        const limit = 51;
        const coefficient = (title.length <= limit) ? 1 : 0.9 - (((title.length - limit) / limit) * 0.1);
        return `calc(var(--textSize) * ${coefficient})`;
    }

    /**
     * Handles the click event on a component.
     * @param {MouseEvent} event The click event.
     * @returns {void}
     */
    handleClick = (event) => {
        event.preventDefault();
        const uniform_resource_locator = (String(event.target.localName) == "a") ? String(event.target.href) : String(event.target.parentElement.href);
        this.tracker.sendEvent("click", {
            uniform_resource_locator: uniform_resource_locator,
        })
        .then(() => {
            window.open(uniform_resource_locator, "_blank");
        });
    };

    /**
     * Rendering the component
     * @returns {React.Component}
     */
    render() {
        if (this.state.System.data_loaded) {
            return (
                <div className="YouTube">
                    <div>
                        <a href={this.state.Media.YouTube.uniform_resource_locator} target="__blank" onClick={this.handleClick.bind(this)}>
                            <img src={this.state.Media.YouTube.thumbnail} />
                        </a>
                    </div>
                    <div class="data">
                        <div class="metadata">
                            <div style={{height: this.getTitleHeight(this.state.Media.YouTube.title), fontSize: this.getTitleFontSize(this.state.Media.YouTube.title)}}>{this.state.Media.YouTube.title}</div>
                            <div>
                                <a href={this.state.Media.YouTube.author_channel} target="__blank" onClick={this.handleClick.bind(this)}>{this.state.Media.YouTube.author}</a>
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
}