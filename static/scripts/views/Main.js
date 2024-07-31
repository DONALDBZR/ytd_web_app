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
        if (window.location.pathname.includes("Search")) {
            const search = {
                System: this.state.System,
            };
            return <Search data={search} />;
        } else if (window.location.pathname.includes("Download")) {
            return <Download />;
        } else {
            const homepage = {
                System: this.state.System,
            };
            return <Homepage data={homepage} />;
        }
    }

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
         * @type {{System: {view_route: string, dom_element: HTMLElement}, Trend: [{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}]}}
         */
        this.state = {
            System: this.props.data.System,
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
        console.info(`Route: ${window.location.pathname}\nComponent: Main.Homepage\nComponent Status: Mount`);
        this.setTrend()
        .then((status) => console.info(`Route: ${window.location.pathname}\nComponent: Main.Homepage\nComponent Status: Mount\nTrend API Route: /\nTrend API Status: ${status}`));
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
     * Setting the data of the weekly trend in the state of the
     * component.
     * @returns {Promise<number>}
     */
    async setTrend() {
        const response = await this.getTrend();
        const response_data = response.data;
        this.setState((previous) => ({
            ...previous,
            Trend: response_data,
        }));
        return response.status;
    }

    /**
     * Retrieving the response's data.
     * @returns {Promise<{status: number, data: [{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}]}>}
     */
    async getTrend() {
        const server_response = await this.sendGetTrendRequest();
        return {
            status: server_response.status,
            data: await server_response.json(),
        };
    }

    /**
     * Sending a request to the server to retrieve the weekly trend
     * based on the usage of the application.
     * @returns {Promise<Response>}
     */
    async sendGetTrendRequest() {
        return fetch("/Trend/", {
            method: "GET",
        });
    }

    /**
     * Rendering the component
     * @returns {HTMLElement}
     */
    render() {
        /**
         * The data to be used for the Trend component.
         * @type {{Trend: [{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}]}}
         */
        const trend = {
            Trend: this.state.Trend,
        };
        return (
            <>
                <div id="loading">
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
                <Trend data={trend} />
            </>
        );
    }
}

/**
 * The component to be rendered for the trends
 */
class Trend extends Homepage {
    /**
     * Constructing the Trend component which is based on the
     * Homepage component.
     * @param {{data: {Trend: [{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}]}}} props The properties of the component
     */
    constructor(props) {
        super(props);
        this.props = props;
        /**
         * The state of the component.
         * @type {{Trend: [{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}]}}
         */
        this.state = {
            Trend: this.props.data.Trend,
        };
    }

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setData();
        console.info(`Route: ${window.location.pathname}\nComponent: Main.Homepage.Trend\nComponent Status: Mount`);
    }

    /**
     * Updating the component as soon as the states are different.
     * @param {{data: {Trend: [{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}]}}} previous_props The properties of the component
     * @returns {void}
     */
    componentDidUpdate(previous_props) {
        if (this.props != previous_props) {
            this.setData();
        }
        console.info(`Route: ${window.location.pathname}\nComponent: Main.Homepage.Trend\nComponent Status: Update`);
    }

    /**
     * Setting the main state of the component.
     * @returns {void}
     */
    setData() {
        this.setState((previous) => ({
            ...previous,
            Trend: this.props.data.Trend,
        }));
    }

    /**
     * Retrieving the width of the trend list's carousel.
     * @param {[{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}]} trend_list The list of media content
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
     * @param {[{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}]} trend_list The list of media content
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
     * Constructing the Search component of the application.
     * @param {{data: {System: {view_route: string, dom_element: HTMLElement}}}} props The properties of the component
     */
    constructor(props) {
        super(props);
        this.props = props;
        /**
         * The data for the properties of the Search component.
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
        console.info(`Route: ${window.location.pathname}\nComponent: Main.Search\nComponent Status: Mount`);
    }

    /**
     * Updating the component as soon as the states are different.
     * @param {{data: {System: {view_route: string, dom_element: HTMLElement}}}} previous_props The properties of the component
     * @returns {void}
     */
    componentDidUpdate(previous_props) {
        if (this.props != previous_props) {
            this.setData();
        }
        console.info(`Route: ${window.location.pathname}\nComponent: Main.Search\nComponent Status: Update`);
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
        /**
         * The properties of the Media component.
         * @type {{System: {dom_element: HTMLElement}}}
         */
        const media = {
            System: {
                dom_element: this.state.System.dom_element,
            },
        };
        return (
            <>
                <div id="loading">
                    <i class="fa-solid fa-spinner fa-spin"></i>
                </div>
                <Media data={media} />
            </>
        );
    }
}

/**
 * The component that will be used for the Search page that
 * will have the data for the Media.
 */
