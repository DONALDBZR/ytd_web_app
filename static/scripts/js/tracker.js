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
        this.allowed_events = ["page_view", "search_submitted", "color_scheme_updated", "click"];
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
     * Sending a tracking event with additional metadata.
     *
     * This method validates the event name, sanitizes additional data, constructs an event object with timestamp and user details, and sends it to the tracking endpoint using a network request.
     * @param {string} event_name The name of the event to be tracked.
     * @param {Object} [additional_data={}] Optional additional data related to the event.
     * @returns {Promise<void>}
     * @throws {Error} If an issue occurs while sending the event.
     */
    async sendEvent(event_name, additional_data = {}) {
        if (!this.allowed_events.includes(event_name)) {
            console.error(`Invalid event name: ${event_name}`);
            return;
        }
        const sanitized_additional_data = Object.fromEntries(Object.entries(additional_data).map(([key, value]) => [this.sanitize(key), this.sanitize(value)]));
        const current_time = new Date();
        const event_data = {
            event_name: event_name,
            page_url: window.location.pathname,
            timestamp: `${current_time.getFullYear()}/${String(current_time.getMonth() + 1).padStart(2, "0")}/${String(current_time.getDate() + 1).padStart(2, "0")} ${String(current_time.getHours() + 1).padStart(2, "0")}:${String(current_time.getMinutes() + 1).padStart(2, "0")}:${String(current_time.getSeconds() + 1).padStart(2, "0")}`,
            user_agent: navigator.userAgent,
            screen_resolution: `${window.screen.width}x${window.screen.height}`,
            ...sanitized_additional_data,
        };
        try {
            const response = await fetch(this.endpoint, {
                method: this.request_method,
                headers: this.headers,
                body: JSON.stringify(event_data),
            });
            console.log(`Event Successfully Tracked!\nStatus: ${response.status}`);
        } catch (error) {
            console.error(`Error Tracking Event: ${error.message}`);
        }
    }

    /**
     * Sanitizing input data by removing unwanted characters while preserving safe URL components.
     *
     * This method ensures that:
     * - The input is a string before applying sanitization.
     * - Strings retain only alphanumeric characters, dashes (`-`), underscores (`_`), 
     *   colons (`:`), slashes (`/`), periods (`.`), ampersands (`&`), question marks (`?`), and equal signs (`=`).
     * - The string is truncated to a maximum length of 256 characters.
     * - The sanitized string is further processed using `encodeURI()` to ensure proper URL encoding.
     * @param {*} data The data to be sanitized. If not a string, it is returned as is.
     * @returns {*}
     */
    sanitize(data) {
        if (typeof data !== "string") {
            return data;
        }
        const sanitized_data = data.replace(/[^a-zA-Z0-9-_:/.&?=]/g, "").substring(0, 256);
        return encodeURI(sanitized_data);
    }
}

window.Tracker = new Tracker();