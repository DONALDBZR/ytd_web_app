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
        const related_content = JSON.parse(localStorage.getItem("related_content")).data;
        this.setState((previous) => ({
            ...previous,
            Media: {
                ...previous.Media,
                RelatedContents: related_content,
            },
        }));
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