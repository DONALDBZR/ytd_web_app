/**
 * The component that will be used for the Search page that will have the data for the Media.
 */
class Media extends React.Component {
    /**
     * Constructing the component that will be used for the Media data type.
     * @param {*} props
     */
    constructor(props) {
        super(props);
    }

    /**
     * Rendering the component
     * @returns {React.JSX.Component}
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