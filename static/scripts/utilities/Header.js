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
}

export default Header;
