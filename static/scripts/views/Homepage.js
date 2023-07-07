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
                        color_scheme: data.color_scheme,
                    },
                })
            )
            .then(() => this.verifyColorScheme());
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
            this.adjustPage();
        }
    }
    /**
     * Changing the color scheme according to the user's taste
     * @returns {void}
     */
    setColorScheme() {
        if (
            this.state.System.color_scheme == "light" ||
            this.state.System.color_scheme == ""
        ) {
            this.setState({
                System: {
                    color_scheme: "dark",
                },
            });
            this.setSession();
        } else {
            this.setState({
                System: {
                    color_scheme: "light",
                },
            });
            this.setSession();
        }
    }
    /**
     * Modifying the session and storing it accordingly
     * @returns {void}
     */
    setSession() {
        const delay = 2000;
        event.preventDefault();
        fetch("/Session/Post", {
            method: "POST",
            body: JSON.stringify({
                color_scheme: this.state.System.color_scheme,
            }),
            headers: "application/json",
        })
            .then((response) => response.json())
            .then(() => this.redirector(delay));
    }
    /**
     * Adjusting the color scheme of the application
     * @returns {void}
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
                "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))";
            const color2 =
                "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))";
            const color3 =
                "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (69 / 255)), calc(var(--percentage) * (65 / 255)))";
            root.style.setProperty("--color1", color1);
            root.style.setProperty("--color2", color2);
            root.style.setProperty("--color3", color3);
        }
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
     * Rendering the component
     * @returns {HTMLHeaderElement}
     */
    render() {
        return (
            <header>
                <nav>
                    <div class="active">
                        <a href="/">Extractio</a>
                    </div>
                    <div>
                        <div>
                            <a href="/search">
                                <i class="fa fa-search"></i>
                            </a>
                        </div>
                        <div>
                            <ColorScheme />
                        </div>
                    </div>
                </nav>
            </header>
        );
    }
}
/**
 * The color scheme
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
     * Running the methods needed as soon as the component has been successfully mounted
     * @returns {void}
     */
    componentDidMount() {
        this.getSession();
    }
    /**
     * Rendering the component which allows the user to change the color scheme
     * @returns {HTMLButtonElement}
     */
    render() {
        if (this.state.System.color_scheme == "light") {
            return (
                <button onclick={this.setColorScheme}>
                    <i class="fa-solid fa-toggle-off"></i>
                </button>
            );
        } else {
            return (
                <button onclick={this.setColorScheme}>
                    <i class="fa-solid fa-toggle-on"></i>
                </button>
            );
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
                <p>
                    The aim of the application is that software and contents
                    must be free and it allows anyone to get content from
                    certain platforms to be obtained for free as it is an
                    application developed for people by people.
                </p>
                <div>
                    <div>
                        <i class="fa-brands fa-youtube"></i>
                    </div>
                </div>
            </main>
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
