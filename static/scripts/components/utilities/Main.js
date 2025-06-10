import Application from "./Application";


/**
 * The utility class of the Main component.
 */
class Main extends Application {
    /**
     * Retrieving trending video data from `localStorage`.
     * @returns {{trend: ?[{audio_file: ?string, author: string, author_channel: string, duration: string, identifier: string, published_at: string, thumbnail: string, title: string, uniform_resource_locator: string, video_file: ?string, views: number}], data_loaded: boolean}} An object containing the parsed trend data and a boolean indicating whether the data is loaded.
     */
    getTrends() {
        const trend_data = localStorage.getItem("trend");
        const trend = (trend_data) ? JSON.parse(trend_data).data : null;
        const data_loaded = Boolean(trend && window.Tracker);
        return {
            trend: trend,
            data_loaded: data_loaded,
        };
    }

    /**
     * Handling mouse enter on a trend list item by controlling its animation state.
     * 
     * Pauses the animation if the viewport width is less than 640 pixels otherwise, resumes it.
     * @param {MouseEvent} event - The mouse enter event object.
     * @returns {void}
     */
    handleTrendListMouseEnter(event) {
        const trend_list = event.target.parentElement;
        trend_list.style.animationPlayState = window.innerWidth < 640 ? "paused" : "unset";
    }

    /**
     * Adding the mouse leave event handler for the trend list.
     * @param {MouseEvent} event - The mouse leave event object.
     * @returns {void}
     */
    handleTrendListMouseLeave(event) {
        const trend_list = event.target.parentElement;
        trend_list.style.animationPlayState = (window.innerWidth < 640) ? "running" : "unset";
    }

    /**
     * Decoding HTML entities in a given string.
     * 
     * This function takes a string that may contain HTML entities and returns the decoded version.  It uses a temporary `textarea` element to leverage the browser's parsing capabilities.
     * @param {string} encoded_string - The string potentially containing HTML entities.
     * @returns {string}
     */
    decodeHtmlEntities(encoded_string) {
        if (typeof encoded_string !== "string") {
            console.warn(`Route: ${window.location.pathname}\nMessage: The data is not a string.\nData: ${encoded_string}`);
            return encoded_string;
        }
        const text_area = document.createElement("textarea");
        text_area.innerHTML = encoded_string;
        return text_area.value;
    }

    /**
     * Handling click events, tracking the event and opening the link in a new tab.
     * 
     * This method prevents the default behavior of the event, extracts the URL from the clicked anchor (`<a>`) element or its parent, and sends a tracking event.  If the tracking event is successfully sent, the URL is opened in a new tab.  If an error occurs, it logs the error and refreshes the page after a delay.
     * @param {MouseEvent} event The click event object.
     * @param {Tracker} tracker - The tracker class which will track the user's activity on the application.
     * @returns {Promise<void>}
     * @throws {Error} If an issue occurs while sending the tracking event.
     */
    async handleClick(event, tracker) {
        const delay = 200;
        event.preventDefault();
        try {
            const uniform_resource_locator = (String(event.target.localName) == "a") ? String(event.target.href) : String(event.target.parentElement.href);
            await tracker.sendEvent("click", {
                uniform_resource_locator: uniform_resource_locator,
            });
            window.open(uniform_resource_locator, "_blank");
        } catch (error) {
            console.error(`An error occurred while sending the event or setting the route!\nError: ${error.message}`);
            setTimeout(() => window.location.reload(), delay);
        }
    };

    /**
     * Retrieving media metadata from `localStorage`.
     * 
     * This method reads the `media` key from localStorage, parses it as JSON, and extracts the media data.  It also checks whether the global `window.Tracker` exists to determine if the data is fully loaded.
     * @returns {{media: ?{audio: ?string, author: string, author_channel: string, duration: string, identifier: string, published_at: string, thumbnail: string, title: string, uniform_resource_locator: string, video: ?string, views: number}, data_loaded: boolean}} An object containing the media metadata and a flag indicating whether it is ready for use.
     */
    getMedia() {
        const data = localStorage.getItem("media");
        const media = (typeof data == "string") ? JSON.parse(data).data : null;
        const data_loaded = Boolean(media && window.Tracker);
        return {
            media: media,
            data_loaded: data_loaded,
        };
    }

    /**
     * Validating the presence of a media identifier extracted from a URL.
     * 
     * This function checks if the given identifier exists.  If it does not, it throws an error indicating that the media URL is invalid due to a missing identifier.
     * @param {string|null|undefined} identifier The media identifier extracted from the URL.
     * @returns {void}
     * @throws {Error} If the identifier is null, undefined, or an empty string.
     */
    retrieveMediaIdentifierExists(identifier) {
        if (identifier) {
            return;
        }
        throw new Error("The uniform resource locator is invalid as the identifier cannot be extracted.");
    }

