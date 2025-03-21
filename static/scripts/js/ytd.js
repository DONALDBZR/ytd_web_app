/**
 * The main script that will initialize the application as
 * needed
 */
class YTD {
    /**
     * Setting the data needed as well as initalizing the
     * application
     * @returns {YTD}
     */
    constructor() {
        /**
         * The request URI of the page needed
         * @type {string}
         */
        this.__requestUniformRequestInformation;
        /**
         * The ID of the body
         * @type {string}
         */
        this.__bodyId;
        /**
         * Stylesheets of the application
         * @type {string[]}
         */
        this._stylesheets = [
            "/static/stylesheets/ytd.css",
            "/static/stylesheets/desktop.css",
            "/static/stylesheets/mobile.css",
            "/static/stylesheets/tablet.css",
        ];
        /**
         * Relationship of the object
         * @type {string}
         */
        this.__relationship;
        /**
         * MIME Type of the object
         * @type {string}
         */
        this.__mimeType;
        /**
         * Media queries for the stylesheets
         * @type {string[]}
         */
        this._mediaQueries = [
            "screen and (min-width: 1024px)",
            "screen and (min-width: 640px) and (max-width: 1023px)",
            "screen and (max-width: 639px)",
        ];
        /**
         * The body of the page
         * @type {HTMLBodyElement}
         */
        this.__body;
        /**
         * Class name of the body
         * @type {string}
         */
        this.__bodyClassName;
        /**
         * Contains the title for a document.  This element inherits
         * all of the properties and methods of the HTMLElement
         * interface.
         * @type {HTMLTitleElement}
         */
        this.__title;
        /**
         * Contains descriptive metadata about a document.  It inherits
         * all of the properties and methods described in the
         * HTMLElement interface.
         * @type {HTMLMetaElement|null}
         */
        this.__meta;
        /**
         * Contains the descriptive information, or metadata, for a
         * document. This object inherits all of the properties and
         * methods described in the HTMLElement interface.
         * @type {HTMLHeadElement}
         */
        this.__head;
        /**
         * The origin of the server connection.
         * @type {string}
         */
        this.__origin;
        /**
         * The identifiers of the stylsheets.
         * @type {string[]}
         */
        this._stylesheetIdentifiers = ["ytd-css", "desktop-css", "mobile-css", "tablet-css"];
        this.init();
    }

    /**
     * @returns {string}
     */
    getRequestURI() {
        return this.__requestUniformRequestInformation;
    }

    /**
     * @param {string} request_uri
     * @returns {void}
     */
    setRequestURI(request_uri) {
        this.__requestUniformRequestInformation = request_uri;
    }

    /**
     * @returns {string}
     */
    getBodyId() {
        return this.__bodyId;
    }

    /**
     * @param {string} body_id
     * @returns {void}
     */
    setBodyId(body_id) {
        this.__bodyId = body_id;
    }

    /**
     * @returns {string}
     */
    getRelationship() {
        return this.__relationship;
    }

    /**
     * @param {string} relationship
     * @returns {void}
     */
    setRelationship(relationship) {
        this.__relationship = relationship;
    }

    /**
     * @returns {string}
     */
    getMimeType() {
        return this.__mimeType;
    }

    /**
     * @param {string} mime_type
     * @returns {void}
     */
    setMimeType(mime_type) {
        this.__mimeType = mime_type;
    }
    
    /**
     * @returns {HTMLBodyElement}
     */
    getBody() {
        return this.__body;
    }

    /**
     * @param {HTMLBodyElement} body
     * @returns {void}
     */
    setBody(body) {
        this.__body = body;
    }

    /**
     * @returns {string}
     */
    getBodyClassName() {
        return this.__bodyClassName;
    }

    /**
     * @param {string} body_class_name
     * @returns {void}
     */
    setBodyClassName(body_class_name) {
        this.__bodyClassName = body_class_name;
    }

