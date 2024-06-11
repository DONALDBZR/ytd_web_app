/**
 * The component that is the main for all of the pages
 */
class Main extends React.Component {
    /**
     * Constructing the Main component of the application which
     * reflects eveything of the Main tag.
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        /**
         * The states of the component
         * @type {{System: {view_route: string, dom_element: HTMLElement}}}
         */
        this.state = {
            System: {
                view_route: "",
                dom_element: "",
            },
        };
        // /**
        //  * States of the application
        //  * @type {{ System: { view_route: string, status: number, message: string, url: string }, Media: { search: string, YouTube: { uniform_resource_locator: string, title: string, author: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, identifier: string, File: { audio: string?, video: string? }, } }, Trend: [ { uniform_resource_locator: string, title: string, author: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, identifier: string, File: { audio: string?, video: string? } } ] }}
        //  */
        // this.state = {
        //     System: {
        //         view_route: "",
        //         status: 0,
        //         message: "",
        //         url: "",
        //     },
        //     Media: {
        //         search: "",
        //         YouTube: {
        //             uniform_resource_locator: "",
        //             title: "",
        //             author: "",
        //             author_channel: "",
        //             views: 0,
        //             published_at: "",
        //             thumbnail: "",
        //             duration: "",
        //             identifier: "",
        //             File: {
        //                 audio: "",
        //                 video: "",
        //             },
        //         },
        //     },
        //     Trend: [],
        // };
    }

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setData();
        console.info(`Route: ${this.state.System.view_route}\nComponent: Main\nComponent Status: Mount`);
    }

    /**
     * Setting the main state of the component.
     * @returns {void}
     */
    setData() {
        this.setState((previous) => ({
            System: {
                ...previous.System,
                view_route: window.location.pathname,
                dom_element: document.body.querySelector("main"),
            },
        }));
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
            /**
             * The data for the Homepage component.
             * @type {{System: {view_route: string, dom_element: HTMLElement}}}
             */
            const homepage = {
                System: this.state.System,
            };
            return <Homepage data={homepage} />;
        }
    }

    // /**
    //  * Retrieving the current trend.
    //  * @returns {void}
    //  */
    // getTrend() {
    //     if (
    //         this.state.System.view_route == "/" ||
    //         this.state.System.view_route == ""
    //     ) {
    //         fetch("/Trend/", {
    //             method: "GET",
    //         })
    //             .then((response) => response.json())
    //             .then((data) =>
    //                 this.setState({
    //                     Trend: data,
    //                 })
    //             );
    //     }
    // }

    // /**
    //  * Handling any change that is made in the user interface
    //  * @param {Event} event
    //  * @returns {void}
    //  */
    // handleChange(event) {
    //     const target = event.target;
    //     const value = target.value;
    //     const name = target.name;
    //     this.setState((previous) => ({
    //         Media: {
    //             ...previous.Media,
    //             [name]: value,
    //         },
    //     }));
    // }

    // /**
    //  * Handling the form submission
    //  * @param {Event} event
    //  * @returns {void}
    //  */
    // handleSubmit(event) {
    //     document.querySelector("#loading").style.display = "flex";
    //     const delay = 200;
    //     const url = new URL(this.state.Media.search);
    //     const platform = url.host.replaceAll("www.", "").replaceAll(".com", "");
    //     event.preventDefault();
    //     fetch("/Media/Search", {
    //         method: "POST",
    //         body: JSON.stringify({
    //             Media: {
    //                 search: this.state.Media.search,
    //                 platform: platform,
    //             },
    //         }),
    //         headers: {
    //             "Content-Type": "application/json",
    //         },
    //     })
    //         .then((response) => response.json())
    //         .then((data) => this.setMediaYouTubeUniformResourceLocator(data))
    //         .then(() => this.setMediaYouTubeIdentifier())
    //         .then(() => this.setRoute())
    //         .then(() => this.redirector(delay, this.state.System.url));
    // }

    // /**
    //  * Generating the uniform resource locator for retrieving the
    //  * metadata of the content.
    //  * @returns {string}
    //  */
    // generateMetadata() {
    //     if (this.state.System.view_route.includes("Search")) {
    //         return `/Media/${this.state.System.view_route.replace(
    //             "/Search/",
    //             ""
    //         )}`;
    //     } else {
    //         return `/Media/${this.state.System.view_route.replace(
    //             "/Download/YouTube/",
    //             ""
    //         )}`;
    //     }
    // }

    // /**
    //  * Setting the metadata into the state of the application.
    //  * @param {object} data Metadata
    //  * @returns {void}
    //  */
    // setMetadata(data) {
    //     if (
    //         typeof data.Media.YouTube != "undefined" &&
    //         ((typeof data.Media.YouTube.audio == "undefined" &&
    //             typeof data.Media.YouTube.video == "undefined") ||
    //             (typeof data.Media.YouTube.audio == "null" &&
    //                 typeof data.Media.YouTube.video == "null"))
    //     ) {
    //         this.setState((previous) => ({
    //             Media: {
    //                 ...previous.Media,
    //                 YouTube: {
    //                     ...previous.Media.YouTube,
    //                     uniform_resource_locator:
    //                         data.Media.YouTube.uniform_resource_locator,
    //                     title: data.Media.YouTube.title,
    //                     author: data.Media.YouTube.author,
    //                     author_channel: data.Media.YouTube.author_channel,
    //                     views: data.Media.YouTube.views,
    //                     published_at: data.Media.YouTube.published_at,
    //                     thumbnail: data.Media.YouTube.thumbnail,
    //                     duration: data.Media.YouTube.duration,
    //                     identifier: data.Media.YouTube.identifier,
    //                     File: {
    //                         ...previous.Media.YouTube.File,
    //                         audio: null,
    //                         video: null,
    //                     },
    //                 },
    //             },
    //         }));
    //     } else {
    //         this.setState((previous) => ({
    //             Media: {
    //                 ...previous.Media,
    //                 YouTube: {
    //                     ...previous.Media.YouTube,
    //                     uniform_resource_locator:
    //                         data.Media.YouTube.uniform_resource_locator,
    //                     title: data.Media.YouTube.title,
    //                     author: data.Media.YouTube.author,
    //                     author_channel: data.Media.YouTube.author_channel,
    //                     views: data.Media.YouTube.views,
    //                     published_at: data.Media.YouTube.published_at,
    //                     thumbnail: data.Media.YouTube.thumbnail,
    //                     duration: data.Media.YouTube.duration,
    //                     identifier: data.Media.YouTube.identifier,
    //                     File: {
    //                         ...previous.Media.YouTube.File,
    //                         audio: data.Media.YouTube.audio,
    //                         video: data.Media.YouTube.video,
    //                     },
    //                 },
    //             },
    //         }));
    //     }
    // }

    // /**
    //  * Retrieving the data of the media content that is searched by
    //  * the user.
    //  * @returns {void}
    //  */
    // getMedia() {
    //     fetch(this.generateMetadata(), {
    //         method: "GET",
    //     })
    //         .then((response) => response.json())
    //         .then((data) => this.setMetadata(data))
    //         .then(
    //             () =>
    //                 (document.querySelector("#loading").style.display = "none")
    //         );
    // }

    // /**
    //  * Retrieving Media from the server by using its uniform
    //  * resource locator.
    //  * @returns {void}
    //  */
    // retrieveMedia() {
    //     document.querySelector("#loading").style.display = "flex";
    //     const delay = 200;
    //     const uniform_resource_locator = document.querySelector(
    //         "button[name='mediaDownloader']"
    //     ).value;
    //     const url = new URL(uniform_resource_locator);
    //     const platform = url.host.replaceAll("www.", "").replaceAll(".com", "");
    //     fetch("/Media/Download", {
    //         method: "POST",
    //         body: JSON.stringify({
    //             Media: {
    //                 uniform_resource_locator: uniform_resource_locator,
    //                 platform: platform,
    //             },
    //         }),
    //         headers: {
    //             "Content-Type": "application/json",
    //         },
    //     })
    //         .then((response) => response.json())
    //         .then((data) => {
    //             setTimeout(() => {
    //                 window.location.href = data.data.data.url;
    //             }, delay);
    //         });
    // }

    // /**
    //  * Redirecting the user to an intended url
    //  * @param {number} delay The amount of time in milliseconds before firing the method
    //  * @param {string} uniform_resource_locator The route
    //  * @returns {void}
    //  */
    // redirector(delay, uniform_resource_locator) {
    //     setTimeout(() => {
    //         window.location.href = uniform_resource_locator;
    //     }, delay);
    // }

    // /**
    //  * Setting the uniform resource locator for a specific YouTube content.
    //  * @param {object} data The dataset from the server.
    //  * @returns {void}
    //  */
    // setMediaYouTubeUniformResourceLocator(data) {
    //     this.setState((previous) => ({
    //         Media: {
    //             ...previous.Media,
    //             YouTube: {
    //                 ...previous.Media.YouTube,
    //                 uniform_resource_locator:
    //                     data.data.data.uniform_resource_locator,
    //             },
    //         },
    //     }));
    // }

    // /**
    //  * Extracting the identifier of a specific YouTube content.
    //  * @returns {void}
    //  */
    // setMediaYouTubeIdentifier() {
    //     if (
    //         this.state.Media.YouTube.uniform_resource_locator.includes(
    //             "youtube"
    //         )
    //     ) {
    //         this.setState((previous) => ({
    //             Media: {
    //                 ...previous.Media,
    //                 YouTube: {
    //                     ...previous.Media.YouTube,
    //                     identifier:
    //                         this.state.Media.YouTube.uniform_resource_locator.replace(
    //                             "https://www.youtube.com/watch?v=",
    //                             ""
    //                         ),
    //                 },
    //             },
    //         }));
    //     } else {
    //         this.setState((previous) => ({
    //             Media: {
    //                 ...previous.Media,
    //                 YouTube: {
    //                     ...previous.Media.YouTube,
    //                     identifier:
    //                         this.state.Media.YouTube.uniform_resource_locator
    //                             .replace("https://youtu.be/", "")
    //                             .replace(/\?.*/, ""),
    //                 },
    //             },
    //         }));
    //     }
    // }

    // /**
    //  * Setting the route to be redirected.
    //  * @returns {void}
    //  */
    // setRoute() {
    //     // Verifying the view route before updating to the new route.
    //     if (this.state.System.view_route == "/Search") {
    //         this.setState((previous) => ({
    //             System: {
    //                 ...previous.System,
    //                 url: `${this.state.System.view_route}/${this.state.Media.YouTube.identifier}`,
    //             },
    //         }));
    //     } else {
    //         this.setState((previous) => ({
    //             System: {
    //                 ...previous.System,
    //                 url: `/Search/${this.state.Media.YouTube.identifier}`,
    //             },
    //         }));
    //     }
    // }

    // /**
    //  * Downloading the file retrieved from the server.
    //  * @param {Event} event
    //  * @returns {void}
    //  */
    // getFile(event) {
    //     /**
    //      * Button that was clicked
    //      * @type {HTMLButtonElement}
    //      */
    //     const button = event.target.parentElement.parentElement;
    //     /**
    //      * Uniform resource locator of the file needed.
    //      * @type {string}
    //      */
    //     const file_location = button.value;
    //     let file_name = this.state.Media.YouTube.title;
    //     if (file_location.includes("/Public/Audio/")) {
    //         file_name = `${file_name}.mp3`;
    //     } else if (file_location.includes("/Public/Video/")) {
    //         file_name = `${file_name}.mp4`;
    //     }
    //     fetch("/Download", {
    //         method: "POST",
    //         body: JSON.stringify({
    //             file: file_location,
    //             file_name: file_name,
    //         }),
    //         headers: {
    //             "Content-Type": "application/json",
    //         },
    //     })
    //         .then((response) => response.blob())
    //         .then((data) => {
    //             let a = document.createElement("a");
    //             a.href = window.URL.createObjectURL(data);
    //             a.download = file_name;
    //             a.click();
    //         });
    // }

    // /**
    //  * Checking that the location of the media file needed is in
    //  * the state of the application.
    //  * @returns {string|void}
    //  */
    // verifyFile() {
    //     // Verifying that the file exists in the server to be able to verify the directory of the file, else, redirect the user.
    //     if (this.state.Media.YouTube.File.video != null) {
    //         return this.getMediaFile();
    //     } else {
    //         window.location.href = `/Search/${this.state.Media.YouTube.identifier}`;
    //     }
    // }

    // /**
    //  * Retrieving the media file for the application to load.
    //  * @returns {string}
    //  */
    // getMediaFile() {
    //     // Verifying the directory of the file to get its relative directory.
    //     if (this.state.Media.YouTube.File.video.includes("extractio")) {
    //         return this.state.Media.YouTube.File.video.replace(
    //             "/home/darkness4869/Documents/extractio",
    //             ""
    //         );
    //     } else {
    //         return this.state.Media.YouTube.File.video.replace(
    //             "/var/www/html/ytd_web_app",
    //             ""
    //         );
    //     }
    // }
}