    /**
     * Handling the media retrieval process from a given YouTube uniform resource locator.
     * 
     * This method prevents the default form or link behavior, displays a loading indicator, parses the YouTube uniform resource locator, determines the media type, extracts the unique identifier, and initiates the media download process.  If an error occurs during uniform resource locator processing, it logs the error to the console.
     * @param {MouseEvent} event - The mouse event triggered by the user interaction.
     * @returns {void}
     */
    retrieveMedia(event) {
        event.preventDefault();
        const loading_icon = document.querySelector("#loading");
        loading_icon.style.display = "flex";
        try {
            const uniform_resource_locator = new URL(this.state.Media.YouTube.uniform_resource_locator);
            const platform = this.getPlatform(uniform_resource_locator);
            const type = (uniform_resource_locator.pathname.includes("shorts")) ? "Shorts" : "Video";
            const identifier = this.getIdentifier(uniform_resource_locator, type);
            this.retrieveMediaIdentifierExists(identifier);
            this.downloadMedia(platform, type, identifier, 200);
        } catch (error) {
            console.error(`There is an error while processing the uniform resource locator for downloading the media content.\nError: ${error.message}`);
            setTimeout(() => window.location.reload(), 200);
        }
    }

    /**
     * Sending a tracking event and initiates the media download process.
     * 
     * Based on the provided media type and identifier, this method constructs the appropriate download route, logs a tracking event, and performs the download process.  It manages the server response and handles any errors by logging them and optionally redirecting the user after a delay.
     * @param {string} platform - The supported platform.
     * @param {string} type - The type of media.
     * @param {string} identifier - The unique identifier of the media.
     * @param {number} delay - The delay in milliseconds before processing the response or redirection.
     * @param {Tracker} tracker - The tracker class which will track the user's activity on the application.
     * @returns {Promise<void>}
     */
    async downloadMedia(platform, type, identifier, delay, tracker) {
        const uniform_resource_locator = (type == "Shorts") ? `/Download/YouTube/Shorts/${identifier}` : `/Download/YouTube/${identifier}`;
        try {
            await tracker.sendEvent("click", {
                uniform_resource_locator: uniform_resource_locator,
            });
            const response = await this.postMediaDownload(platform, type, identifier);
            await this.manageResponse(response, delay);
        } catch (error) {
            console.error(`An error occurred while sending the event or setting the route!\nError: ${error.message}`);
            this.redirect(delay, window.location.href);
        }
    }

    /**
     * Handling application flow based on the server's response.
     * 
     * Clears local storage if applicable, then redirects the user after a specified delay.  If the response status is `201`, the user is redirected to the provided download uniform resource locator.  For any other status, the user is redirected to the current page. If an error occurs during processing, it logs the error and rethrows it.
     * @param {{status: number, uniform_resource_locator: string}} response - The response object from the backend, including HTTP status and redirect uniform resource locator.
     * @param {number} delay - The delay (in milliseconds) before redirecting the user.
     * @returns {void}
     * @throws {Error} Throws an error if the application fails to process the response.
     */
    manageResponse(response, delay) {
        try {
            this.clearLocalStorage(response.status);
            const uniform_resource_locator = (response.status == 201) ? response.uniform_resource_locator : window.location.href;
            this.redirect(delay, uniform_resource_locator);
        } catch (error) {
            console.error(`There is an error while processing the response.\nError: ${error.message}`);
            throw new Error(error.message);
        }
    }

    /**
     * Sending a POST request to the server to initiate the download of a media file.
     * 
     * Constructs the YouTube media uniform resource locator based on the media type and sends it to the backend endpoint with metadata.  Returns a simplified object containing the HTTP status code and the uniform resource locator to which the user can be redirected to access the media.
     * @param {string} platform - The supported platform.
     * @param {string} type - The type of media.
     * @param {string} identifier - The unique media identifier.
     * @returns {Promise<{status: number, uniform_resource_locator: string}>} A promise that resolves with the server response status and download route.
     * @throws {Error} Throws an error if the request fails or JSON parsing fails.
     */
    async postMediaDownload(platform, type, identifier) {
        const query = "/Media/Download";
        const youtube_uniform_resource_locator = (type == "Shorts") ? `https://www.youtube.com/shorts/${identifier}`: `https://www.youtube.com/watch?v=${identifier}`;
        try {
            const response = await fetch(query, {
                method: "POST",
                body: JSON.stringify({
                    Media: {
                        uniform_resource_locator: youtube_uniform_resource_locator,
                        platform: platform,
                        type: type,
                        identifier: identifier,
                    },
                }),
                headers: {
                    "Content-Type": "application/json",
                },
            });
            const data = await response.json();
            const uniform_resource_locator = (response.status == 201) ? ((type == "Shorts") ? `/Download/YouTube/Shorts/${data.identifier.replaceAll("shorts/", "")}` : `/Download/YouTube/${data.identifier}`) : "/";
            return {
                status: response.status,
                uniform_resource_locator: uniform_resource_locator,
            };
        } catch (error) {
            console.error(`There is an issue while downloading the file.\nError: ${error.message}`);
            throw new Error(error.message);
        }
    }
}

export default Main;
