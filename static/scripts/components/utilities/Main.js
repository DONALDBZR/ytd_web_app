/**
 * The utility class of the Main component.
 */
class Main {
    /**
     * Retrieving the Trend data from the `localStorage`.
     * @returns {{trend: ?[{audio_file: ?string, author: string, author_channel: string, duration: string, identifier: string, published_at: string, thumbnail: string, title: string, uniform_resource_locator: string, video_file: ?string, views: number}], data_loaded: boolean}}
     */
    getTrends() {
        const trend = (localStorage.getItem("trend") != null) ? JSON.parse(localStorage.getItem("trend")).data : null;
        const data_loaded = (trend != null && window.Tracker);
        return {
            trend: trend,
            data_loaded: data_loaded,
        };
    }
}

export default Main;