/**
 * The component to be rendered for the homepage
 */
class Homepage extends Main {
    /**
     * Constructing the Homepage component which is based on the
     * Main component.
     * @param {{data: {System: {view_route: string, dom_element: HTMLElement}}}} props The properties of the component
     */
    constructor(props) {
        super(props);
        this.props = props;
        /**
         * The state of the component
         * @type {{System: {view_route: string, dom_element: HTMLElement}}}
         */
        this.state = {
            System: this.props.data.System,
        };
    }

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setData();
        console.info(`Route: ${this.state.System.view_route}\nComponent: Main.Homepage\nComponent Status: Mount`);
    }

    /**
     * Setting the main state of the component.
     * @returns {void}
     */
    setData() {
        this.setState((previous) => ({
            ...previous,
            System: this.props.data.System,
        }));
    }

    /**
     * Rendering the component
     * @returns {HTMLElement}
     */
    render() {
        return (
            <>
                {/*<div id="loading">
                    <i class="fa-solid fa-spinner fa-spin"></i>
                </div>
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
                <Trend />*/}
            </>
        );
    }
}

/**
 * The component to be rendered for the trends
 */
class Trend extends Homepage {
    /**
     * Constructing the application from React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
    }

    /**
     * Retrieving the width of the trend list's carousel.
     * @param {[{uniform_resource_locator: string, title: string, author: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, identifier: string, File: {audio: string | null, video: string | null}}]} trend_list The list of media content
     * @returns {string}
     */
    getTrendListWidth(trend_list) {
        const application_width = window.innerWidth;
        let trend_list_width_pixelate = "";
        if (application_width < 640) {
            const trend_list_width = application_width * trend_list.length;
            trend_list_width_pixelate = `${trend_list_width}px`;
        } else {
            trend_list_width_pixelate = `${application_width}px`;
        }
        return trend_list_width_pixelate;
    }

