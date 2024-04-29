import { useCallback, useContext, useEffect, useState } from "react";
import accountService from "../../app/services/account";
import { AuthContext } from "../../app/contexts/AuthContext";
import { CircularProgress } from "@mui/material";
import { UserProps } from "./types";
import { Container, InfoCard } from "./styles";

export const Account = () => {
  const { user } = useContext(AuthContext);
  const [isLoading, setIsLoading] = useState(true);
  const [userData, setUserData] = useState<UserProps | null>(null);

  const getUser = useCallback(async () => {
    if (!user) return;

    try {
      const response = await accountService.getAccount("jvpedrosa"); //TODO
      setUserData(response);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }, [user]);

  useEffect(() => {
    getUser();
  }, [getUser]);

  return (
    <>
      {isLoading ? (
        <CircularProgress />
      ) : (
        <Container>
          <h1>Olá {userData?.full_name}</h1>

          <InfoCard>
            <h2>Dados cadastrados:</h2>
            <p>Email: {userData?.email}</p>
            <p>Username: {userData?.username}</p>
          </InfoCard>
        </Container>
      )}
    </>
  );
};
