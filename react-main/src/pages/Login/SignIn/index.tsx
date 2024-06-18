import { useContext, useState } from "react";
import { DefaultInput } from "../../../components/forms/DefaultInput";
import { FormGroup } from "../../../components/forms/FormGroup";
import { FormContainer, HeaderContent } from "../styles";
import { AuthContext } from "../../../app/contexts/AuthContext";
import { Visibility, VisibilityOff } from "@mui/icons-material";
import { theme } from "../../../styles/theme";
import { Button } from "@mui/material";

export const SignIn = () => {
  const [isLoading, setIsLoading] = useState(false);
  const { signIn } = useContext(AuthContext);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const handleLogin = async () => {
    setIsLoading(true);
    try {
      await signIn(username, password);
    } catch (error) {
      console.log({ error });
    } finally {
      setIsLoading(false);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <FormContainer
      onKeyDown={(event: React.KeyboardEvent) => {
        if (event.key === "Enter") {
          event.preventDefault();

          handleLogin();
        }
      }}
    >
      <HeaderContent>
        <h2>Login</h2>
      </HeaderContent>

      <FormGroup>
        <label htmlFor="username">Nome de Usuário</label>
        <DefaultInput
          placeholder="Digite seu nome de usuário"
          value={username}
          onChange={(event) => setUsername(event.target.value)}
        />
      </FormGroup>

      <FormGroup>
        <label htmlFor="password">Senha</label>
        <div className="flex">
          <DefaultInput
            placeholder="Digite sua senha"
            type={showPassword ? "text" : "password"}
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
          {showPassword ? (
            <VisibilityOff
              className="toggle-password"
              onClick={togglePasswordVisibility}
              sx={{
                color: theme.text,
              }}
            />
          ) : (
            <Visibility
              className="toggle-password"
              onClick={togglePasswordVisibility}
              sx={{
                color: theme.text,
              }}
            />
          )}
        </div>
      </FormGroup>

      <Button
        type="submit"
        variant="contained"
        disabled={isLoading}
        onClick={handleLogin}
      >
        {isLoading ? "Carregando..." : "Entrar"}
      </Button>
    </FormContainer>
  );
};