    /**
     * Retrieving the animation of the trend list's carousel.
     * @param {[{uniform_resource_locator: string, title: string, author: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, identifier: string, File: {audio: string | null, video: string | null}}]} trend_list The list of media content
     * @returns {string}
     */
    getTrendListAnimation(trend_list) {
        const delay = 8;
        const application_width = window.innerWidth;
        let trend_list_animation = "";
        if (application_width < 640) {
            const trend_list_delay = delay * trend_list.length;
            trend_list_animation = `trend-scroll ${trend_list_delay}s linear infinite`;
        } else {
            trend_list_animation = `none`;
        }
        return trend_list_animation;
    }

    /**
     * Adding the mouse enter event handler for the trend list.
     * @returns {void}
     */
    handleTrendListMouseEnter() {
        const trend_list = document.querySelector("#Homepage main .Trend div");
        let animation_play_state = "";
        if (window.innerWidth < 640) {
            animation_play_state = "paused";
        } else {
            animation_play_state = "unset";
        }
        trend_list.style.animationPlayState = animation_play_state;
    }

    /**
     * Adding the mouse leave event handler for the trend list.
     * @returns {void}
     */
    handleTrendListMouseLeave() {
        const trend_list = document.querySelector("#Homepage main .Trend div");
        let animation_play_state = "";
        if (window.innerWidth < 640) {
            animation_play_state = "running";
        } else {
            animation_play_state = "unset";
        }
        trend_list.style.animationPlayState = animation_play_state;
    }

