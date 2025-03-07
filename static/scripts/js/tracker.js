/**
 * The tracker class which will track the user's activity on
 * the application.
 */
class Tracker {
    /**
     * Initializing the class.
     */
    constructor() {
        this.endpoint = "/Track/";
        this.request_method = "POST";
        this.headers = {
            "Content-Type": "application/json",
        };
        this.init();
    }

    /**
     * Initializing the tracker by firstly tracking the page view.
     * @returns {void}
     */
    init() {
        window.addEventListener("load", () => this.trackPageView());
        console.log("Tracker initialized");
    }

    /**
     * Tracking the page view event.
     * @returns {Promise<void>}
     */
    async trackPageView() {
        const loading_time = await this.getLoadingTime();
        this.sendEvent("page_view", {
            referrer: document.referrer,
            loading_time: loading_time,
        });
    }

    /**
     * Retrieving the loading time of a page.
     * @returns {Promise<number | null>}
     */
    async getLoadingTime() {
        return new Promise((resolve) => {
            if (!("performance" in window && "PerformanceNavigationTiming" in window)) {
                resolve(null);
                return;
            }
            const navigation_entries = performance.getEntriesByType("navigation");
            if (navigation_entries.length === 0) {
                resolve(null);
                return;
            }
            const navigation_timing = navigation_entries[0];
            if (document.readyState === "complete") {
                const loading_time = navigation_timing.domComplete - navigation_timing.startTime;
                resolve(loading_time);
                return;
            }
            window.addEventListener("load", () => this.resolveLoadingTime.bind(this, resolve));
        });
    }

    /**
     * Retrieving the loading time after the DOM has been loaded.
     * @param {Function} resolve The resolve function of the promise.
     * @returns {void}
     */
    resolveLoadingTime(resolve) {
        const navigation_entries = performance.getEntriesByType("navigation");
        if (navigation_entries.length > 0) {
            const navigation_timing = navigation_entries[0];
            const loading_time = navigation_timing.domComplete - navigation_timing.startTime;
            resolve(loading_time);
            return;
        }
        if ("performance" in window && performance.timing) {
            const loading_time_fallback = performance.timing.domComplete - performance.timing.startTime;
            resolve(loading_time_fallback);
            return;
        }
        resolve(null);
    }

    /**
     * Sending the event to the API for further processing.
     * @param {string} event_name The name of the event. 
     * @param {*} additional_data Additional data to be sent with the event.
     * @returns {Promise<void>}
     */
    async sendEvent(event_name, additional_data = {}) {
        const current_time = new Date();
        const current_month = (current_time.getMonth() + 1 < 10) ? `0${current_time.getMonth() + 1}` : current_time.getMonth() + 1;
        const current_date = (current_time.getDate() < 10) ? `0${current_time.getDate()}` : current_time.getDate();
        const current_hour = (current_time.getHours() < 10) ? `0${current_time.getHours()}` : current_time.getHours();
        const current_minute = (current_time.getMinutes() < 10) ? `0${current_time.getMinutes()}` : current_time.getMinutes();
        const current_second = (current_time.getSeconds() < 10) ? `0${current_time.getSeconds()}` : current_time.getSeconds();
        const event_data = {
            event_name: event_name,
            page_url: window.location.pathname,
            timestamp: `${current_time.getFullYear()}/${current_month}/${current_date} ${current_hour}:${current_minute}:${current_second}`,
            user_agent: navigator.userAgent,
            screen_resolution: `${window.screen.width}x${window.screen.height}`,
            ...additional_data
        };
        try {
            const response = await fetch(this.endpoint, {
                method: this.request_method,
                headers: this.headers,
                body: JSON.stringify(event_data),
            });
            console.log(`Event Successfully Tracked!\nStatus: ${response.status}`);
        } catch (error) {
            console.error(`Error Tracking Event: ${error}`);
        }
    }
}

window.Tracker = new Tracker();