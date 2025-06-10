/**
 * The main script that will initialize the application as needed.
 */
class YTD {
    /**
     * Setting the data needed as well as initalizing the application.
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
         * @type {HTMLMetaElement}
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
         * The identifiers of the stylesheets.
         * @type {[string]}
         */
        this._stylesheetIdentifiers = ["ytd-css", "desktop-css", "tablet-css", "mobile-css"];
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
     * @returns {HTMLMetaElement}
     */
    getMeta() {
        return this.__meta;
    }

    /**
     * @param {HTMLMetaElement} meta
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
     * Defining the title of the page for the application.
     * @returns {void}
     */
    addTitle() {
        this.setTitle(document.createElement("title"));
        const is_homepage = (this.getRequestURI() == "" || this.getRequestURI() == "/");
        if (is_homepage) {
            this.getTitle().text = "Extractio";
            this.getHead().appendChild(this.getTitle());
            return;
        }
        const data = localStorage.getItem("media");
        if (!data) {
            setTimeout(() => this.addTitle(), 1000);
        }
        this.setTitle(document.createElement("title"));
        const media = JSON.parse(data).data;
        if (this.getRequestURI().includes("/Search/")) {
            this.getTitle().text = `Extractio Data: ${media.title}`;
            this.getHead().appendChild(this.getTitle());
            return;
        }
        if (this.getRequestURI().includes("/Download/")) {
            this.getTitle().text = `Extractio: ${media.title}`;
            this.getHead().appendChild(this.getTitle());
            return;
        }
    }

    /**
     * Defining the description of the page.
     * @returns {void}
     */
    addDescription() {
        const data = localStorage.getItem("media");
        const is_homepage = (this.getRequestURI() == "" || this.getRequestURI() == "/");
        if (!data && !is_homepage) {
            setTimeout(() => this.addDescription(), 1000);
        }
        this.setMeta(document.createElement("meta"));
        this.getMeta().name = "description";
        if (is_homepage) {
            this.getMeta().content = "Extractio extracts content from various platforms for various needs.";
            this.getHead().appendChild(this.getMeta());
            setTimeout(() => this.configureRobot(), 2000);
            return;
        }
        const media = JSON.parse(data).data;
        const platform = new URL(media.uniform_resource_locator).hostname.replace("www.", "").replace(".com", "");
        if (this.getRequestURI().includes("/Search/")) {
            this.getMeta().content = `Metadata for the content from ${media.author} on ${platform} entitled ${media.title}`;
            this.getHead().appendChild(this.getMeta());
            setTimeout(() => this.configureRobot(), 2000);
            return;
        }
        if (this.getRequestURI().includes("/Download/")) {
            this.getMeta().content = `Content from ${media.author} on ${platform} entitled ${media.title}`;
            this.getHead().appendChild(this.getMeta());
            setTimeout(() => this.configureRobot(), 2000);
            return;
        }
    }

    /**
     * Configuring the pages for which the web crawlers can index on the application.
     * @returns {void}
     */
    configureRobot() {
        this.setMeta(document.createElement("meta"));
        this.getMeta().name = "robots";
        this.getMeta().content = (this.getRequestURI().includes("/Download/")) ? "index" : "index, follow";
        this.getHead().appendChild(this.getMeta());
    }

    /**
     * Optimizing the web application for search engines
     * @returns {void}
     */
    optimize() {
        this.addTitle();
        this.addDescription();
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
        if (!this.getRequestURI().includes("Search")) {
            return;
        }
        if (window.outerWidth < 1024) {
            return;
        }
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
        if (status == 304) {
            related_content.timestamp = current_time + 3600;
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
        if (status == 304) {
            media.timestamp = current_time + 3600;
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
        if (status == 304) {
            trend.timestamp = current_time + 86400;
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
        if (status == 304) {
            session.Client.timestamp = current_time + 3600;
            localStorage.setItem(data_object, JSON.stringify(session));
            console.info(`Route: ${request_method} ${route}\nStatus: ${status}`);
            return;
        }
        localStorage.removeItem(data_object);
        this.getSession(route, request_method, data_object)
        .then((status) => console.info(`Route: ${request_method} ${route}\nStatus: ${status}`));
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
        const link = this.getHead().querySelector(`#${identifier}`);
        if (!link) {
            return;
        }
        link.rel = "stylesheet";
    }
}

/**
 * Loading the service worker.
 * @returns {Promise<void>}
 */
const load = async () => {
    try {
        const registration = await navigator.serviceWorker.register("/static/scripts/js/service-worker.js");
        console.info(`ServiceWorker registration successful.\nScope: ${registration.scope}`);
    } catch (error) {
        console.error(`ServiceWorker registration failed.\nError: ${error.message}`);
    }
};

const application = new YTD();
window.addEventListener("resize", () => application.resizeApplication(), true);
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => load());
}
document.addEventListener("DOMContentLoaded", () => application.addStylesheets(), true);
