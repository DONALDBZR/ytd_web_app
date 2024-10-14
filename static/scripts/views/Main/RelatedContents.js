/**
 * The component that will render the contents that are related
 * to the content that is currently being displayed where the
 * identifier of content is related to them.
 */
class RelatedContents extends React.Component {
    /**
     * Constructing the component given that it will only render
     * the related contents with the properties and states of the
     * component.
     * @param {*} props The properties of the component.
     */
    constructor(props) {
        super(props);
        /**
         * The states of the component.
         * @type {{Media: {RelatedContents: [{duration: string, channel: string, title: string, uniform_resource_locator: string, author_channel: string, thumbnail: string}]}}
         */
        this.state = {
            Media: {
                RelatedContents: [],
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
        console.info(`Route: ${window.location.pathname}\nComponent: Main.Search.Media.RelatedContents\nComponent Status: Mount`);
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
            this.setRelatedContents()
            .then((status) => console.info(`Route: ${window.location.pathname}\nComponent: Main.Search.Media.YouTube\nComponent Status: Update\nAPI: /Media/RelatedContents\nAPI Status: ${status}`));
        }
        console.info(`Route: ${window.location.pathname}\nComponent: Main.Search.Media.YouTube\nComponent Status: Update`);
    }

    /**
     * Setting the data for the related contents.
     * @returns {Promise<number>}
     */
    async setRelatedContents() {
        const response = await this.getRelatedContents();
        const data = response.data;
        this.setState((previous) => ({
            ...previous,
            Media: {
                ...previous.Media,
                RelatedContents: data,
            },
        }));
        return response.status;
    }

    /**
     * Retrieving the related contents from the response retrieved
     * from the Media API.
     * @returns {Promise<{status: number, data: [{duration: string, channel: string, title: string, uniform_resource_locator: string, author_channel: string, thumbnail: string}]}>}
     */
    async getRelatedContents() {
        const response = await this.sendGetRelatedContentsRequest();
        return {
            status: response.status,
            data: await response.json(),
        };
    }

    /**
     * Sending the request to the server for the related contents
     * for the Media API to retrieve the contents.
     * @returns {Promise<Response>}
     */
    async sendGetRelatedContentsRequest() {
        const identifier = window.location.pathname.replace("/Search/", "");
        return fetch(`/Media/RelatedContents/${identifier}`, {
            method: "GET",
        });
    }

    /**
     * Rendering the component
     * @returns {React.Component}
     */
    render() {
        return (
            <div className="RelatedContents"></div>
        );
    }
}