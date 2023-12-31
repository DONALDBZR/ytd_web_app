/**
 * The main script that will initialize the application as needed
 */
class YTD {
    /**
     * Setting the data needed as well as initalizing the application
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
     * Initializing the application
     * @returns {void}
     */
    init() {
        this.setRequestURI(window.location.pathname);
        this.setBody(document.body);
        if (this.getRequestURI() == "/") {
            this.setBodyId("Homepage");
        } else {
            this.setBodyId(this.getRequestURI().replaceAll("/", ""));
        }
        this.getBody().id = this.getBodyId();
        this.optimize();
    }
    /**
     * Defining the title of the page for the application.
     * @returns {void}
     */
    addTitle() {
        this.setTitle(document.createElement("title"));
        // Verifying the request uniform resource indicator to set up the title of the page
        if (this.getRequestURI() == "" || this.getRequestURI() == "/") {
            this.getTitle().text = "Extractio";
        } else if (this.getRequestURI() == "/Search/") {
            this.getTitle().text = "Extractio: Search";
        } else if (
            this.getRequestURI().includes("/Search/") &&
            this.getRequestURI() != "/Search/"
        ) {
            fetch(`/Media/${this.getRequestURI().replace("/Search/", "")}`, {
                method: "GET",
            })
                .then((response) => response.json())
                .then((data) => {
                    this.getTitle().text = `Extractio Data: ${data.Media.YouTube.title}`;
                });
        } else if (this.getRequestURI().includes("/Download/")) {
            fetch(
                `/Media/${this.getRequestURI().replace(
                    "/Download/YouTube/",
                    ""
                )}`,
                {
                    method: "GET",
                }
            )
                .then((response) => response.json())
                .then((data) => {
                    this.getTitle().text = `Extractio: ${data.Media.YouTube.title}`;
                });
        }
        document.head.appendChild(this.getTitle());
    }
    /**
     * Defining the description of the page.
     * @returns {void}
     */
    addDescription() {
        this.setMeta(document.createElement("meta"));
        this.getMeta().name = "description";
        if (this.getRequestURI() == "" || this.getRequestURI() == "/") {
            this.getMeta().content =
                "Extractio extracts content from various platforms for various needs.";
        } else if (this.getRequestURI() == "/Search/") {
            this.getMeta().content =
                "The content needed can be searched, here.";
        } else if (
            this.getRequestURI().includes("/Search/") &&
            this.getRequestURI() != "/Search/"
        ) {
            fetch(`/Media/${this.getRequestURI().replace("/Search/", "")}`, {
                method: "GET",
            })
                .then((response) => response.json())
                .then((data) => {
                    const uniform_resource_locator = new URL(
                        data.Media.YouTube.uniform_resource_locator
                    );
                    const platform = uniform_resource_locator.hostname
                        .replace("www.", "")
                        .replace(".com", "");
                    this.getMeta().content = `Metadata for the content from ${data.Media.YouTube.author} on ${platform} entitled ${data.Media.YouTube.title}`;
                });
        } else if (this.getRequestURI().includes("/Download/")) {
            fetch(
                `/Media/${this.getRequestURI().replace(
                    "/Download/YouTube/",
                    ""
                )}`,
                {
                    method: "GET",
                }
            )
                .then((response) => response.json())
                .then((data) => {
                    const uniform_resource_locator = new URL(
                        data.Media.YouTube.uniform_resource_locator
                    );
                    const platform = uniform_resource_locator.hostname
                        .replace("www.", "")
                        .replace(".com", "");
                    this.getMeta().content = `Content from ${data.Media.YouTube.author} on ${platform} entitled ${data.Media.YouTube.title}`;
                });
        }
        document.head.appendChild(this.getMeta());
        setTimeout(() => this.configureRobot(), 200);
    }
    /**
     * Configuring the pages for which the web crawlers can index
     * on the application.
     * @returns {void}
     */
    configureRobot() {
        this.setMeta(document.createElement("meta"));
        this.getMeta().name = "robots";
        if (this.getRequestURI() == "" || this.getRequestURI() == "/") {
            this.getMeta().content = "index, follow";
        } else if (this.getRequestURI() == "/Search/") {
            this.getMeta().content = "index, follow";
        } else if (
            this.getRequestURI().includes("/Search/") &&
            this.getRequestURI() != "/Search/"
        ) {
            this.getMeta().content = "index, nofollow";
        } else if (this.getRequestURI().includes("/Download/")) {
            this.getMeta().content = "index, nofollow";
        }
        document.head.appendChild(this.getMeta());
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
     * Styling the application
     * @returns {void}
     */
    style() {
        this.setRelationship("stylesheet");
        this.setMimeType("text/css");
        for (let index = 0; index < this._stylesheets.length; index++) {
            const link = document.createElement("link");
            link.href = this._stylesheets[index];
            if (link.href.includes("desktop")) {
                link.media = this._mediaQueries[0];
            } else if (link.href.includes("mobile")) {
                link.media = this._mediaQueries[2];
            } else if (link.href.includes("tablet")) {
                link.media = this._mediaQueries[1];
            }
            link.rel = this.getRelationship();
            link.type = this.getMimeType();
            document.head.appendChild(link);
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
    }
}
const application = new YTD();
