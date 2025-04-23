/**
 * The name of the cache for the service worker.
 * @type {string}
 */
const main_cache_name = "extractio-app-cache-v3";
/**
 * The uniform resource locators to cache.
 * @type {string[]}
 */
const uniform_resource_locators_to_cache = [
    "/",
    "/static/stylesheets/ytd.css",
    "/static/stylesheets/ytd/Homepage.css",
    "/static/stylesheets/ytd/Search.css",
    "/static/stylesheets/desktop.css",
    "/static/stylesheets/desktop/Homepage.css",
    "/static/stylesheets/desktop/Search.css",
    "/static/stylesheets/tablet.css",
    "/static/stylesheets/tablet/Homepage.css",
    "/static/stylesheets/tablet/Search.css",
    "/static/stylesheets/mobile.css",
    "/static/stylesheets/mobile/Homepage.css",
    "/static/stylesheets/mobile/Search.css",
    "/static/scripts/js/react.production.min.js",
    "/static/scripts/js/react-dom.production.min.js",
    "/static/scripts/js/babel.min.js",
    "/static/scripts/js/ytd.js",
    "/static/scripts/views/Homepage.js",
    "/static/scripts/views/Search.js",
    "/static/scripts/views/Header.js",
    "/static/scripts/views/Header/ColorScheme.js",
    "/static/scripts/views/Header/Homepage.js",
    "/static/scripts/views/Header/Search.js",
    "/static/scripts/views/Main.js",
    "/static/scripts/views/Main/Homepage.js",
    "/static/scripts/views/Main/Media.js",
    "/static/scripts/views/Main/RelatedContents.js",
    "/static/scripts/views/Main/Search.js",
    "/static/scripts/views/Main/Trend.js",
    "/static/scripts/views/Main/YouTube.js",
    "/static/scripts/views/Footer.js",
    "/manifest.json",
    "/static/images/icons/Extractio.png",
];

/**
 * The listener for the installation of the service worker.
 * @param {Event} event The install event
 * @returns {void}
 */
const install = (event) => {
    event.waitUntil(
        caches.open(main_cache_name)
        .then((cache) => cacheUniformResourceLocators(cache))
    );
};

/**
 * Caching the uniform resource locators.
 * @param {Cache} cache The cache storage to be used.
 * @returns {Promise<void>}
 */
const cacheUniformResourceLocators = (cache) => {
    console.log('Opened cache');
    return cache.addAll(uniform_resource_locators_to_cache);
};

/**
 * Retrieving the data to be cached.
 * @param {Event} event The fetch event
 * @returns {void}
 */
const retrieveData = (event) => {
    event.respondWith(
        caches.match(event.request)
        .then((response) => manageResponse(response, event.request))
    );
};

/**
 * Managing the response of the service worker when retrieving
 * the data to be cached.
 * @param {Response|undefined} response The response to be managed
 * @param {RequestInfo|URL} request The request from the event.
 * @returns {Response|Promise<Response>}
 */
const manageResponse = (response, request) => {
    if (response) {
        return response;
    }
    return fetch(request)
    .then((response) => manageCachedResponse(response, request));
};

/**
 * Managing the response of the requested cached event.
 * @param {Response} response The response to be managed.
 * @param {RequestInfo|URL} request The request from the event.
 * @returns {Promise<Response>}
 */
const manageCachedResponse = async (response, request) => {
    const cache = await caches.open(main_cache_name);
    return cloneResponse(cache, request, response);
};

/**
 * Cloning the response of the service worker.
 * @param {Cache} cache The cache storage to be used.
 * @param {RequestInfo|URL} request The request from the event.
 * @param {Response} response The response to be cloned.
 * @returns {Response}
 */
const cloneResponse = (cache, request, response) => {
    cache.put(request, response.clone());
    return response;
};

/**
 * Activating the service worker.
 * @param {Event} event The activate event
 * @returns {void}
 */
const activate = (event) => {
    const cache_whitelist = [main_cache_name];
    event.waitUntil(
        caches.keys()
        .then((cache_names) => maintainCache(cache_names, cache_whitelist, caches))
    );
};

/**
 * Maintaining the caches.
 * @param {string[]} cache_names The cache names to be maintained.
 * @param {string[]} cache_whitelist The cache whitelist.
 * @param {CacheStorage} caches The cache storage to be used.
 * @returns {Promise<(boolean | undefined)[]>}
 */
const maintainCache = (cache_names, cache_whitelist, caches) => {
    return Promise.all(
        cache_names.map((cache_name) => deleteBlacklistedCaches(cache_whitelist, cache_name, caches))
    );
};

/**
 * Removing blacklisted caches.
 * @param {string[]} cache_whitelist The cache whitelist.
 * @param {string} cache_name The cache name to be removed.
 * @param {CacheStorage} caches The cache storage to be used.
 * @returns {Promise<boolean> | undefined}
 */
const deleteBlacklistedCaches = (cache_whitelist, cache_name, caches) => {
    if (!cache_whitelist.includes(cache_name)) {
        return caches.delete(cache_name);
    }
};

self.addEventListener("install", (event) => install(event));
self.addEventListener('fetch', (event) => retrieveData(event));
self.addEventListener('activate', (event) => activate(event));