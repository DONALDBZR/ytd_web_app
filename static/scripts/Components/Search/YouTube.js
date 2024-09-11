import React, { Component } from "react";


/**
 * The component that is the YouTube component given that it
 * will only be rendered only when the data corresponds to it.
 */
class YouTube extends Component {
    /**
     * Constructing the Youtube component
     */
    constructor(props) {
        super(props);
        /**
         * The states of the component.
         * @type {{System: {api_call: number}, Media: {YouTube: {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, published_at: string, views: number, thumbnail: string, File: {audio: string, video: string}}}}}
         */
        this.state = {
            System: {
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
        let api_call = this.state.System.api_call;
        if (api_call < 1) {
            this.setData(api_call);
        }
        console.info(`Route: ${window.location.pathname}\nComponent: Main.YouTube\nComponent Status: Mount`);
    }

    /**
     * Setting the main state of the component.
     * @param {number} api_call
     * @returns {void}
     */
    setData(api_call) {
        api_call += 1;
        this.setState((previous) => ({
            ...previous,
            System: {
                ...previous.System,
                api_call: api_call,
            },
        }));
        this.setMediaMetadata()
            .then((status) => console.info(`Route: ${window.location.pathname}\nComponent: Main.YouTube\nAPI: /Media\nAPI Status: ${status}`));
    }

    /**
     * Updating the component.
     * @returns {void}
     */
    componentDidUpdate() {
        let api_call = this.state.System.api_call;
        if (api_call < 1) {
            this.setData(api_call);
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
        const api_origin = (window.location.port == 591) ? "https://omnitechbros.ddns.net:591" : "https://omnitechbros.ddns.net:5000";
        return fetch(`${api_origin}${this.generateMetadata()}`, {
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
     * Retrieving Media from the server by using its uniform
     * resource locator.
     * @returns {void}
     */
    retrieveMedia() {
        document.querySelector("#loading").style.display = "flex";
        const delay = 200;
        const uniform_resource_locator = document.querySelector("button[name='mediaDownloader']").value;
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
                        <img src={this.state.Media.YouTube.thumbnail} alt="Thumbnail" />
                    </a>
                </div>
                <div className="data">
                    <div className="metadata">
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
                        <button name="mediaDownloader" value={this.state.Media.YouTube.uniform_resource_locator} onClick={this.retrieveMedia}>
                            <i className="fa-solid fa-download"></i>
                        </button>
                    </div>
                </div>
            </div>
        );
    }
}

export default YouTube;