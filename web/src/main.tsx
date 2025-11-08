import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import "./index.css";
import "./Home"

function App(){
  return (
    <BrowserRouter>
      <nav className="p-4 bg-slate-100">
        <Link className="mr-4" to="/">Home</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home/>}/>
      </Routes>
    </BrowserRouter>
  )
}

createRoot(document.getElementById("root")!).render(<App />);