    /**
     * @returns {HTMLTitleElement}
     */
    getTitle() {
        return this.__title;
    }

    /**
     * @param {HTMLTitleElement} title
     * @returns {void}
     */
    setTitle(title) {
        this.__title = title;
    }

    /**
     * @returns {HTMLMetaElement|null}
     */
    getMeta() {
        return this.__meta;
    }

    /**
     * @param {HTMLMetaElement|null} meta
     * @returns {void}
     */
    setMeta(meta) {
        this.__meta = meta;
    }

    /**
     * @returns {HTMLHeadElement}
     */
    getHead() {
        return this.__head;
    }

    /**
     * @param {HTMLHeadElement} head
     * @returns {void}
     */
    setHead(head) {
        this.__head = head;
    }

    /**
     * @returns {string}
     */
    getOrigin() {
        return this.__origin;
    }

    /**
     * @param {number} port
     * @returns {void}
     */
    setOrigin(port) {
        this.__origin = (port == 591) ? "https://omnitechbros.ddns.net:591" : "https://omnitechbros.ddns.net:5000";
    }

    /**
     * Initializing the application
     * @returns {void}
     */
    init() {
        this.setOrigin(Number(window.location.port));
        this.setRequestURI(window.location.pathname);
        this.setBody(document.body);
        this.setHead(document.head);
        if (this.getRequestURI() == "/") {
            this.setBodyId("Homepage");
        } else {
            this.setBodyId(this.getRequestURI().replaceAll("/", ""));
        }
        this.getBody().id = this.getBodyId();
        this.loadData();
    }

    /**
     * Adding the stylesheets needed for the application.
     * @returns {void}
     */
    addStylesheets() {
        this._stylesheetIdentifiers.forEach((identifier) => this.addStylesheet(identifier));
    }

    /**
     * Adding the stylesheet based on its identifier.
     * @param {string} identifier The identifier of the stylesheet.
     * @returns {void}
     */
    addStylesheet(identifier) {
        let link = document.getElementById(identifier);
        if (link) {
            link.rel = "stylesheet";
        }
    }

    /**
     * Defining the title of the page for the application.
     * @returns {void}
     */
    addTitle() {
        let media;
        let local_storage_data;
        this.setTitle(document.createElement("title"));
        if (this.getRequestURI() == "" || this.getRequestURI() == "/") {
            this.getTitle().text = "Extractio";
        } else if (this.getRequestURI() == "/Search/") {
            this.getTitle().text = "Extractio: Search";
        } else if (this.getRequestURI().includes("/Search/") && this.getRequestURI() != "/Search/") {
            local_storage_data = localStorage.getItem("media");
            media = (typeof local_storage_data == "string") ? JSON.parse(localStorage.getItem("media")).data : null;
            this.getTitle().text = (media) ? `Extractio Data: ${media.title}` : "Extractio: Search";
        } else if (this.getRequestURI().includes("/Download/")) {
            local_storage_data = localStorage.getItem("media");
            media = (typeof local_storage_data == "string") ? JSON.parse(localStorage.getItem("media")).data : null;
            this.getTitle().text = (media) ? `Extractio: ${media.title}` : "Extractio";
        }
        this.getHead().appendChild(this.getTitle());
    }

