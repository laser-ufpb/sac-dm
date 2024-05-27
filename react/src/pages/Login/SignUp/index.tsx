import { useContext, useState } from "react";
import { FormContainer, HeaderContent } from "../styles";
import { AuthContext } from "../../../app/contexts/AuthContext";
import { FormGroup } from "../../../components/forms/FormGroup";
import { DefaultInput } from "../../../components/forms/DefaultInput";
import { Button } from "@mui/material";
import { Visibility, VisibilityOff } from "@mui/icons-material";
import { theme } from "../../../styles/theme";

export const SignUp = () => {
  const [isLoading, setIsLoading] = useState(false);
  const { signUp, hideLoginModal } = useContext(AuthContext);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [full_name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleSignUp = async () => {
    if (password !== confirmPassword) {
      alert("Senhas não coincidem");
      return;
    }
    setIsLoading(true);
    try {
      await signUp({
        username,
        email,
        full_name,
        disabled: false,
        hashed_password: password,
      });
    } catch (error) {
      console.error({ error });
    } finally {
      setIsLoading(false);
      hideLoginModal();
    }
  };

  return (
    <FormContainer>
      <HeaderContent>
        <h2>Cadastre-se</h2>
      </HeaderContent>

      <FormGroup>
        <label htmlFor="username">Usuário</label>
        <DefaultInput
          placeholder="Digite seu usuário"
          value={username}
          onChange={(event) => setUsername(event.target.value)}
        />
      </FormGroup>

      <FormGroup>
        <label htmlFor="email">E-mail</label>
        <DefaultInput
          placeholder="Digite seu e-mail"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />
      </FormGroup>

      <FormGroup>
        <label htmlFor="full_name">Nome completo</label>
        <DefaultInput
          placeholder="Digite seu nome completo"
          value={full_name}
          onChange={(event) => setName(event.target.value)}
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

      <FormGroup>
        <label htmlFor="confirmPassword">Confirme sua senha</label>
        <div className="flex">
          <DefaultInput
            placeholder="Confirme sua senha"
            type={showPassword ? "text" : "password"}
            value={confirmPassword}
            onChange={(event) => setConfirmPassword(event.target.value)}
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
        onClick={handleSignUp}
        disabled={isLoading}
        style={{ marginTop: "10px" }}
        variant="contained"
      >
        {isLoading ? "Carregando..." : "Cadastrar"}
      </Button>
    </FormContainer>
  );
};
