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
         * The states of the component.
         * @type {*}
         */
        this.state = {};
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
     * @returns {React.Component}
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