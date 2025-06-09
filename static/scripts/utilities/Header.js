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

    /**
     * Validating the server response and returning a structured result.
     * 
     * This function checks whether the `data` object from the server contains a valid `data` property of type object.  If valid, it returns the status and the structured response data.  If not, it logs an error and returns a default 400 response with an empty data object.
     * 
     * @param {Response} response The response from the server.
     * @param {{data?: {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file?: string|null, video_file?: string|null}}} data The data of the response.
     * @returns {{status: number, data: object}} An object containing the HTTP status and the validated response data or an empty object.
     */
    isValidResponse(response, data) {
        if (data.data && typeof data.data === "object") {
            return {
                status: response.status,
                data: data.data,
            };
        }
        console.error("Invalid data received from the server.");
        return {
            status: 400,
            data: {},
        };
    }

    /**
     * Sending a GET request to the Media API to retrieve metadata for a specific media item.
     * 
     * This function constructs a query to the backend using the provided media platform, type, and identifier.  If the server responds with a valid data structure, it returns the parsed metadata and the HTTP status.  If the response is invalid or an error occurs during the request, it logs the issue and returns a fallback result.
     * 
     * @param {string} platform - The name of the media platform.
     * @param {string} type - The media type.
     * @param {string} identifier - The unique identifier for the media.
     * @returns {Promise<{status: number, data: {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio_file?: string|null, video_file?: string|null} | {}}>} A promise resolving to an object with the HTTP status and media metadata, or an empty object on failure.
     */
    async getSearchMedia(platform, type, identifier) {
        try {
            const query = `/Media/Search?platform=${encodeURIComponent(platform)}&type=${encodeURIComponent(type)}&identifier=${encodeURIComponent(identifier)}`;
            const response = await fetch(query, { method: "GET" });
            const data = await response.json();
            return this.isValidResponse(response, data);
        } catch (error) {
            console.error(`Failed to retrieve metadata of media content.\nError: ${error.message}`);
            return {
                status: 500,
                data: {},
            };
        }
    }
}

export default Header;
