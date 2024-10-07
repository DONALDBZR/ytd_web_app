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
     * @returns {React.Component}
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