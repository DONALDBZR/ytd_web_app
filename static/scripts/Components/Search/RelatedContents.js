import React, { Component } from "react";


/**
 * The components that will render the related contents.
 */
class RelatedContents extends Component {
    /**
     * Constructing the Youtube component
     */
    constructor(props) {
        super(props);
        /**
         * The states of the component.
         * @type {{System: {api_call: number}, Media: [{duration: string, channel: string, title: string, uniform_resource_locator: string, author_channel: string, thumbnail: string}]}}
         */
        this.state = {
            System: {
                api_call: 0,
            },
            Media: [],
        };
    }

    /**
     * Executing all of the methods that are needed as soon as the
     * component is mounted.
     * @returns {void}
     */
    componentDidMount() {
        let api_call = this.state.System.api_call;
        if (api_call < 1) {
            this.setData(api_call);
        }
        console.info(`Route: ${window.location.pathname}\nComponent: Main.RelatedContents\nComponent Status: Mount`);
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
        console.info(`Route: ${window.location.pathname}\nComponent: Main.RelatedContents\nComponent Status: Update`);
    }

    /**
     * Setting the data of the component.
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
        this.setRelatedContents()
            .then((status) => console.info(`Route: ${window.location.pathname}\nComponent: Main.RelatedContents\nAPI: /Media/RelatedContents\nAPI Status: ${status}`));
    }

    /**
     * Setting the metadata for the related contents of the media
     * content.
     * @returns {Promise<number>}
     */
    async setRelatedContents() {
        const current_time = Date.now() / 1000;
        const identifier = window.location.pathname.replace("/Search/", "");
        // let response = (localStorage.getItem("get_related_contents") != null && Number(JSON.parse(localStorage.getItem("get_related_contents")).timestamp) + 604800 > current_time) await this.getRelatedContents();
        const data = response.data;
        this.setState((previous) => ({
            ...previous,
            Media: data,
        }));
        return response.status;
    }

    /**
     * Retrieving the metadata of the related content from the
     * response retrieved from the Media API.
     * @returns {Promise<{status: number, data: [{duration: string, channel: string, title: string, uniform_resource_locator: string, author_channel: string, thumbnail: string}], timestamp: number, api_request: string}>}
     */
    async getRelatedContents() {
        const current_time = Date.now() / 1000;
        const identifier = window.location.pathname.replace("/Search/", "");
        const api_request = `/Media/RelatedContents/${identifier}`;
        const response = await this.sendGetRelatedContentsRequest();
        return {
            status: response.status,
            data: await response.json(),
            timestamp: current_time,
            api_request: api_request,
        };
    }

    /**
     * Sending a GET request to the Media API to retrieve the
     * metadata of the related content.
     * @returns {Promise<Response>}
     */
    async sendGetRelatedContentsRequest() {
        const api_origin = (window.location.port == 591) ? "https://omnitechbros.ddns.net:591" : "https://omnitechbros.ddns.net:5000";
        const identifier = window.location.pathname.replace("/Search/", "");
        return fetch(`${api_origin}/Media/RelatedContents/${identifier}`, {
            method: "GET",
        });
    }

    /**
     * Rendering the media card for the related contents.
     * @param {{duration: string, channel: string, title: string, uniform_resource_locator: string, author_channel: string, thumbnail: string}} content
     * @returns {HTMLDivElement}
     */
    renderRelatedContentCard(content) {
        let identifier = content.uniform_resource_locator.replace("https://www.youtube.com/watch?v=", "");
        return (
            <div className="card" key={identifier}>
                <div>
                    <a href={content.uniform_resource_locator} target="__blank">
                        <img src={content.thumbnail} loading="lazy" alt={`Thumbnail for ${content.title}`} />
                    </a>
                </div>
                <div>
                    <div>{content.title}</div>
                    <div>
                        <a href={content.author_channel}>{content.channel}</a>
                    </div>
                    <div>
                        <div>Duration:</div>
                        <div>{content.duration}</div>
                    </div>
                    <div>
                        <a href={`/Download/YouTube/${identifier}`}>
                            <i className="fa-solid fa-download"></i>
                        </a>
                    </div>
                </div>
            </div>
        );
    }

    /**
     * Rendering the component.
     * @returns {HTMLDivElement}
     */
    render() {
        return (
            <div className="RelatedContents">
                {this.state.Media.map((content) => this.renderRelatedContentCard(content))}
            </div>
        );
    }
}

export default RelatedContents;