/**
 * The component to be rendered for the search page
 */
class MainSearch extends React.Component {
    /**
     * Constructing the Search component of the application.
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        /**
         * The data for the properties of the Search component.
         * @type {{Media: {YouTube: {uniform_resource_locator: string, author: string, title: string,identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string,audio_file: string, video_file: string}}}}
         */
        this.state = {
            Media: {},
        };
    }

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setData();
        console.info(`Route: ${window.location.pathname}\nComponent: Search.Main.MainSearch\nComponent Status: Mount`);
    }

    /**
     * Setting the main state of the component.
     * @returns {void}
     */
    setData() {
        const media = JSON.parse(localStorage.getItem("media")).data.Media;
        this.setData((previous) => ({
            ...previous,
            Media: media,
        }));
    }

    /**
     * Rendering the component
     * @returns {React.Component}
     */
    render() {
        return (
            <main>
                <div id="loading">
                    <i class="fa-solid fa-spinner fa-spin"></i>
                </div>
                <Media />
                <RelatedContents />
            </main>
        );
    }
}