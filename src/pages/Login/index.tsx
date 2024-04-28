import { useContext, useState } from "react";
import { FormContainer, HeaderContent } from "./styles";
import { AuthContext } from "../../app/contexts/AuthContext";
import { FormGroup } from "../../components/forms/FormGroup";
import { DefaultInput } from "../../components/forms/DefaultInput";
import { Visibility, VisibilityOff } from "@mui/icons-material";
import { theme } from "../../styles/theme";
import { Button } from "@mui/material";
import { CustomModal } from "../../components/CustomModal";

export const Login = () => {
  const [isLoading, setIsLoading] = useState(false);
  const { isLoginModalVisible, hideLoginModal, signIn } =
    useContext(AuthContext);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const handleLogin = async () => {
    setIsLoading(true);
    try {
      await signIn(email, password);
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
    <CustomModal open={isLoginModalVisible} onClose={hideLoginModal} size="sm">
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
          <label htmlFor="email">E-mail</label>
          <DefaultInput
            placeholder="Digite seu e-mail"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
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
    </CustomModal>
  );
};
