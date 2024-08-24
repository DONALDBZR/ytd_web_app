import React, { Component } from "react";


/**
 * The component to be rendered for the trends.
 */
class Trend extends Component {
    /**
     * Constructing the Trend component which is based on the Main
     * component of the Homepage.
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        /**
         * The states of the component.
         * @type {{Trend: [{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}], System: {api_call: number}}}
         */
        this.state = {
            Trend: [],
            System: {
                api_call: 0,
            },
        };
    }

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        const api_origin = (window.location.port == 591) ? "https://omnitechbros.ddns.net:591" : "https://omnitechbros.ddns.net:5000";
        let api_call = this.state.System.api_call;
        api_call++;
        this.setState((previous) => ({
            ...previous,
            System: {
                ...previous.System,
                api_call: api_call,
                api_origin: api_origin,
            },
        }));
        this.setTrend(api_origin)
        .then((status) => console.info(`Route: ${window.location.pathname}\nComponent: Homepage.Main.Trend\nComponent Status: Mount\nTrend API Route: /\nTrend API Status: ${status}`));
    }

    /**
     * Updating the component as soon as there is a change in the
     * properties.
     * @returns {void}
     */
    componentDidUpdate() {
        let api_call = this.state.System.api_call;
        if (api_call < 1) {
            api_call++;
            this.setState((previous) => ({
                ...previous,
                System: {
                    ...previous.System,
                    api_call: api_call,
                },
            }));
            this.setTrend()
            .then((status) => console.info(`Route: ${window.location.pathname}\nComponent: Homepage.Main.Trend\nComponent Status: Update\nTrend API Route: /\nTrend API Status: ${status}`));
        }
    }

    /**
     * Setting the data of the weekly trend in the state of the
     * component.
     * @param {string} api_origin
     * @returns {Promise<number>}
     */
    async setTrend(api_origin) {
        const response = await this.getTrend(api_origin);
        const response_data = response.data;
        this.setState((previous) => ({
            ...previous,
            Trend: response_data,
        }));
        return response.status;
    }

    /**
     * Retrieving the response's data.
     * @param {string} api_origin
     * @returns {Promise<{status: number, data: [{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}]}>}
     */
    async getTrend(api_origin) {
        const server_response = await this.sendGetTrendRequest(api_origin);
        return {
            status: server_response.status,
            data: await server_response.json(),
        };
    }

    /**
     * Sending a request to the server to retrieve the weekly trend
     * based on the usage of the application.
     * @param {string} api_origin
     * @returns {Promise<Response>}
     */
    async sendGetTrendRequest(api_origin) {
        return fetch(`${api_origin}/Trend/`, {
            method: "GET",
        });
    }

    /**
     * Retrieving the width of the trend list's carousel.
     * @param {[{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}]} trend_list The list of media content
     * @returns {string}
     */
    getTrendListWidth(trend_list) {
        return (window.innerWidth < 640) ? `${window.innerWidth * trend_list}px` : `${window.innerWidth}px`;
    }

    /**
     * Retrieving the animation of the trend list's carousel.
     * @param {[{uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file: string, video_file: string}]} trend_list The list of media content
     * @returns {string}
     */
    getTrendListAnimation(trend_list) {
        const delay = 8;
        return (window.innerWidth < 640) ? `trend-scroll ${delay * trend_list.length}s linear infinite` : "none";
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
     * Rendering the component
     * @returns {HTMLDivElement}
     */
    render() {
        return (
            <div className="Trend">
                <div style={{width: this.getTrendListWidth(this.state.Trend), animation: this.getTrendListAnimation(this.state.Trend)}} onMouseEnter={this.handleTrendListMouseEnter} onMouseLeave={this.handleTrendListMouseLeave}>
                    {this.state.Trend.map((content) => {
                        return (
                            <div class="card" key={content.identifier}>
                                <div>
                                    <a
                                        href={content.uniform_resource_locator}
                                        target="__blank"
                                    >
                                        <img src={content.thumbnail} loading="lazy" alt={`Thumbnail for ${content.title}`} />
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

export default Trend;