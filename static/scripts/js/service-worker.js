const main_cache_name = "extractio-app-cache-v3";
const uniform_resource_locators_to_cache = [
    "/",
    "/static/stylesheets/ytd.css",
    "/static/stylesheets/desktop.css",
    "/static/stylesheets/tablet.css",
    "/static/stylesheets/mobile.css",
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
 * @param {Event} event
 * @returns {void}
 */
const install = (event) => {
    event.waitUntil(
        caches.open(main_cache_name)
        .then((cache) => {
            console.log('Opened cache');
            return cache.addAll(uniform_resource_locators_to_cache);
        })
    );
};
self.addEventListener("install", (event) => install(event));
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
        .then((response) => {
            if (response) {
                return response;
            }
            return fetch(event.request)
            .then((response) => {
                return caches.open(main_cache_name)
                .then((cache) => {
                    cache.put(event.request, response.clone());
                    return response;
                });
            });
        })
    );
});
self.addEventListener('activate', (event) => {
    const cache_whitelist = [main_cache_name];
    event.waitUntil(
        caches.keys().then((cache_names) => {
            return Promise.all(
                cache_names.map((cache_name) => {
                    if (!cache_whitelist.includes(cache_name)) {
                        return caches.delete(cache_name);
                    }
                })
            );
        })
    );
});