import React, { Component } from "react";
import YouTube from "./YouTube";
import RelatedContents from "./RelatedContents";


/**
 * The component that will be used for the Search page that will have the data for the Media.
 */
class Media extends Component {
    /**
     * Constructing the component that will be used for the Media data type.
     * @param {*} props
     */
    constructor(props) {
        super(props);
    }

    /**
     * Rendering the component
     * @returns {React.JSX.Element}
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

export default Media;
