/**
 * The component that is the footer for all of the pages
 */
class Footer extends React.Component {
    /**
     * Rendering the component
     * @returns {HTMLFooterElement}
     */
    render() {
        return (
            <>
                <div>Extractio</div>
            </>
        );
    }
}
// Rendering the page
ReactDOM.render(<Footer />, document.querySelector("footer"));
