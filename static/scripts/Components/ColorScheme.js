import React, { Component } from "react";


/**
 * It allows the component to be changed on the intereaction of
 * the user to change its color scheme.
 */
class ColorScheme extends Component {
    /**
     * Constructing the color scheme's component from the header.
     * @param {{data: {System: {color_scheme: string, api_call: number}}}} props The properties of the component.
     */
    constructor(props) {
        super(props);
        /**
         * The states of the component.
         * @type {{System: {color_scheme: string, api_call: number}}}
         */
        this.state = {
            System: {
                color_scheme: this.props.data.System.color_scheme,
                api_call: this.props.data.System.api_call,
            },
        }
    }

    /**
     * Running the functions needed as soon as the component is
     * mount.
     * @returns {void}
     */
    componentDidMount() {
        this.setState((previous) => ({
            ...previous,
            System: {
                ...previous.System,
                api_call: this.props.data.System.api_call,
                color_scheme: this.props.data.System.color_scheme,
            },
        }));
        this.adjustPage()
        .then((status) => console.info(`Route: ${window.location.pathname}\nComponent: Homepage.Header.ColorScheme\nComponent Status: Mount\nSession API Route: /\nSession API Status: ${status}`));
    }

    /**
     * Updating the component as soon as the states are different.
     * @param {{data: {System: {color_scheme: string, api_call: number}}}} previous_properties The properties of the component.
     * @returns {void}
     */
    componentDidUpdate(previous_properties) {
        if (this.props != previous_properties) {
            this.setState((previous) => ({
                ...previous,
                System: {
                    ...previous.System,
                    api_call: this.props.data.System.api_call,
                    color_scheme: this.props.data.System.color_scheme,
                },
            }));
            this.adjustPage()
            .then((status) => console.info(`Route: ${window.location.pathname}\nComponent: Homepage.Header.ColorScheme\nComponent Status: Updated\nSession API Route: /\nSession API Status: ${status}`));
        }
    }

    /**
     * Verifying that the color scheme does not have a value
     * @returns {Promise<number>}
     */
    async verifyColorScheme() {
        this.setState((previous) => ({
            System: {
                ...previous.System,
                color_scheme: this.props.data.System.color_scheme,
            },
        }));
        return 304;
    }

    /**
     * Adjusting the color scheme of the application
     * @returns {Promise<number>}
     */
    async adjustPage() {
        const root = document.querySelector(":root");
        const status = await this.verifyColorScheme();
        const color1 = (this.state.System.color_scheme == "light" || this.state.System.color_scheme == "") ? "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))" : "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))";
        const color2 = (this.state.System.color_scheme == "light" || this.state.System.color_scheme == "") ? "rgb(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)))" : "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)))";
        const color3 = (this.state.System.color_scheme == "light" || this.state.System.color_scheme == "") ? "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (69 / 255)), calc(var(--percentage) * (65 / 255)))" : "rgb(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (69 / 255)), calc(var(--percentage) * (65 / 255)))";
        const color5 = (this.state.System.color_scheme == "light" || this.state.System.color_scheme == "") ? "rgba(calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (250 / 255)), calc(var(--percentage) * (90 / 255)), calc(var(--percentage) / 2))" : "rgba(calc(var(--percentage) * (27 / 255)), calc(var(--percentage) * (54 / 255)), calc(var(--percentage) * (92 / 255)), calc(var(--percentage) / 2))";
        root.style.setProperty("--color1", color1);
        root.style.setProperty("--color2", color2);
        root.style.setProperty("--color3", color3);
        root.style.setProperty("--color5", color5);
        return status;
    }

    /**
     * Rendering the component which will allow the user to change
     * the color scheme.
     * @returns {HTMLElement}
     */
    render() {
        return (this.state.System.color_scheme == "dark") ? (<i class="fa-solid fa-toggle-on"></i>) : (<i class="fa-solid fa-toggle-off"></i>);
    }
}

export default ColorScheme;