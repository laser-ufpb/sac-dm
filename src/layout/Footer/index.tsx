import { Container } from "./styles";
import { Link } from "react-router-dom";

const VERSION = "1.0.0";

export function Footer() {
  return (
    <Container>
      <Link to={"https://controlit.com.br"} target="_blank">
        <small>@2024 Aviação FE</small>
      </Link>

      <small>Version: {VERSION}</small>
    </Container>
  );
}
