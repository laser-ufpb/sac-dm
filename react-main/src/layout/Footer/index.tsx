import { Container } from "./styles";
import { Link } from "react-router-dom";

const VERSION = "1.0.1";

export function Footer() {
  return (
    <Container>
      <Link
        to={"https://www.linkedin.com/in/joao-victor-pedrosa-candido/"}
        target="_blank"
      >
        <small>@2024 Aviação FE</small>
      </Link>

      <small>Version: {VERSION}</small>
    </Container>
  );
}