    /**
     * Rendering the component
     * @returns {HTMLDivElement}
     */
    render() {
        return (
            <div className="Trend">
                <div style={{width: this.getTrendListWidth(this.state.Trend), animation: this.getTrendListAnimation(this.state.Trend)}} onMouseEnter={this.handleTrendListMouseEnter} onMouseLeave={this.handleTrendListMouseLeave}>
                    {this.state.Trend.map((content) => {
                        return (
                            <div class="card">
                                <div>
                                    <a
                                        href={content.uniform_resource_locator}
                                        target="__blank"
                                    >
                                        <img src={content.thumbnail} />
                                    </a>
                                </div>
                                <div>
                                    <div>{content.title}</div>
                                    <div>
                                        <a href={content.author_channel}>
                                            {content.author}
                                        </a>
                                    </div>
                                    <div>
                                        <div>Duration:</div>
                                        <div>{content.duration}</div>
                                    </div>
                                    <div>
                                        <div>Views:</div>
                                        <div>
                                            {content.views.toLocaleString(
                                                "en-US"
                                            )}
                                        </div>
                                    </div>
                                    <div>
                                        <a
                                            href={`/Download/YouTube/${content.identifier}`}
                                        >
                                            <i class="fa-solid fa-download"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
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
                <div id="loading">
                    <i class="fa-solid fa-spinner fa-spin"></i>
                </div>
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

    componentDidMount() {
        this.getRoute();
        setTimeout(() => {
            if (this.state.System.view_route != "/Search/") {
                document.querySelector("#loading").style.display = "flex";
                this.getMedia();
            }
        }, 1);
    }

    /**
     * Rendering the component
     * @returns {HTMLDivElement}
     */
    render() {
        if (
            window.location.pathname != "/Search/" &&
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
 * The component to be rendered for the Download page but only
 * when it is for media from YouTube
 */
class YouTubeDownloader extends Main {
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
// Rendering the page
ReactDOM.render(<Main />, document.querySelector("main"));