    /**
     * Defining the description of the page.
     * @returns {void}
     */
    addDescription() {
        let local_storage_data;
        let media;
        this.setMeta(document.createElement("meta"));
        this.getMeta().name = "description";
        if (this.getRequestURI() == "" || this.getRequestURI() == "/") {
            this.getMeta().content = "Extractio extracts content from various platforms for various needs.";
        } else if (this.getRequestURI() == "/Search/") {
            this.getMeta().content = "The content needed can be searched, here.";
        } else if (this.getRequestURI().includes("/Search/") && this.getRequestURI() != "/Search/") {
            local_storage_data = localStorage.getItem("media");
            media = (typeof local_storage_data == "string") ? JSON.parse(localStorage.getItem("media")).data : null;
            const platform = (media) ? new URL(media.uniform_resource_locator).hostname.replace("www.", "").replace(".com", "") : "";
            this.getMeta().content = (media) ? `Metadata for the content from ${media.author} on ${platform} entitled ${media.title}` : "The content needed can be searched, here.";
        } else if (this.getRequestURI().includes("/Download/")) {
            local_storage_data = localStorage.getItem("media");
            media = (typeof local_storage_data == "string") ? JSON.parse(localStorage.getItem("media")).data : null;
            const platform = (media) ? new URL(media.uniform_resource_locator).hostname.replace("www.", "").replace(".com", "") : "";
            this.getMeta().content = (media) ? `Content from ${media.author} on ${platform} entitled ${media.title}` : "The content needed can be searched, here.";
        }
        this.getHead().appendChild(this.getMeta());
        setTimeout(() => this.configureRobot(), 2000);
    }

    /**
     * Configuring the pages for which the web crawlers can index
     * on the application.
     * @returns {void}
     */
    configureRobot() {
        this.setMeta(document.createElement("meta"));
        this.getMeta().name = "robots";
        this.getMeta().content = "index, follow";
        this.getHead().appendChild(this.getMeta());
    }

    /**
     * Optimizing the web application for search engines
     * @returns {void}
     */
    optimize() {
        this.addTitle();
        this.addDescription();
        this.style();
    }

    /**
     * Retrieving the media query needed for the stylesheets.
     * @param {string} href The hyperlink of the stylesheet.
     * @returns {string}
     */
    getMediaQuery(href) {
        if (href.includes("desktop")) {
            return this._mediaQueries[0];
        } else if (href.includes("mobile")) {
            return this._mediaQueries[2];
        } else if (href.includes("tablet")) {
            return this._mediaQueries[1];
        } else {
            return "";
        }
    }

    /**
     * Styling the application
     * @returns {void}
     */
    style() {
        this.setRelationship("stylesheet");
        this.setMimeType("text/css");
        this.resizeApplication();
    }

    /**
     * Resizing the application which depends on the client's size
     * @returns {void}
     */
    resizeApplication() {
        const root = document.querySelector(":root");
        const height = `${root.clientHeight}px`;
        const width = `${root.clientWidth}px`;
        root.style.setProperty("--height", height);
        root.style.setProperty("--width", width);
    }

    /**
     * Loading the data needed for the API.
     * @returns {void}
     */
    loadData() {
        this.setSession();
        if (window.location.pathname.includes("Search")) {
            setTimeout(() => this.loadDataSearchPage(), 100);
        } else if (window.location.pathname.includes("Download/YouTube")) {
            setTimeout(() => this.loadDataDownloadPage(), 100);
        } else {
            setTimeout(() => this.loadDataHomepage(), 100);
        }
        setTimeout(() => this.optimize(), 1000);
    }

    /**
     * Loading the data specifically for the Download page.
     * @returns {void}
     */
    loadDataDownloadPage() {
        this.setMedia();
        this.setRelatedContents();
    }

    /**
     * Loading the data specifically for the Search page.
     * @returns {void}
     */
    loadDataSearchPage() {
        this.setMedia();
        this.setRelatedContents();
    }

    /**
     * Retrieving the identifier needed for the API and the caching
     * mechanicsm to operate smoothly.
     * @returns {string}
     */
    _getRelatedContentsIdentifier() {
        if (this.getRequestURI().includes("Search")) {
            return this.getRequestURI().replace("/Search/", "");
        } else if (this.getRequestURI().includes("Download/YouTube")) {
            return this.getRequestURI().replace("/Download/YouTube/", "");
        }
    }

