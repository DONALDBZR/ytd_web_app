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
        this.render();
    }
    /**
     * Importing and rendering the scripts
     * @returns {void}
     */
    render() {
        const script = document.createElement("script");
        this.setBodyClassName(this.getBody().className);
        this.setMimeType("text/babel");
        if (this.getBodyClassName().includes("error")) {
            if (this.getBodyClassName().includes("404")) {
                script.src = "/static/scripts/views/HTTP404.js";
            }
        } else if (this.getBodyId().includes("Search")) {
            script.src = "/static/scripts/views/Search.js";
        } else {
            script.src = `/static/scripts/views/${this.getBodyId()}.js`;
        }
        script.type = this.getMimeType();
        this.getBody().appendChild(script);
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
