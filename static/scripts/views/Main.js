/**
 * The component that is the main for all of the pages
 */
class Main extends React.Component {
    /**
     * Constructing the Main component of the application.
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
    }

    /**
     * Running the methods needed as soon as the component has been
     * successfully mounted.
     * @returns {void}
     */
    componentDidMount() {
        this.setData();
    }

    /**
     * Setting the main state of the component.
     * @returns {void}
     */
    setData() {
        this.setState((previous) => ({
            System: {
                ...previous.System,
                view_route: window.location.pathname,
                dom_element: document.body.querySelector("main"),
            },
        }));
    }

    /**
     * Rendering the component
     * @returns {HTMLElement}
     */
    render() {
        if (window.location.pathname.includes("Search")) {
            const search = {
                System: this.state.System,
            };
            return <Search data={search} />;
        } else if (window.location.pathname.includes("Download")) {
            return <Download />;
        } else {
            const homepage = {
                System: this.state.System,
            };
            return <Homepage data={homepage} />;
        }
    }

    // /**
    //  * Handling any change that is made in the user interface
    //  * @param {Event} event
    //  * @returns {void}
    //  */
    // handleChange(event) {
    //     const target = event.target;
    //     const value = target.value;
    //     const name = target.name;
    //     this.setState((previous) => ({
    //         Media: {
    //             ...previous.Media,
    //             [name]: value,
    //         },
    //     }));
    // }

    // /**
    //  * Handling the form submission
    //  * @param {Event} event
    //  * @returns {void}
    //  */
    // handleSubmit(event) {
    //     document.querySelector("#loading").style.display = "flex";
    //     const delay = 200;
    //     const url = new URL(this.state.Media.search);
    //     const platform = url.host.replaceAll("www.", "").replaceAll(".com", "");
    //     event.preventDefault();
    //     fetch("/Media/Search", {
    //         method: "POST",
    //         body: JSON.stringify({
    //             Media: {
    //                 search: this.state.Media.search,
    //                 platform: platform,
    //             },
    //         }),
    //         headers: {
    //             "Content-Type": "application/json",
    //         },
    //     })
    //         .then((response) => response.json())
    //         .then((data) => this.setMediaYouTubeUniformResourceLocator(data))
    //         .then(() => this.setMediaYouTubeIdentifier())
    //         .then(() => this.setRoute())
    //         .then(() => this.redirector(delay, this.state.System.url));
    // }

    // /**
    //  * Retrieving Media from the server by using its uniform
    //  * resource locator.
    //  * @returns {void}
    //  */
    // retrieveMedia() {
    //     document.querySelector("#loading").style.display = "flex";
    //     const delay = 200;
    //     const uniform_resource_locator = document.querySelector(
    //         "button[name='mediaDownloader']"
    //     ).value;
    //     const url = new URL(uniform_resource_locator);
    //     const platform = url.host.replaceAll("www.", "").replaceAll(".com", "");
    //     fetch("/Media/Download", {
    //         method: "POST",
    //         body: JSON.stringify({
    //             Media: {
    //                 uniform_resource_locator: uniform_resource_locator,
    //                 platform: platform,
    //             },
    //         }),
    //         headers: {
    //             "Content-Type": "application/json",
    //         },
    //     })
    //         .then((response) => response.json())
    //         .then((data) => {
    //             setTimeout(() => {
    //                 window.location.href = data.data.data.url;
    //             }, delay);
    //         });
    // }

    // /**
    //  * Redirecting the user to an intended url
    //  * @param {number} delay The amount of time in milliseconds before firing the method
    //  * @param {string} uniform_resource_locator The route
    //  * @returns {void}
    //  */
    // redirector(delay, uniform_resource_locator) {
    //     setTimeout(() => {
    //         window.location.href = uniform_resource_locator;
    //     }, delay);
    // }

    // /**
    //  * Setting the uniform resource locator for a specific YouTube content.
    //  * @param {object} data The dataset from the server.
    //  * @returns {void}
    //  */
    // setMediaYouTubeUniformResourceLocator(data) {
    //     this.setState((previous) => ({
    //         Media: {
    //             ...previous.Media,
    //             YouTube: {
    //                 ...previous.Media.YouTube,
    //                 uniform_resource_locator:
    //                     data.data.data.uniform_resource_locator,
    //             },
    //         },
    //     }));
    // }

