import { useContext, useState } from "react";
import { CustomModal } from "../../components/CustomModal";
import { SignIn } from "./SignIn";
import { SignUp } from "./SignUp";
import { AuthContext } from "../../app/contexts/AuthContext";
import { Button } from "@mui/material";

export const Login = () => {
  const { isLoginModalVisible, hideLoginModal } = useContext(AuthContext);
  const [showSignIn, setShowSignIn] = useState(true);

  const toggleForms = () => {
    setShowSignIn(!showSignIn);
  };

  return (
    <CustomModal open={isLoginModalVisible} onClose={hideLoginModal} size="sm">
      {showSignIn ? (
        <>
          <SignIn />
          <Button onClick={toggleForms} style={{ marginTop: "10px" }}>
            Não tem uma conta? Cadastre-se
          </Button>
        </>
      ) : (
        <>
          <SignUp
            open={!showSignIn}
            onClose={hideLoginModal}
            toggleForms={toggleForms}
          />
          <Button onClick={toggleForms} style={{ marginTop: "10px" }}>
            Já tem uma conta? Entre aqui
          </Button>
        </>
      )}
    </CustomModal>
  );
};
