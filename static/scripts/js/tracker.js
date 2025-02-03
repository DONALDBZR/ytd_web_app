/**
 * The tracker class which will track the user's activity on
 * the application.
 */
class Tracker {
    /**
     * Initializing the class.
     */
    constructor() {
        this.endpoint = "/track";
        this.request_method = "POST";
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
     */
    trackPageView() {
        this.sendEvent("page_view", {
            referrer: document.referrer,
        });
    }
}