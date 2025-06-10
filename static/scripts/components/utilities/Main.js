/**
 * The utility class of the Main component.
 */
class Main {
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
            console.warn(`Component: Trend\nMessage: The data is not a string.\nData: ${encoded_string}`);
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
     * @returns {Promise<void>}
     * @throws {Error} If an issue occurs while sending the tracking event.
     */
    async handleClick(event) {
        const delay = 200;
        event.preventDefault();
        try {
            const uniform_resource_locator = (String(event.target.localName) == "a") ? String(event.target.href) : String(event.target.parentElement.href);
            await this.tracker.sendEvent("click", {
                uniform_resource_locator: uniform_resource_locator,
            });
            window.open(uniform_resource_locator, "_blank");
        } catch (error) {
            console.error(`An error occurred while sending the event or setting the route!\nError: ${error.message}`);
            setTimeout(() => window.location.reload(), delay);
        }
    };
}

export default Main;
