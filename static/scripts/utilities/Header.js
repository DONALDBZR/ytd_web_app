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

    /**
     * Clearing specific `localStorage` entries if the HTTP status indicates a successful response.
     * 
     * This function removes the `media` and `related_content` keys from `localStorage` only if the provided status is exactly 200.  If the status differs, no action is taken.
     * 
     * @param {number} status - The HTTP status code returned from the server.
     * @returns {void}
     */
    clearLocalStorage(status) {
        if (status == 200) {
            localStorage.removeItem("media");
            localStorage.removeItem("related_content");
        }
    }

    /**
     * Checking domains that are not allowed.
     * @param {URL} uniform_resource_locator The parsed uniform resource locator
     * @returns {void}
     */
    __checkNotAllowedDomains(uniform_resource_locator) {
        const allowed_domains = ["www.youtube.com", "youtu.be"];
        if (allowed_domains.includes(uniform_resource_locator.hostname)) {
            return;
        }
        throw new Error(`The domain is not allowed!\nHost Name: ${uniform_resource_locator.hostname}`);
    }

    /**
     * Checking the uniform resource locator against the regular expression.
     * @param {RegExp} regular_expression Regular expression
     * @param {string} uniform_resource_locator Uniform Resource Locator
     * @returns {void}
     */
    __checkInvalidUniformResourceLocator(regular_expression, uniform_resource_locator) {
        if (regular_expression.test(uniform_resource_locator.href)) {
            return;
        }
        throw new Error(`Invalid YouTube uniform resource locator format!\nUniform Resource Locator: ${uniform_resource_locator.href}`);
    }

    /**
     * Sanitizing the given uniform resource locator by ensuring it belongs to an allowed domain.
     * @param {string} uniform_resource_locator The uniform resource locator
     * @returns {string}
     */
    sanitizeUniformResourceLocator(uniform_resource_locator) {
        const youtube_regular_expression = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/(watch\?v=|embed\/|shorts\/|)([a-zA-Z0-9_-]{11})(&.*)?$/;
        const parsed_uniform_resource_locator = new URL(uniform_resource_locator);
        try {
            this.__checkNotAllowedDomains(parsed_uniform_resource_locator);
            this.__checkInvalidUniformResourceLocator(youtube_regular_expression, parsed_uniform_resource_locator);
            return parsed_uniform_resource_locator.href;
        } catch (error) {
            console.error(`Invalid uniform resource locator!\nUniform Resource Locator: ${parsed_uniform_resource_locator}\nError: ${error.message}`);
            throw new Error(error.message);
        }
    }

    /**
     * Fetching and setting the sanitized YouTube media uniform resource locator in the application state.
     * 
     * This function performs a backend request to fetch media information using the provided platform, type, and identifier.  If the response is successful, it sanitizes the returned uniform resource locator, clears any related cached media from `localStorage`, and updates the application state.
     * 
     * @param {string} platform - The media platform.
     * @param {string} type - The media type.
     * @param {string} identifier - The media identifier.
     * @returns {Promise<{status: number, uniform_resource_locator: string}>} The HTTP status and sanitized uniform resource locator.
     * @throws {Error} If the uniform resource locator processing or state update fails.
     */
    async setMediaYouTubeUniformResourceLocator(platform, type, identifier) {
        const response = await this.getSearchMedia(platform, type, identifier);
        try {
            this.clearLocalStorage(response.status);
            const uniform_resource_locator = this.sanitizeUniformResourceLocator(decodeURIComponent(response.data.uniform_resource_locator));
            return {
                status: response.status,
                uniform_resource_locator: uniform_resource_locator,
            };
        } catch (error) {
            console.error(`Failed to set the uniform resource locator.\nError: ${error.message}`);
            throw new Error(error.message);
        }
    }

    /**
     * Extracting the YouTube identifier from a parsed uniform resource locator based on the media type.
     * 
     * Supports various YouTube uniform resource locator formats, including Shorts, Shortened and Standard.
     * @param {URL} uniform_resource_locator - A parsed `URL` object representing the YouTube link.
     * @param {string} type - The media type to guide the identifier extraction.
     * @returns {?string} - The extracted YouTube identifier if found, otherwise `null`.
     * @throws {Error} Throws if the uniform resource locator does not match supported YouTube formats or if extraction fails.
     */
    getYouTubeIdentifier(uniform_resource_locator, type) {
        const hostname = uniform_resource_locator.hostname.replace(/^www\./, "");
        if (type === "Shorts") {
            return uniform_resource_locator.pathname.replace("/shorts/", "").trim();
        }
        if (hostname === "youtu.be") {
            return uniform_resource_locator.pathname.slice(1).trim();
        }
        if (hostname === "youtube.com" && uniform_resource_locator.pathname.includes("/watch")) {
            return uniform_resource_locator.searchParams.get("v")?.trim() || null;
        }
        throw new Error(`Error while retrieving the YouTube identifier!\nUniform Resource Locator: ${uniform_resource_locator.href}`);
    }

    /**
     * Validating that a YouTube identifier has been successfully extracted.
     * 
     * This method ensures that the provided identifier is not null, undefined, or an empty string.  It is typically called after attempting to extract an identifier from a uniform resource locator.
     * 
     * @param {?string} identifier - The extracted YouTube identifier to validate.
     * @returns {void}
     * @throws {Error} Throws an error if the identifier is missing or invalid.
     */
    isIdentifierExtracted(identifier) {
        if (typeof identifier === "string" && identifier.trim() !== "") {
            return;
        }
        throw new Error("The identifier could not be extracted or is invalid.");
    }

    /**
     * Extracting the YouTube video or media identifier from a given uniform resource locator.
     * 
     * This method parses the input URL, validates its domain against a list of disallowed domains, and retrieves the YouTube identifier based on the specified media type.
     * @param {string} uniform_resource_locator - The full YouTube uniform resource locator.
    * @param {string} type - The media type used to determine how the ID is extracted.
    * @returns {Promise<string>} - A promise that resolves to the sanitized YouTube identifier string.
    * @throws {Error} Will throw an error if the URL is invalid, belongs to a disallowed domain, or the identifier cannot be extracted.
     */
    async extractYouTubeIdentifier(uniform_resource_locator, type) {
        try {
            const parsed_uniform_resource_locator = new URL(uniform_resource_locator);
            this.__checkNotAllowedDomains(parsed_uniform_resource_locator);
            const identifier = this.getYouTubeIdentifier(parsed_uniform_resource_locator, type);
            this.isIdentifierExtracted(identifier);
            return String(this.sanitize(identifier));
        } catch (error) {
            console.error(`Error extracting YouTube identifier.\nError: ${error.message}`);
            throw new Error(error.message);
        }
    }

    /**
     * Resolving and setting the YouTube media identifier in the application state.
     * 
     * This function first retrieves a media uniform resource locator from the backend using the provided platform, type, and identifier.  It then extracts the canonical YouTube identifier from that uniform resource locator and updates the application state with this value under `Media.YouTube.identifier`.
     * 
     * @param {string} platform - The media platform.
     * @param {string} type - The media type.
     * @param {string} identifier - The initial identifier extracted from the user-provided uniform resource locator.
     * @returns {Promise<{status: number, identifier: string}>} The response status and the final, validated YouTube identifier.
     * @throws {Error} If an error occurs during the fetch or extraction process.
     */
    async setMediaYouTubeIdentifier(platform, type, identifier) {
        try {
            const response = await this.setMediaYouTubeUniformResourceLocator(platform, type, identifier);
            const status = response.status;
            const new_identifier = await this.extractYouTubeIdentifier(response.uniform_resource_locator, type);
            return {
                status: status,
                identifier: new_identifier,
            };
        } catch (error) {
            console.error(`An error occurred while setting the YouTube identifier.\nError: ${error.message}`);
            throw new Error(error.message);
        }
    }

    /**
     * Setting the application's route based on the media identifier and platform.
     * 
     * This function calls an internal method to resolve the media identifier for the given platform and type.  It then updates the application state with the appropriate `view_route` depending on the response status.  If the status is 200, it redirects to a search-specific route; otherwise, it retains the current location.
     * @param {string} platform The media platform.
     * @param {string} type The media type.
     * @param {string} identifier The unique identifier for the media.
     * @returns {Promise<number>} The HTTP response status from the identifier resolution request.
     * @throws {Error} If an error occurs while resolving the media or updating the state.
     */
    async setRoute(platform, type, identifier) {
        try {
            const response = await this.setMediaYouTubeIdentifier(platform, type, identifier);
            return response.status;
        } catch (error) {
            console.error(`An error occurred while setting the route!\nError: ${error.message}`);
            throw new Error(error.message);
        }
    }

    /**
     * Searching for the Media content and redirecting the user to the searched content.
     * 
     * This function builds the search uniform resource locator based on the media type, logs the search event using a tracking service, sets the route for the selected platform and media type, and finally redirects the user to the view route.  If any step fails, the page is reloaded after the delay.
     * @param {string} platform The media platform.
     * @param {string} type The media type.
     * @param {string} identifier The unique identifier for the media.
     * @param {number} delay Delay in milliseconds before redirection.
     * @param {Tracker} tracker The tracker class which will track the user's activity on the application.
     * @returns {Promise<void>}
     */
    async searchMediaMetadata(platform, type, identifier, delay, tracker) {
        const search = (type == "Shorts") ? `https://www.youtube.com/shorts/${identifier}` : `https://www.youtube.com/watch?v=${identifier}`;
        const route = (type == "Shorts") ? `/Search/Shorts/${identifier}` : `/Search/${identifier}`;
        try {
            await tracker.sendEvent("search_submitted", {
                search_term: search,
            });
            const status = await this.setRoute(platform, type, identifier);
            console.info(`Route: GET /Media/Search?platform=${platform}&type=${type}&identifier=${identifier}\nStatus: ${status}\nEvent Listener: onSubmit\nReferrer: ${window.location.href}\nView Route: ${route}\nDelay: ${delay} ms`);
            setTimeout(() => this.redirect(route), delay);
        } catch (error) {
            console.error(`An error occurred while sending the event or setting the route!\nError: ${error.message}`);
            setTimeout(() => window.location.reload(), delay);
        }
    }

    /**
     * Redirecting the application to the route needed.
     * @param {string} route - The route of which the application will be redirected.
     * @returns {void}
     */
    redirect(route) {
        window.location.href = route;
    }

    /**
     * Validating whether the provided color scheme is allowed.
     * @param {string} color_scheme - The color scheme to validate.
     * @returns {Promise<void>} Resolves if the color scheme is valid.
     * @throws {Error} Throws an error with status 400 if the color scheme is invalid.
     */
    async isAllowedColorScheme(color_scheme) {
        const allowed_color_schemes = ["light", "dark"];
        if (allowed_color_schemes.includes(color_scheme)) {
            return;
        }
        throw new Error(`The color scheme is invalid.\nStatus: 400\nColor Scheme: ${color_scheme}`);
    }

    /**
     * Sending a PUT request to the server to update the user's session with the selected color scheme.  Validating the provided scheme before making the request.
     * @param {string} color_scheme - The desired color scheme to set.
     * @returns {Promise<number>}
     */
    async updateSession(color_scheme) {
        try {
            await this.isAllowedColorScheme(color_scheme);
            const response = await fetch("/Session/", {
                method: "PUT",
                body: JSON.stringify({
                    Client: {
                        color_scheme: color_scheme,
                    },
                }),
                headers: {
                    "Content-Type": "application/json",
                },
            });
            return response.status;
        } catch (error) {
            console.error(`The application has failed to update the session.\nError: ${error.message}`);
            throw new Error(error.message);
        }
    }

    /**
     * Handling the server response after attempting to update the session.
     * 
     * - Throws an error if the response status is not 202 or session data is invalid.
     * - On success:
     *   - Updates the local session data with a new timestamp and selected color scheme.
     *   - Applies new CSS custom properties to reflect the selected theme.
     *   - Updates the icon inside the triggering button to reflect the theme state.
     *   - Hides the loading icon once processing is complete.
     * @param {number} status - The HTTP response status code from the server.
     * @param {string} color_scheme - The color scheme to apply.
     * @param {HTMLButtonElement} button - The button that triggered the update, its icon and value are updated.
     * @param {HTMLDivElement} loading_icon - The loading indicator element to hide after completion.
     * @returns {Promise<void>} Resolves when the session data, visual theme, and UI state are successfully updated.
     * @throws {Error} If the status is not 202, session data is invalid, or the icon is missing from the button.
     */
    async manageResponse(status, color_scheme, button, loading_icon) {
        if (status !== 202) {
            throw new Error(`Status: ${status}\nError: There is an issue with the application's API and the session cannot be updated.`);
        }
        const session = JSON.parse(localStorage.getItem("session"));
        if (!session || !session.Client) {
            throw new Error("Invalid session structure in localStorage.");
        }
        session.Client.timestamp = Date.now() / 1000;
        session.Client.color_scheme = color_scheme;
        localStorage.setItem("session", JSON.stringify(session));
        const root = document.querySelector(":root");
        const icon = button.querySelector("i");
        const color_1 = (color_scheme == "light") ? "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))" : "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))";
        const color_2 = (color_scheme == "light") ? "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))" : "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))";
        const color_5 = (color_scheme == "light") ? "rgba(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)), calc(var(--percentage) / 2))" : "rgba(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)), calc(var(--percentage) / 2))";
        root.style.setProperty("--color1", color_1);
        root.style.setProperty("--color2", color_2);
        root.style.setProperty("--color5", color_5);
        button.value = color_scheme;
        if (!icon) {
            throw new Error("The icon is not present in the DOM.");
        }
        icon.className = (color_scheme == "light") ? "fa-solid fa-toggle-off" : "fa-solid fa-toggle-on";
        loading_icon.style.display = "none";
        console.info(`Route: PUT /Session/\nStatus: ${status}`);
    }

    /**
     * Updating the application's color scheme by sending a tracking event, updating the user session, and handling the server response.  If any step fails, the page reloads after the specified delay.
     * @param {string} color_scheme - The desired color scheme to apply.
     * @param {number} delay - The time to wait before reloading the page in milliseconds, if needed.
     * @param {HTMLButtonElement} button - The button that triggers the event.
     * @param {Tracker} tracker - The tracker class which will track the user's activity on the application.
     * @returns {Promise<void>}
     */
    async updateColorScheme(color_scheme, delay, button) {
        const loading_icon = document.querySelector("#loading");
        loading_icon.style.display = "flex";
        try {
            await tracker.sendEvent("color_scheme_updated", {
                color_scheme: color_scheme,
            });
            const status = await this.updateSession(color_scheme);
            await this.manageResponse(status, color_scheme, button, loading_icon);
        } catch (error) {
            console.error(`An error occurred while sending the event or setting the route!\nError: ${error.message}`);
            setTimeout(() => window.location.reload(), delay);
        }
    }

    /**
     * Handling the form submission event to extract metadata from a media URL.
     * 
     * This function prevents the default form submission behavior, displays a loading icon, parses the user-provided media URL to determine the platform, media type (video or shorts), and identifier, and then initiates metadata fetching via `searchMediaMetadata`.
     * @param {SubmitEvent} event - An event which takes place in the DOM.
     * @param {Tracker} tracker - The tracker class which will track the user's activity on the application.
     * @returns {void}
     */
    handleSubmit(event, tracker) {
        event.preventDefault();
        const loading_icon = document.querySelector("main #loading");
        loading_icon.style.display = "flex";
        try {
            const uniform_resource_locator = new URL(this.state.Media.search);
            const platform = this.getPlatform(uniform_resource_locator);
            const type = (uniform_resource_locator.pathname.includes("shorts")) ? "Shorts" : "Video";
            const identifier = this.getIdentifier(uniform_resource_locator, type);
            this.handleSubmitIdentifierExists(identifier);
            this.searchMediaMetadata(platform, type, identifier, 200, tracker);
        } catch (error) {
            console.error(`There is an error while processing the uniform resource locator for searching the media content.\nError: ${error.message}`);
        }
    }
}

export default Header;
