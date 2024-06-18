import { useCallback, useEffect, useState } from "react";
import accountService from "../../app/services/account";
import { Button, CircularProgress } from "@mui/material";
import { UserProps } from "./types";
import {
  AccountDetails,
  Container,
  ExitButton,
  Header,
  InfoCard,
} from "./styles";
import { BackPage } from "../../components/BackPage";
import { ExitToApp } from "@mui/icons-material";

export const Account = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [userData, setUserData] = useState<UserProps | null>(null);

  const getUser = useCallback(async () => {
    const storedUser = localStorage.getItem("user");
    if (!storedUser) return;

    const parsedUser = JSON.parse(storedUser);
    try {
      const response = await accountService.getAccount(parsedUser);
      setUserData(response);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    localStorage.clear();
    window.location.reload();
  }, []);

  useEffect(() => {
    getUser();
  }, [getUser]);

  return (
    <Container>
      {isLoading ? (
        <CircularProgress />
      ) : (
        <>
          <Header>
            <BackPage />

            <h1>Minha Conta</h1>
          </Header>

          <AccountDetails>
            <img
              src="https://avatars.githubusercontent.com/u/14032497?v=4"
              alt="Avatar"
            />
            <h2>{userData?.full_name}</h2>
          </AccountDetails>

          <InfoCard>
            <h3>Dados pessoais</h3>
            <div>
              <strong>Nome:</strong>
              <p>{userData?.full_name}</p>
            </div>
            <div>
              <strong>Usuário:</strong>
              <p>{userData?.username}</p>
            </div>
            <div>
              <strong>Email:</strong>
              <p>{userData?.email}</p>
            </div>
          </InfoCard>

          <ExitButton>
            <Button
              variant="contained"
              color="error"
              startIcon={<ExitToApp />}
              onClick={logout}
            >
              Sair
            </Button>
          </ExitButton>
        </>
      )}
    </Container>
  );
};
