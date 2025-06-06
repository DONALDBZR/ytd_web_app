import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Homepage from "./Homepage";
import Search from "./Search";
import Download from "./Download";


const root = ReactDOM.createRoot(document.body);

root.render(
    <Router>
        <Routes>
            <Route path="/" element={<Homepage />} />
            <Route path="/Search/:id" element={<Search />} />
            <Route path="/Search/Shorts/:id" element={<Search />} />
            <Route path="/Download/YouTube/:id" element={<Download />} />
            <Route path="/Download/YouTube/Shorts/:id" element={<Download />} />
        </Routes>
    </Router>
);