    // /**
    //  * Extracting the identifier of a specific YouTube content.
    //  * @returns {void}
    //  */
    // setMediaYouTubeIdentifier() {
    //     if (
    //         this.state.Media.YouTube.uniform_resource_locator.includes(
    //             "youtube"
    //         )
    //     ) {
    //         this.setState((previous) => ({
    //             Media: {
    //                 ...previous.Media,
    //                 YouTube: {
    //                     ...previous.Media.YouTube,
    //                     identifier:
    //                         this.state.Media.YouTube.uniform_resource_locator.replace(
    //                             "https://www.youtube.com/watch?v=",
    //                             ""
    //                         ),
    //                 },
    //             },
    //         }));
    //     } else {
    //         this.setState((previous) => ({
    //             Media: {
    //                 ...previous.Media,
    //                 YouTube: {
    //                     ...previous.Media.YouTube,
    //                     identifier:
    //                         this.state.Media.YouTube.uniform_resource_locator
    //                             .replace("https://youtu.be/", "")
    //                             .replace(/\?.*/, ""),
    //                 },
    //             },
    //         }));
    //     }
    // }

    // /**
    //  * Setting the route to be redirected.
    //  * @returns {void}
    //  */
    // setRoute() {
    //     // Verifying the view route before updating to the new route.
    //     if (this.state.System.view_route == "/Search") {
    //         this.setState((previous) => ({
    //             System: {
    //                 ...previous.System,
    //                 url: `${this.state.System.view_route}/${this.state.Media.YouTube.identifier}`,
    //             },
    //         }));
    //     } else {
    //         this.setState((previous) => ({
    //             System: {
    //                 ...previous.System,
    //                 url: `/Search/${this.state.Media.YouTube.identifier}`,
    //             },
    //         }));
    //     }
    // }

    // /**
    //  * Downloading the file retrieved from the server.
    //  * @param {Event} event
    //  * @returns {void}
    //  */
    // getFile(event) {
    //     /**
    //      * Button that was clicked
    //      * @type {HTMLButtonElement}
    //      */
    //     const button = event.target.parentElement.parentElement;
    //     /**
    //      * Uniform resource locator of the file needed.
    //      * @type {string}
    //      */
    //     const file_location = button.value;
    //     let file_name = this.state.Media.YouTube.title;
    //     if (file_location.includes("/Public/Audio/")) {
    //         file_name = `${file_name}.mp3`;
    //     } else if (file_location.includes("/Public/Video/")) {
    //         file_name = `${file_name}.mp4`;
    //     }
    //     fetch("/Download", {
    //         method: "POST",
    //         body: JSON.stringify({
    //             file: file_location,
    //             file_name: file_name,
    //         }),
    //         headers: {
    //             "Content-Type": "application/json",
    //         },
    //     })
    //         .then((response) => response.blob())
    //         .then((data) => {
    //             let a = document.createElement("a");
    //             a.href = window.URL.createObjectURL(data);
    //             a.download = file_name;
    //             a.click();
    //         });
    // }

    // /**
    //  * Checking that the location of the media file needed is in
    //  * the state of the application.
    //  * @returns {string|void}
    //  */
    // verifyFile() {
    //     // Verifying that the file exists in the server to be able to verify the directory of the file, else, redirect the user.
    //     if (this.state.Media.YouTube.File.video != null) {
    //         return this.getMediaFile();
    //     } else {
    //         window.location.href = `/Search/${this.state.Media.YouTube.identifier}`;
    //     }
    // }

    // /**
    //  * Retrieving the media file for the application to load.
    //  * @returns {string}
    //  */
    // getMediaFile() {
    //     // Verifying the directory of the file to get its relative directory.
    //     if (this.state.Media.YouTube.File.video.includes("extractio")) {
    //         return this.state.Media.YouTube.File.video.replace(
    //             "/home/darkness4869/Documents/extractio",
    //             ""
    //         );
    //     } else {
    //         return this.state.Media.YouTube.File.video.replace(
    //             "/var/www/html/ytd_web_app",
    //             ""
    //         );
    //     }
    // }
}