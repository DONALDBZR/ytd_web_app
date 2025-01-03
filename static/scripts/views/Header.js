/**
 * The component for the header.
 */
class Header extends React.Component {
    /**
     * The consturctor of the components.
     * @param {*} props 
     */
    constructor(props) {
        super(props);
    }
    
    /**
     * Rendering the component for the header.
     * @returns {React.Component}
     */
    render() {
        if (window.location.pathname.includes("Search")) {
            return <HeaderSearch />;
        } else if (window.location.pathname.includes("Download")) {
            return <HeaderDownload />;
        } else {
            return <HeaderHomepage />;
        }
    }
}
