import { ThemeProvider } from "styled-components";
import "./index.css";
import { theme } from "./styles/theme";
import { Header } from "./layout/Header";
import { BrowserRouter } from "react-router-dom";
import { Routes } from "./app/router";
import { Footer } from "./layout/Footer";
import { AuthProvider } from "./app/contexts/AuthContext";
import { Login } from "./pages/Login";

function App() {
  return (
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        <AuthProvider>
          <Header />
          <Login />
          <div className="container">
            <Routes />
          </div>
          <Footer />
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;
