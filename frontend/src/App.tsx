import { NavLink, Route, Routes } from "react-router-dom";
import { ProviderSelector } from "./components/Common";
import Artifacts from "./pages/Artifacts";
import Chat from "./pages/Chat";

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <span className="app-title">Lenny Growth Assistant</span>
        <ProviderSelector />
        <nav className="app-nav">
          <NavLink to="/">Chat</NavLink>
          <NavLink to="/artifacts">Artifacts</NavLink>
        </nav>
      </header>

      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/artifacts" element={<Artifacts />} />
      </Routes>
    </div>
  );
}

export default App;