    /**
     * Setting the related contents of the related media content.
     * @returns {void}
     */
    setRelatedContents() {
        const identifier = this._getRelatedContentsIdentifier();
        const data_object = "related_content";
        const related_content = JSON.parse(localStorage.getItem(data_object));
        const route = `/Media/RelatedContents/${identifier}`;
        const request_method = "GET";
        let status = 0;
        const current_time = Math.floor(Date.now() / 1000);
        if (!related_content) {
            this.getRelatedContents(route, request_method, data_object, identifier)
            .then((status) => console.info(`Route: ${request_method} ${route}\nStatus: ${status}`));
            return;
        }
        status = ((current_time < related_content.timestamp + 3600) && (related_content.identifier == identifier)) ? 304 : 204;
        if ((current_time < related_content.timestamp + 3600) && (related_content.identifier == identifier)) {
            related_content.timestamp = current_time + 3600;
            related_content.data = this.sanitizeRelatedContentList(related_content.data);
            localStorage.setItem(data_object, JSON.stringify(related_content));
            console.info(`Route: ${request_method} ${route}\nStatus: ${status}`);
            return;
        }
        localStorage.removeItem(data_object);
        console.info(`Route: ${request_method} ${route}\nStatus: ${status}`);
        this.getRelatedContents(route, request_method, data_object, identifier)
        .then((status) => console.info(`Route: ${request_method} ${route}\nStatus: ${status}`));
    }

    /**
     * Sanitizing the data of the related contents.
     * @param {{duration: string, channel: string, title: string, uniform_resource_locator: string, author_channel: string, thumbnail: string}[]} related_contents The related content list to sanitize.
     * @returns {{duration: string, channel: string, title: string, uniform_resource_locator: string, author_channel: string, thumbnail: string}[]}
     */
    sanitizeRelatedContentList(related_contents) {
        const sanitized_related_contents = [];
        for (let index = 0; index < related_contents.length; index++) {
            const related_content = related_contents[index];
            sanitized_related_contents.push({
                duration: this.escapeHtml(related_content.duration),
                channel: this.escapeHtml(related_content.channel),
                title: this.escapeHtml(related_content.title),
                uniform_resource_locator: this.escapeHtml(related_content.uniform_resource_locator),
                author_channel: this.escapeHtml(related_content.author_channel),
                thumbnail: this.escapeHtml(related_content.thumbnail),
            });
        }
        return sanitized_related_contents;
    }

    /**
     * Retrieving the route needed for the Media API route.
     * @returns {string}
     */
    _getMediaApiRoute() {
        if (this.getRequestURI().includes("Search")) {
            return `/Media/${this.getRequestURI().replace("/Search/", "")}`;
        } else if (this.getRequestURI().includes("Download/YouTube")) {
            return `/Media/${this.getRequestURI().replace("/Download/YouTube/", "")}`;
        }
    }

    /**
     * Setting the media metadata of the content.
     * @returns {void}
     */
    setMedia() {
        const data_object = "media";
        const media = JSON.parse(localStorage.getItem(data_object));
        const route = this._getMediaApiRoute();
        const request_method = "GET";
        let status = 0;
        const current_time = Math.floor(Date.now() / 1000);
        if (!media) {
            this.getMedia(route, request_method, data_object)
            .then((status) => console.info(`Route: ${request_method} ${route}\nStatus: ${status}`));
            return;
        }
        status = ((current_time < media.timestamp + 3600) && (media.data.identifier == this.getRequestURI().replace("/Search/", ""))) ? 304 : 204;
        if ((current_time < media.timestamp + 3600) && (media.data.identifier == this.getRequestURI().replace("/Search/", ""))) {
            media.timestamp = current_time + 3600;
            media.data.uniform_resource_locator = this.escapeHtml(media.data.uniform_resource_locator);
            media.data.author = this.escapeHtml(media.data.author);
            media.data.title = this.escapeHtml(media.data.title);
            media.data.identifier = this.escapeHtml(media.data.identifier);
            media.data.author_channel = this.escapeHtml(media.data.author_channel);
            media.data.published_at = this.escapeHtml(media.data.published_at);
            media.data.thumbnail = this.escapeHtml(media.data.thumbnail);
            media.data.duration = this.escapeHtml(media.data.duration);
            media.data.audio_file = (media.data.audio_file != null) ? this.escapeHtml(media.data.audio_file) : null;
            media.data.video_file = (media.data.video_file != null) ? this.escapeHtml(media.data.video_file) : null;
            localStorage.setItem(data_object, JSON.stringify(media));
            console.info(`Route: ${request_method} ${route}\nStatus: ${status}`);
            return;
        }
        localStorage.removeItem(data_object);
        console.info(`Route: ${request_method} ${route}\nStatus: ${status}`);
        this.getMedia(route, request_method, data_object)
        .then((status) => console.info(`Route: ${request_method} ${route}\nStatus: ${status}`));
    }

