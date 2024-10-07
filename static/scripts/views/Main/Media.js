/**
 * The component that will be used for the Search page that
 * will have the data for the Media.
 */
class Media extends React.Component {
    /**
     * Constructing the component that will be used for the Media
     * data type.
     * @param {*} props
     */
    constructor(props) {
        super(props);
        /**
         * The states of the application.
         * @type {{}}
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
        console.info(`Route: ${window.location.pathname}\nComponent: Search.Main.MainSearch.Media\nComponent Status: Mount`);
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
            <div className="Media">
                <YouTube />
                <RelatedContents />
            </div>
        );
    }
}