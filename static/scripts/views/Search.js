/**
 * The Application that is going to be rendered in the DOM
 */
class Application extends React.Component {
    /**
     * Constructing the application from React's Component
     * @param {*} props The properties of the component
     */
    constructor(props) {
        super(props);
        this.state = {
            System: {
                color_scheme: "",
                status: 0,
                message: "",
                url: "",
            },
            Media: {
                search: "",
                YouTube: {
                    uniform_resource_locator: "",
                    artist: "",
                    title: "",
                    author: "",
                    author_channel: "",
                    views: 0,
                    published_at: "",
                    thumbnail: "",
                    duration: "",
                },
            },
        };
    }
    /**
     * Retrieving the session of the application
     * @returns {void}
     */
    getSession() {
        fetch("/Session", {
            method: "GET",
        })
            .then((response) => response.json())
            .then((data) =>
                this.setState({
                    System: {
                        color_scheme: data.Client.color_scheme,
                    },
                })
            )
            .then(() => this.verifyColorScheme())
            .then(() => this.adjustPage());
    }
    /**
     * Verifying that the color scheme does not have a value
     * @returns {void}
     */
    verifyColorScheme() {
        if (this.state.System.color_scheme == "") {
            this.setState({
                System: {
                    color_scheme: "light",
                },
            });
        }
    }
    /**
     * Adjusting the color scheme of the application
     * @returns {string}
     */
    adjustPage() {
        const root = document.querySelector(":root");
        if (
            this.state.System.color_scheme == "light" ||
            this.state.System.color_scheme == ""
        ) {
            const color1 =
                "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))";
            const color2 =
                "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))";
            const color3 =
                "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (69 / 255)), calc(var(--percentage) * (65 / 255)))";
            root.style.setProperty("--color1", color1);
            root.style.setProperty("--color2", color2);
            root.style.setProperty("--color3", color3);
        } else {
            const color1 =
                "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))";
            const color2 =
                "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))";
            const color3 =
                "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (69 / 255)), calc(var(--percentage) * (65 / 255)))";
            root.style.setProperty("--color1", color1);
            root.style.setProperty("--color2", color2);
            root.style.setProperty("--color3", color3);
        }
    }
    /**
     * Changing the color scheme according to the user's taste
     * @returns {void}
     */
    setColorScheme() {
        const delay = 200;
        event.preventDefault();
        let color_scheme = document.querySelector(
            "button[name='colorSchemeChanger']"
        ).value;
        if (color_scheme == "light") {
            color_scheme = "dark";
        } else {
            color_scheme = "light";
        }
        fetch("/Session/Post", {
            method: "POST",
            body: JSON.stringify({
                Client: {
                    color_scheme: color_scheme,
                },
            }),
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((response) => response.json())
            .then(() => {
                setTimeout(() => {
                    window.location.href = window.location.href;
                }, delay);
            });
    }
    /**
     * Handling any change that is made in the user interface
     * @param {Event} event
     * @returns {void}
     */
    handleChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;
        this.setState((previous) => ({
            Media: {
                ...previous.Media,
                [name]: value,
            },
        }));
    }
    /**
     * Handling the form submission
     * @param {Event} event
     * @returns {void}
     */
    handleSubmit(event) {
        const delay = 200;
        event.preventDefault();
        fetch("/Media/Search", {
            method: "POST",
            body: JSON.stringify({
                Media: {
                    search: this.state.Media.search,
                },
            }),
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((response) => response.json())
            .then((data) =>
                this.setState({
                    Media: {
                        artist: data.YouTube.artist,
                        title: data.YouTube.title,
                        uniform_resource_locator:
                            data.YouTube.uniform_resource_locator,
                        identifier: data.YouTube.identifier,
                    },
                })
            )
            .then(() => {
                if (window.location.pathname == "/Search") {
                    this.setState((previous) => ({
                        System: {
                            ...previous.System,
                            url: `${window.location.pathname}/${this.state.Media.identifier}`,
                        },
                    }));
                } else {
                    this.setState((previous) => ({
                        System: {
                            ...previous.System,
                            url: `/Search/${this.state.Media.identifier}`,
                        },
                    }));
                }
            })
            .then(() => this.redirector(delay, this.state.System.url));
    }
    /**
     * Redirecting the user to an intended url
     * @param {int} delay The amount of time in milliseconds before firing the method
     * @param {string} uniform_resource_locator The route
     * @returns {void}
     */
    redirector(delay, uniform_resource_locator) {
        setTimeout(() => {
            window.location.href = uniform_resource_locator;
        }, delay);
    }
    /**
     * Retrieving the data of the media content that is searched by the user
     * @returns {void}
     */
    getMedia() {
        fetch("/Media", {
            method: "GET",
        })
            .then((response) => response.json())
            .then((data) => {
                if (typeof data.Media.YouTube != "undefined") {
                    this.setState((previous) => ({
                        Media: {
                            ...previous.Media,
                            YouTube: {
                                uniform_resource_locator:
                                    data.Media.YouTube.uniform_resource_locator,
                                artist: data.Media.YouTube.artist,
                                title: data.Media.YouTube.title,
                                author: data.Media.YouTube.author,
                                author_channel:
                                    data.Media.YouTube.author_channel,
                                views: data.Media.YouTube.views,
                                published_at: data.Media.YouTube.published_at,
                                thumbnail: data.Media.YouTube.thumbnail,
                                duration: data.Media.YouTube.duration,
                            },
                        },
                    }));
                }
            });
    }
    /**
     * Rendering the application by instantiating its components
     * @returns {HTMLBodyElement}
     */
    render() {
        return [<Header />, <Main />, <Footer />];
    }
}
/**
 * The component that is the header
 */
class Header extends Application {
    /**
     * Constructing the header component and also inheriting the properties and states from the application
     * @param {*} props
     */
    constructor(props) {
        super(props);
    }
    /**
     * Running the methods needed as soon as the component has been successfully mounted
     * @returns {void}
     */
    componentDidMount() {
        this.getSession();
    }
    /**
     * Rendering the component
     * @returns {HTMLHeaderElement}
     */
    render() {
        return (
            <header>
                <nav>
                    <div>
                        <a href="/">Extractio</a>
                    </div>
                    <div>
                        <div class="active">
                            <a href="/Search">
                                <i class="fa fa-search"></i>
                            </a>
                        </div>
                        <div>
                            <button
                                name="colorSchemeChanger"
                                value={this.state.System.color_scheme}
                                onClick={this.setColorScheme}
                            >
                                <ColorScheme />
                            </button>
                        </div>
                    </div>
                </nav>
            </header>
        );
    }
}
/**
 * It allows the component to be change on intearction of the user to change its color scheme
 */
class ColorScheme extends Header {
    /**
     * Constructing the color scheme's component and also inheriting the properties and states from the header
     * @param {*} props
     */
    constructor(props) {
        super(props);
    }
    /**
     * Rendering the component which allows the user to change the color scheme
     * @returns {HTMLButtonElement}
     */
    render() {
        if (this.state.System.color_scheme == "dark") {
            return <i class="fa-solid fa-toggle-on"></i>;
        } else if (this.state.System.color_scheme == "light") {
            return <i class="fa-solid fa-toggle-off"></i>;
        }
    }
}
/**
 * The component that is the main
 */
class Main extends Application {
    /**
     * Rendering the component
     * @returns {HTMLMainElement}
     */
    render() {
        return (
            <main>
                <form method="POST" onSubmit={this.handleSubmit.bind(this)}>
                    <input
                        type="search"
                        placeholder="Search..."
                        name="search"
                        value={this.state.Media.search}
                        onChange={this.handleChange.bind(this)}
                        required
                    />
                    <button>
                        <i class="fa fa-search"></i>
                    </button>
                </form>
                <Media />
            </main>
        );
    }
}
/**
 * The Media Component that will render according the to the data retrieved
 */
class Media extends Main {
    /**
     * Constructing the media component and also inheriting the properties and states from the main
     * @param {*} props
     */
    constructor(props) {
        super(props);
    }
    /**
     * Running the methods needed as soon as the component has been successfully mounted
     * @returns {void}
     */
    componentDidMount() {
        if (window.location.pathname != "/Search") {
            this.getMedia();
        }
    }
    /**
     * Rendering the component
     * @returns {HTMLDivElement}
     */
    render() {
        if (
            window.location.pathname != "/Search" &&
            this.state.Media.YouTube.identifier != ""
        ) {
            return (
                <div className="Media">
                    <YouTube />
                </div>
            );
        }
    }
}
/**
 * The component that is the YouTube component given that it will only be rendered only when the data corresponds to it.
 */
class YouTube extends Media {
    /**
     * Constructing the Youtube component and also inheriting the properties and states from the media
     * @param {*} props
     */
    constructor(props) {
        super(props);
    }
    /**
     * Rendering the component
     * @returns {HTMLDivElement}
     */
    render() {
        return (
            <div className="YouTube">
                <div>
                    <a
                        href={this.state.Media.YouTube.uniform_resource_locator}
                        target="__blank"
                    >
                        <img src={this.state.Media.YouTube.thumbnail} />
                    </a>
                </div>
                <div class="data">
                    <div>{`${this.state.Media.YouTube.artist} - ${this.state.Media.YouTube.title}`}</div>
                    <div>
                        <a
                            href={this.state.Media.YouTube.author_channel}
                            target="__blank"
                        >
                            {this.state.Media.YouTube.author}
                        </a>
                    </div>
                    <div>
                        <div id="duration">
                            <div>Duration:</div>
                            <div>{this.state.Media.YouTube.duration}</div>
                        </div>
                        <div id="views">
                            <div>Views:</div>
                            <div>
                                {this.state.Media.YouTube.views.toLocaleString(
                                    "en-US"
                                )}
                            </div>
                        </div>
                    </div>
                    <div>
                        <button
                            name="mediaDownloader"
                            value={
                                this.state.Media.YouTube
                                    .uniform_resource_locator
                            }
                            onClick={this.retrieveMedia}
                        >
                            <i class="fa-solid fa-download"></i>
                        </button>
                    </div>
                </div>
            </div>
        );
    }
}
/**
 * The component that is the footer
 */
class Footer extends Application {
    /**
     * Rendering the component
     * @returns {HTMLFooterElement}
     */
    render() {
        return (
            <footer>
                <div>Extractio</div>
            </footer>
        );
    }
}
// Rendering the page
ReactDOM.render(<Application />, document.body);