    /**
     * Loading the data specifically for the homepage.
     * @returns {void}
     */
    loadDataHomepage() {
        this.setTrend();
    }

    /**
     * Retrieving the metadata of the media content.
     * @param {string} route The route to the API endpoint.
     * @param {string} request_method The request method
     * @param {string} data_object The name of the data object in the Local Storage
     * @param {string} identifier The identifier of the related media content.
     * @returns {Promise<number>}
     */
    async getRelatedContents(route, request_method, data_object, identifier) {
        const response = await fetch(route, {
            method: request_method,
        });
        const current_time = Math.floor(Date.now() / 1000);
        const data = await response.json();
        const related_content = {
            timestamp: current_time,
            identifier: identifier,
            data: data,
        };
        localStorage.setItem(data_object, JSON.stringify(related_content));
        return response.status;
    }

    /**
     * Retrieving the metadata of the media content.
     * @param {string} route The route to the API endpoint.
     * @param {string} request_method The request method
     * @param {string} data_object The name of the data object in the Local Storage
     * @returns {Promise<number>}
     */
    async getMedia(route, request_method, data_object) {
        const response = await fetch(route, {
            method: request_method,
        });
        const current_time = Math.floor(Date.now() / 1000);
        const data = await response.json();
        const media = {
            timestamp: current_time,
            data: data,
        };
        localStorage.setItem(data_object, JSON.stringify(media));
        return response.status;
    }

    /**
     * Retrieving the session of the user.
     * @param {string} route The route to the API endpoint.
     * @param {string} request_method The request method
     * @param {string} data_object The name of the data object in the Local Storage
     * @returns {Promise<number>}
     */
    async getSession(route, request_method, data_object) {
        const response = await fetch(route, {
            method: request_method,
        });
        const data = await response.json();
        localStorage.setItem(data_object, JSON.stringify(data));
        return response.status;
    }

    /**
     * Retrieving the weekly trend.
     * @param {string} route The route to the API endpoint.
     * @param {string} request_method The request method
     * @param {string} data_object The name of the data object in the Local Storage
     * @returns {Promise<number>}
     */
    async getTrend(route, request_method, data_object) {
        const response = await fetch(route, {
            method: request_method,
        });
        const current_time = Math.floor(Date.now() / 1000);
        const data = await response.json();
        const trend = {
            timestamp: current_time,
            data: data,
        };
        localStorage.setItem(data_object, JSON.stringify(trend));
        return response.status;
    }

    /**
     * Setting the trend of the week.
     * @returns {void}
     */
    setTrend() {
        const data_object = "trend";
        const trend = JSON.parse(localStorage.getItem(data_object));
        const route = "/Trend/";
        const request_method = "GET";
        let status = 0;
        const current_time = Math.floor(Date.now() / 1000);
        if (!trend) {
            this.getTrend(route, request_method, data_object)
            .then((status) => console.info(`Route: ${request_method} ${route}\nStatus: ${status}`));
            return;
        }
        status = (current_time < trend.timestamp + 86400) ? 304 : 204;
        if (current_time < trend.timestamp + 86400) {
            trend.timestamp = current_time + 86400;
            trend.data = this.sanitizeTrendList(trend.data);
            localStorage.setItem(data_object, JSON.stringify(trend));
            console.info(`Route: ${request_method} ${route}\nStatus: ${status}`);
            return;
        }
        localStorage.removeItem(data_object);
        console.info(`Route: ${request_method} ${route}\nStatus: ${status}`);
        this.getTrend(route, request_method, data_object)
        .then((status) => console.info(`Route: ${request_method} ${route}\nStatus: ${status}`));
    }

