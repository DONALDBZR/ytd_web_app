/**
 * The utility class of the Header component.
 */
class Header {
    /**
     * * Sanitizing a string by escaping special HTML characters.
     * 
     * * This function replaces the following characters with their HTML entity equivalents:
     * - `&` → `&amp;`
     * - `<` → `&lt;`
     * - `>` → `&gt;`
     * - `"` → `&quot;`
     * - `'` → `&#039;`
     * - `/` → `&#x2F;`
     * @param {string} data The input string to be sanitized.
     * @returns {string}
     */
    sanitize(data) {
        const lookup = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#039;",
            "/": "&#x2F;"
        };
        return data.replaceAll(/[&<>"'\/]/g, (character) => lookup[character]);
    }

    /**
     * Retrieving the session data for the component.
     * @returns {?{session: {Client: {timestamp: number, color_scheme: string}}, data_loaded: boolean, view_route: string}}
     */
    setData() {
        const session = JSON.parse(localStorage.getItem("session"));
        const data_loaded = (session != null && window.Tracker);
        const root = document.querySelector(":root");
        const color_1 = (data_loaded) ? ((session.Client.color_scheme == "light") ? "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))" : "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))") : "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))";
        const color_2 = (data_loaded) ? ((session.Client.color_scheme == "light") ? "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))" : "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))") : "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))";
        const color_3 = "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (69 / 255)), calc(var(--percentage) * (65 / 255)))";
        const color_5 = (data_loaded) ? ((session.Client.color_scheme == "light") ? "rgba(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)), calc(var(--percentage) / 2))" : "rgba(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)), calc(var(--percentage) / 2))") : "rgba(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)), calc(var(--percentage) / 2))";
        root.style.setProperty("--color1", color_1);
        root.style.setProperty("--color2", color_2);
        root.style.setProperty("--color3", color_3);
        root.style.setProperty("--color5", color_5);
        if (!data_loaded) {
            return null;
        }
        return {
            session: session,
            data_loaded: data_loaded,
            view_route: window.location.pathname,
        };
    }

    /**
     * Retrieving the identifier of the content based on the type of the content and from the parsed uniform resource locator.
     * 
     * This function handles three types of YouTube uniform resource locators:
     * - Shorts uniform resource locators
     * - Shortened uniform resource locators
     * - Standard video uniform resource locators with query parameters
     * @param {URL} uniform_resource_locator A parsed URL object representing the media link.
     * @param {string} type The media type.
     * @returns {string|null}
     */
    getIdentifier(uniform_resource_locator, type) {
        if (type == "Shorts") {
            return uniform_resource_locator.pathname.replaceAll("/shorts/", "");
        }
        if (uniform_resource_locator.hostname == "youtu.be") {
            return uniform_resource_locator.pathname.slice(1);
        }
        return uniform_resource_locator.searchParams.get("v");
    }

    /**
     * Retrieving the host name which will be used as the platform for the search from the parsed uniform resource locator.
     * 
     * Currently, this function only supports YouTube uniform resource locators.  If the hostname does not match a known YouTube format, it throws an error.
     * @param {URL} uniform_resource_locator The parsed uniform resource locator.
     * @returns {string} The name of the supported platform.
     * @throws {Error} If the URL does not belong to a supported platform.
     */
    getPlatform(uniform_resource_locator) {
        const hostname = uniform_resource_locator.hostname.toLowerCase();
        if (hostname == "youtu.be" || hostname.includes("youtube")) {
            return "youtube";
        }
        throw new Error("The platform is not supported by the application.");
    }

    /**
     * Validating the presence of a media identifier extracted from a URL.
     * 
     * This function checks if the given identifier exists.  If it does not, it throws an error indicating that the media URL is invalid due to a missing identifier.
     * @param {string|null|undefined} identifier The media identifier extracted from the URL.
     * @returns {void}
     * @throws {Error} If the identifier is null, undefined, or an empty string.
     */
    handleSubmitIdentifierExists(identifier) {
        if (identifier) {
            return;
        }
        throw new Error("The uniform resource locator is invalid as the identifier cannot be extracted.");
    }
}

export default Header;
