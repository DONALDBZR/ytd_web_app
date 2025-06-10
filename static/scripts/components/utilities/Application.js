/**
 * The utility class of the Application.
 */
class Application {
    /**
     * Retrieving the host name which will be used as the platform for the search from the parsed uniform resource locator.
     * 
     * Currently, this function only supports YouTube uniform resource locators.  If the hostname does not match a known YouTube format, it throws an error.
     * @param {URL} uniform_resource_locator The parsed uniform resource locator.
     * @returns {string} The name of the supported platform.
     * @throws {Error} If the URL does not belong to a supported platform.
     */
    getPlatform(uniform_resource_locator) {
        const hostname = uniform_resource_locator.hostname.toLowerCase();
        if (hostname == "youtu.be" || hostname.includes("youtube")) {
            return "youtube";
        }
        throw new Error("The platform is not supported by the application.");
    }
}

export default Application;