    /**
     * Sanitizing the trend list.
     * @param {{audio_file: string|null, author: string, author_channel: string, duration: string, identifier: string, published_at: string, thumbnail: string, title: string, uniform_resource_locator: string, video_file: string|null, views: number}[]} trend_list The trend list to sanitize.
     * @returns {{audio_file: string|null, author: string, author_channel: string, duration: string, identifier: string, published_at: string, thumbnail: string, title: string, uniform_resource_locator: string, video_file: string|null, views: number}[]}
     */
    sanitizeTrendList(trend_list) {
        const sanitized_trend_list = [];
        for (let index = 0; index < trend_list.length; index++) {
            const trend = trend_list[index];
            sanitized_trend_list.push({
                audio_file: (trend.audio_file != null) ? this.escapeHtml(trend.audio_file) : null,
                author: this.escapeHtml(trend.author),
                author_channel: this.escapeHtml(trend.author_channel),
                duration: this.escapeHtml(trend.duration),
                identifier: this.escapeHtml(trend.identifier),
                published_at: this.escapeHtml(trend.published_at),
                thumbnail: this.escapeHtml(trend.thumbnail),
                title: this.escapeHtml(trend.title),
                uniform_resource_locator: this.escapeHtml(trend.uniform_resource_locator),
                video_file: (trend.video_file != null) ? this.escapeHtml(trend.video_file) : null,
                views: trend.views,
            });
        }
        return sanitized_trend_list;
    }

    /**
     * Setting the session of the user.
     * @returns {void}
     */
    setSession() {
        const data_object = "session";
        const session = JSON.parse(localStorage.getItem(data_object));
        const route = "/Session/";
        const request_method = "GET";
        let status = 0;
        const current_time = Math.floor(Date.now() / 1000);
        if (!session) {
            this.getSession(route, request_method, data_object)
            .then((status) => console.info(`Route: ${request_method} ${route}\nStatus: ${status}`));
            return;
        }
        status = (current_time < session.Client.timestamp + 3600) ? 304 : 204;
        if (current_time < session.Client.timestamp + 3600) {
            session.Client.timestamp = current_time + 3600;
            session.Client.color_scheme = this.escapeHtml(session.Client.color_scheme);
            localStorage.setItem(data_object, JSON.stringify(session));
            console.info(`Route: ${request_method} ${route}\nStatus: ${status}`);
        }
        localStorage.removeItem(data_object);
        console.info(`Route: ${request_method} ${route}\nStatus: ${status}`);
        this.getSession(route, request_method, data_object)
        .then((status) => console.info(`Route: ${request_method} ${route}\nStatus: ${status}`));
    }

    /**
     * Sanitizing the HTML content.
     * @param {string} unsafe The unsafe HTML content.
     * @returns {string}
     */
    escapeHtml(unsafe) {
        if (unsafe === null || unsafe === undefined) {
            return "";
        }
        const lookup = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;",
        };
        return String(unsafe).replace(/[&<>"']/g, (character) => lookup[character]);
    }
}

/**
 * Loading the service worker.
 * @returns {void}
 */
const load = () => {
    navigator.serviceWorker.register('/static/scripts/js/service-worker.js')
    .then((registration) => console.log('ServiceWorker registration successful with scope: ', registration.scope))
    .catch((error) => console.error('ServiceWorker registration failed: ', error));
};

const application = new YTD();
window.addEventListener("resize", () => application.resizeApplication(), true);
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => load());
}
document.addEventListener("DOMContentLoaded", () => application.addStylesheets(), true);