class Media extends Search {
    /**
     * Constructing the component that will be used for the Media
     * data type.
     * @param {{data: {System: {dom_element: HTMLElement}}}} props
     */
    constructor(props) {
        super(props);
        this.props = props;
        /**
         * The states of the application.
         * @type {{System: {dom_element: HTMLElement}}}
         */
        this.state = {
            System: {
                dom_element: this.props.data.System.dom_element,
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
        console.info(`Route: ${window.location.pathname}\nComponent: Main.Search.Media\nComponent Status: Mount`);
    }

    /**
     * Setting the main state of the component.
     * @returns {void}
     */
    setData() {
        this.setState((previous) => ({
            ...previous,
            System: {
                ...previous.System,
                dom_element: this.props.data.System.dom_element,
            },
        }));
    }

    /**
     * Updating the component as soon as the states are different.
     * @param {{data: {System: {dom_element: HTMLElement}}}} previous_props The properties of the component
     * @returns {void}
     */
    componentDidUpdate(previous_props) {
        if (this.props != previous_props) {
            this.setData();
        }
        console.info(`Route: ${window.location.pathname}\nComponent: Main.Search.Media\nComponent Status: Update`);
    }

    /**
     * Rendering the component
     * @returns {HTMLDivElement}
     */
    render() {
        /**
         * The properties of the Media component.
         * @type {{System: {dom_element: HTMLElement}}}
         */
        const media = {
            System: {
                dom_element: this.state.System.dom_element,
            },
        };
        return (
            <div className="Media">
                <YouTube data={media} />
                <RelatedContents data={media} />
            </div>
        );
    }
}

/**
 * The component that is the YouTube component given that it
 * will only be rendered only when the data corresponds to it.
 */
class YouTube extends Media {
    /**
     * Constructing the Youtube component and also inheriting the
     * properties and states from the media
     * @param {{data: {System: {dom_element: HTMLElement}}}} props
     */
    constructor(props) {
        super(props);
        this.props = props;
        /**
         * The states of the component.
         * @type {{System: {dom_element: HTMLElement, api_call: number}, Media: {YouTube: {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, published_at: string, views: number, thumbnail: string, File: {audio: string, video: string}}}}}
         */
        this.state = {
            System: {
                dom_element: this.props.data.System.dom_element,
                api_call: 0,
            },
            Media: {
                YouTube: {
                    uniform_resource_locator: "",
                    author: "",
                    title: "",
                    identifier: "",
                    author_channel: "",
                    published_at: "",
                    views: 0,
                    thumbnail: "",
                    File: {
                        audio: "",
                        video: "",
                    },
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
        console.info(`Route: ${window.location.pathname}\nComponent: Main.Search.Media.YouTube\nComponent Status: Mount`);
    }

    /**
     * Setting the main state of the component.
     * @returns {void}
     */
    setData() {
        this.setState((previous) => ({
            ...previous,
            System: {
                ...previous.System,
                dom_element: this.props.data.System.dom_element,
            },
        }));
    }

    /**
     * Updating the component as soon as the states are different.
     * @param {{data: {System: {dom_element: HTMLElement}}}} previous_props The properties of the component
     * @returns {void}
     */
    componentDidUpdate(previous_props) {
        let api_call = this.state.System.api_call;
        if (this.props != previous_props) {
            this.setData();
        }
        if (api_call < 1) {
            api_call += 1;
            this.setState((previous) => ({
                ...previous,
                System: {
                    ...previous.System,
                    api_call: api_call,
                },
            }));
            this.setMediaMetadata()
            .then((status) => console.info(`Route: ${window.location.pathname}\nComponent: Main.Search.Media.YouTube\nComponent Status: Update\nAPI: /Media\nAPI Status: ${status}`));
        }
        console.info(`Route: ${window.location.pathname}\nComponent: Main.Search.Media.YouTube\nComponent Status: Update`);
    }

    /**
     * Setting the metadata for the media content.
     * @returns {Promise<number>}
     */
    async setMediaMetadata() {
        const response = await this.getMedia();
        const data = response.data;
        if (typeof data.Media.YouTube != "undefined" && response.status == 200) {
            this.setState((previous) => ({
                ...previous,
                Media: {
                    ...previous.Media,
                    YouTube: {
                        ...previous.Media.YouTube,
                        uniform_resource_locator: data.Media.YouTube.uniform_resource_locator,
                        author: data.Media.YouTube.author,
                        title: data.Media.YouTube.title,
                        identifier: data.Media.YouTube.identifier,
                        author_channel: data.Media.YouTube.author_channel,
                        published_at: data.Media.YouTube.published_at,
                        thumbnail: data.Media.YouTube.thumbnail,
                        duration: data.Media.YouTube.duration,
                        views: data.Media.YouTube.views,
                        File: {
                            ...previous.Media.YouTube.File,
                            audio: data.Media.YouTube.audio_file,
                            video: data.Media.YouTube.video_file,
                        },
                    },
                },
            }))
        }
        document.querySelector("#loading").style.display = "none";
        return response.status;
    }

    /**
     * Retrieving the metadata of the media content from the
     * response retrieved from the Media API.
     * @returns {Promise<{status: number, data: {Media: {YouTube: {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}}}}>}
     */
    async getMedia() {
        const response = await this.sendGetMediaRequest();
        return {
            status: response.status,
            data: await response.json(),
        };
    }

    /**
     * Sending a GET request to the Media API to retrieve the
     * metadata of the media content.
     * @returns {Promise<Response>}
     */
    async sendGetMediaRequest() {
        return fetch(this.generateMetadata(), {
            method: "GET",
        });
    }

    /**
     * Generating the uniform resource locator for retrieving the
     * metadata of the content.
     * @returns {string}
     */
    generateMetadata() {
        if (window.location.pathname.includes("Search")) {
            return `/Media/${window.location.pathname.replace("/Search/", "")}`;
        } else {
            return `/Media/${window.location.pathname.replace("/Download/YouTube/", "")}`;
        }
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
                    <div class="metadata">
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
