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
}

export default Main;
