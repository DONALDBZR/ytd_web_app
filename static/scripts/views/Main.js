/**
 * The component that is the main for all of the pages
 */
class Main extends React.Component {
    /**
     * Constructing the application from React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        /**
         * States of the application
         * @type {{ System: { view_route: string, status: int, message: string, url: string }, Media: { search: string, YouTube: { uniform_resource_locator: string, title: string, author: string, author_channel: string, views: int, published_at: string, thumbnail: string, duration: string, identifier: string, File: { audio: string?, video: string? } } } }}
         */
        this.state = {
            System: {
                view_route: "",
                status: 0,
                message: "",
                url: "",
            },
            Media: {
                search: "",
                YouTube: {
                    uniform_resource_locator: "",
                    title: "",
                    author: "",
                    author_channel: "",
                    views: 0,
                    published_at: "",
                    thumbnail: "",
                    duration: "",
                    identifier: "",
                    File: {
                        audio: "",
                        video: "",
                    },
                },
            },
        };
    }
    /**
     * Running the methods needed as soon as the component has been successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.getRoute();
    }
    /**
     * Setting the view route of the application.
     * @returns {void}
     */
    getRoute() {
        this.setState((previous) => ({
            System: {
                ...previous.System,
                view_route: window.location.pathname,
            },
        }));
    }
    /**
     * Handling any change that is made in the user interface
     * @param {Event} event
     * @returns {void}
     */
    handleChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;
        this.setState((previous) => ({
            Media: {
                ...previous.Media,
                [name]: value,
            },
        }));
    }
    /**
     * Handling the form submission
     * @param {Event} event
     * @returns {void}
     */
    handleSubmit(event) {
        const delay = 200;
        const url = new URL(this.state.Media.search);
        const platform = url.host.replaceAll("www.", "").replaceAll(".com", "");
        event.preventDefault();
        fetch("/Media/Search", {
            method: "POST",
            body: JSON.stringify({
                Media: {
                    search: this.state.Media.search,
                    platform: platform,
                },
            }),
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((response) => response.json())
            .then((data) => this.setMediaYouTubeUniformResourceLocator(data))
            .then(() => this.setMediaYouTubeIdentifier())
            .then(() => this.setRoute())
            .then(() => this.redirector(delay, this.state.System.url));
    }
    /**
     * Retrieving the data of the media content that is searched by
     * the user.
     * @returns {void}
     */
    getMedia() {
        fetch("/Media", {
            method: "GET",
        })
            .then((response) => response.json())
            .then((data) => {
                if (
                    typeof data.Media.YouTube != "undefined" &&
                    ((typeof data.Media.YouTube.audio == "undefined" &&
                        typeof data.Media.YouTube.video == "undefined") ||
                        (typeof data.Media.YouTube.audio == "null" &&
                            typeof data.Media.YouTube.video == "null"))
                ) {
                    this.setState((previous) => ({
                        Media: {
                            ...previous.Media,
                            YouTube: {
                                ...previous.Media.YouTube,
                                uniform_resource_locator:
                                    data.Media.YouTube.uniform_resource_locator,
                                title: data.Media.YouTube.title,
                                author: data.Media.YouTube.author,
                                author_channel:
                                    data.Media.YouTube.author_channel,
                                views: data.Media.YouTube.views,
                                published_at: data.Media.YouTube.published_at,
                                thumbnail: data.Media.YouTube.thumbnail,
                                duration: data.Media.YouTube.duration,
                                identifier: data.Media.YouTube.identifier,
                                File: {
                                    ...previous.Media.YouTube.File,
                                    audio: null,
                                    video: null,
                                },
                            },
                        },
                    }));
                } else {
                    this.setState((previous) => ({
                        Media: {
                            ...previous.Media,
                            YouTube: {
                                ...previous.Media.YouTube,
                                uniform_resource_locator:
                                    data.Media.YouTube.uniform_resource_locator,
                                title: data.Media.YouTube.title,
                                author: data.Media.YouTube.author,
                                author_channel:
                                    data.Media.YouTube.author_channel,
                                views: data.Media.YouTube.views,
                                published_at: data.Media.YouTube.published_at,
                                thumbnail: data.Media.YouTube.thumbnail,
                                duration: data.Media.YouTube.duration,
                                identifier: data.Media.YouTube.identifier,
                                File: {
                                    ...previous.Media.YouTube.File,
                                    audio: data.Media.YouTube.audio,
                                    video: data.Media.YouTube.video,
                                },
                            },
                        },
                    }));
                }
            });
    }
    /**
     * Retrieving Media from the server by using its uniform
     * resource locator.
     * @returns {void}
     */
    retrieveMedia() {
        const delay = 200;
        const uniform_resource_locator = document.querySelector(
            "button[name='mediaDownloader']"
        ).value;
        const url = new URL(uniform_resource_locator);
        const platform = url.host.replaceAll("www.", "").replaceAll(".com", "");
        fetch("/Media/Download", {
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
        })
            .then((response) => response.json())
            .then((data) => {
                setTimeout(() => {
                    window.location.href = data.data.data.url;
                }, delay);
            });
    }
    /**
     * Redirecting the user to an intended url
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
     * Setting the uniform resource locator for a specific YouTube content.
     * @param {object} data The dataset from the server.
     * @returns {void}
     */
    setMediaYouTubeUniformResourceLocator(data) {
        this.setState((previous) => ({
            Media: {
                ...previous.Media,
                YouTube: {
                    ...previous.Media.YouTube,
                    uniform_resource_locator:
                        data.data.data.uniform_resource_locator,
                },
            },
        }));
    }
    /**
     * Extracting the identifier of a specific YouTube content.
     * @returns {void}
     */
    setMediaYouTubeIdentifier() {
        this.setState((previous) => ({
            Media: {
                ...previous.Media,
                YouTube: {
                    ...previous.Media.YouTube,
                    identifier:
                        this.state.Media.YouTube.uniform_resource_locator.replace(
                            "https://www.youtube.com/watch?v=",
                            ""
                        ),
                },
            },
        }));
    }
    /**
     * Setting the route to be redirected.
     * @returns {void}
     */
    setRoute() {
        // Verifying the view route before updating to the new route.
        if (this.state.System.view_route == "/Search") {
            this.setState((previous) => ({
                System: {
                    ...previous.System,
                    url: `${this.state.System.view_route}/${this.state.Media.YouTube.identifier}`,
                },
            }));
        } else {
            this.setState((previous) => ({
                System: {
                    ...previous.System,
                    url: `/Search/${this.state.Media.YouTube.identifier}`,
                },
            }));
        }
    }
    /**
     * Downloading the file retrieved from the server.
     * @param {Event} event
     * @returns {void}
     */
    getFile(event) {
        /**
         * Button that was clicked
         * @type {HTMLButtonElement}
         */
        const button = event.target.parentElement.parentElement;
        /**
         * Uniform resource locator of the file needed.
         * @type {string}
         */
        const file_location = button.value;
        let file_name = "";
        if (file_location.includes("/Public/Audio/")) {
            file_name = file_location
                .replace("/Public/Audio/", "")
                .replace(".mp3", "");
        } else if (file_location.includes("/Public/Video/")) {
            file_name = file_location
                .replace("/Public/Video/", "")
                .replace(".mp4", "");
        }
        fetch("/Download", {
            method: "POST",
            body: JSON.stringify({
                file: file_location,
                file_name: file_name,
            }),
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((response) => response.blob())
            .then((data) => {
                let a = document.createElement("a");
                a.href = window.URL.createObjectURL(data);
                a.download = file_name;
                a.click();
            });
    }
    /**
     * Rendering the component
     * @returns {HTMLElement}
     */
    render() {
        if (this.state.System.view_route.includes("Search")) {
            return <Search />;
        } else if (this.state.System.view_route.includes("Download")) {
            return <Download />;
        } else {
            return <Homepage />;
        }
    }
}
/**
 * The component to be rendered for the homepage
 */
class Homepage extends Main {
    /**
     * Constructing the application from React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
    }
    /**
     * Rendering the component
     * @returns {HTMLElement}
     */
    render() {
        return (
            <>
                <p>
                    The aim of the application is that software and contents
                    must be free and it allows anyone to get content from
                    certain platforms to be obtained for free as it is an
                    application developed for people by people.
                </p>
                <div>
                    <div>
                        <i class="fa-brands fa-youtube"></i>
                    </div>
                </div>
            </>
        );
    }
}
/**
 * The component to be rendered for the search page
 */
class Search extends Main {
    /**
     * Constructing the application from React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
    }
    /**
     * Rendering the component
     * @returns {HTMLMainElement}
     */
    render() {
        return (
            <>
                <form method="POST" onSubmit={this.handleSubmit.bind(this)}>
                    <input
                        type="search"
                        placeholder="Search..."
                        name="search"
                        value={this.state.Media.search}
                        onChange={this.handleChange.bind(this)}
                        required
                    />
                    <button>
                        <i class="fa fa-search"></i>
                    </button>
                </form>
                <Media />
            </>
        );
    }
}

/**
 * The Media Component that will render according the to the data retrieved
 */
class Media extends Search {
    /**
     * Constructing the media component and also inheriting the properties and states from the main
     * @param {*} props
     */
    constructor(props) {
        super(props);
    }
    /**
     * Running the methods needed as soon as the component has been successfully mounted
     * @returns {void}
     */
    componentDidMount() {
        if (window.location.pathname != "/Search") {
            this.getMedia();
        }
    }
    /**
     * Rendering the component
     * @returns {HTMLDivElement}
     */
    render() {
        if (
            window.location.pathname != "/Search" &&
            this.state.Media.YouTube.identifier != ""
        ) {
            return (
                <div className="Media">
                    <YouTube />
                </div>
            );
        }
    }
}
/**
 * The component that is the YouTube component given that it will only be rendered only when the data corresponds to it.
 */
class YouTube extends Media {
    /**
     * Constructing the Youtube component and also inheriting the properties and states from the media
     * @param {*} props
     */
    constructor(props) {
        super(props);
    }
    /**
     * Rendering the component
     * @returns {HTMLDivElement}
     */
    render() {
        return (
            <div className="YouTube">
                <div>
                    <a
                        href={this.state.Media.YouTube.uniform_resource_locator}
                        target="__blank"
                    >
                        <img src={this.state.Media.YouTube.thumbnail} />
                    </a>
                </div>
                <div class="data">
                    <div>{this.state.Media.YouTube.title}</div>
                    <div>
                        <a
                            href={this.state.Media.YouTube.author_channel}
                            target="__blank"
                        >
                            {this.state.Media.YouTube.author}
                        </a>
                    </div>
                    <div>
                        <div id="duration">
                            <div>Duration:</div>
                            <div>{this.state.Media.YouTube.duration}</div>
                        </div>
                        <div id="views">
                            <div>Views:</div>
                            <div>
                                {this.state.Media.YouTube.views.toLocaleString(
                                    "en-US"
                                )}
                            </div>
                        </div>
                    </div>
                    <div>
                        <button
                            name="mediaDownloader"
                            value={
                                this.state.Media.YouTube
                                    .uniform_resource_locator
                            }
                            onClick={this.retrieveMedia}
                        >
                            <i class="fa-solid fa-download"></i>
                        </button>
                    </div>
                </div>
            </div>
        );
    }
}
/**
 * The component to be rendered for the Download page
 */
class Download extends Main {
    /**
     * Constructing the application from React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
    }
    /**
     * Rendering the component
     * @returns {HTMLMainElement}
     */
    render() {
        if (this.state.System.view_route.includes("YouTube")) {
            return (
                <>
                    <YouTubeDownloader />
                </>
            );
        }
    }
}
/**
 * The component to be rendered for the Download page but only when it is for media from YouTube
 */
class YouTubeDownloader extends Main {
    /**
     * Constructing the application from React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
    }
    /**
     * Running the methods needed as soon as the component has been successfully mounted
     * @returns {void}
     */
    componentDidMount() {
        this.getMedia();
    }
    /**
     * Rendering the component
     * @returns {HTMLDivElement}
     */
    render() {
        return (
            <div class="YouTube">
                <div>
                    <a
                        href={this.state.Media.YouTube.uniform_resource_locator}
                        target="__blank"
                    >
                        <i class="fa-brands fa-youtube"></i>
                    </a>
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
// Rendering the page
ReactDOM.render(<Main />, document.querySelector("main"));
