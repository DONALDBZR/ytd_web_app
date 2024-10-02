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
        this.optimize();
    }

    /**
     * Retrieving the metadata of the media content.
     * @param {string} needle The needle to be excluded.
     * @returns {Promise<{Media: {YouTube: {uniform_resource_locator: string, author: string, title: string, identifier: string, author_channel: string, views: number, published_at: string, thumbnail: string, duration: string, audio: string, video: string}}}>}
     */
    async getMedia(needle) {
        const response = await this.getMediaResponse(needle);
        return response.json();
    }

    /**
     * Sending the request to the server to retrieve the data
     * needed to the Media API.
     * @param {string} needle The needle to be excluded.
     * @returns {Promise<Response>}
     */
    async getMediaResponse(needle) {
        return fetch(`/Media/${this.getRequestURI().replace(needle, "")}`, {
            method: "GET",
        });
    }

    /**
     * Defining the title of the page for the application.
     * @returns {void}
     */
    addTitle() {
        this.setTitle(document.createElement("title"));
        if (this.getRequestURI() == "" || this.getRequestURI() == "/") {
            this.getTitle().text = "Extractio";
        } else if (this.getRequestURI() == "/Search/") {
            this.getTitle().text = "Extractio: Search";
        } else if (this.getRequestURI().includes("/Search/") && this.getRequestURI() != "/Search/") {
            this.getMedia("/Search/")
            .then((response) => {
                this.getTitle().text = `Extractio Data: ${response.Media.YouTube.title}`;
            });
        } else if (this.getRequestURI().includes("/Download/")) {
            this.getMedia("/Download/YouTube/")
            .then((response) => {
                this.getTitle().text = `Extractio: ${response.Media.YouTube.title}`;
            });
        }
        this.getHead().appendChild(this.getTitle());
    }

    /**
     * Defining the description of the page.
     * @returns {void}
     */
    addDescription() {
        this.setMeta(document.createElement("meta"));
        this.getMeta().name = "description";
        if (this.getRequestURI() == "" || this.getRequestURI() == "/") {
            this.getMeta().content = "Extractio extracts content from various platforms for various needs.";
        } else if (this.getRequestURI() == "/Search/") {
            this.getMeta().content = "The content needed can be searched, here.";
        } else if (this.getRequestURI().includes("/Search/") && this.getRequestURI() != "/Search/") {
            this.getMedia("/Search/")
            .then((response) => {
                const uniform_resource_locator = new URL(response.Media.YouTube.uniform_resource_locator);
                const platform = uniform_resource_locator.hostname.replace("www.", "").replace(".com", "");
                this.getMeta().content = `Metadata for the content from ${response.Media.YouTube.author} on ${platform} entitled ${response.Media.YouTube.title}`;
            });
        } else if (this.getRequestURI().includes("/Download/")) {
            this.getMedia("/Download/YouTube/")
            .then((response) => {
                const uniform_resource_locator = new URL(response.Media.YouTube.uniform_resource_locator);
                const platform = uniform_resource_locator.hostname.replace("www.", "").replace(".com", "");
                this.getMeta().content = `Content from ${response.Media.YouTube.author} on ${platform} entitled ${response.Media.YouTube.title}`;
            });
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
        for (let index = 0; index < this._stylesheets.length; index++) {
            const link = document.createElement("link");
            link.href = `${this.getOrigin()}${this._stylesheets[index]}`;
            link.media = this.getMediaQuery(link.href);
            link.rel = this.getRelationship();
            link.type = this.getMimeType();
            this.getHead().appendChild(link);
        }
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
        this.loadData();
    }

    /**
     * Loading the data needed for the API.
     * @returns {void}
     */
    loadData() {
        this.loadDataHomepage();
    }

    /**
     * Loading the data specifically for the homepage.
     * @returns {void}
     */
    loadDataHomepage() {
        this.getSession();
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
     * Retrieving the session of the user.
     * @returns {void}
     */
    async setSession() {
        const data_object = "session";
        const session: {Client: {timestamp: number, color_scheme: string}} = JSON.parse(localStorage.getItem(data_object));
        const route = "/Session/";
        const request_method = "GET";
        let status = 0;
        if (!session) {
            const response = await fetch(route, {
                method: request_method,
            });
            const data = await response.json();
            status = response.status;
            localStorage.setItem(data_object, JSON.stringify(data));
            console.info(`Route: ${request_method} ${route}\nStatus: ${status}`);
        } else {
            // const current_time = Math.floor(Date.now() / 1000);
            // const session_expiration_time = session.Client.timestamp + 3600;
            // if (current_time < session_expiration_time) {
            //     status = 304;
            //     session.Client.timestamp = current_time + 3600;
            //     localStorage.setItem(data_object, JSON.stringify(session));
            //     console.info(`Route: ${request_method} ${route}\nStatus: ${status}`);
            // } else {
                
            // }
        }
    }
}

const application = new YTD();
window.addEventListener("resize", () => application.resizeApplication(), true);
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/scripts/js/service-worker.js')
            .then(registration => {
                console.log('ServiceWorker registration successful with scope: ', registration.scope);
            })
            .catch(error => {
                console.log('ServiceWorker registration failed: ', error);
            });
    });
}
