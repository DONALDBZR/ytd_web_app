import React from "react";
import { useParams } from "react-router-dom";


/**
 * A higher-order component (HOC) that injects route parameters from `react-router-dom` into the wrapped component as a `parameters` prop.
 * @param {React.ComponentType<any>} Component - The component to enhance with route parameters.
 * @returns {React.FC<any>}
 */
function routeComponent(Component) {
    return function renderComponent(properties) {
        return <WrappedComponent {...properties} Component={Component} />;
    };
}

/**
 * A helper component that renders the provided component and injects route parameters.
 * @param {Object} props - The props passed to the enhanced component.
 * @param {React.ComponentType<any>} props.Component - The component to render.
 * @returns {JSX.Element}
 */
function WrappedComponent({ Component, ...props }) {
    const parameters = useParams();
    return <Component {...props} parameters={parameters} />;
}

export default routeComponent;
