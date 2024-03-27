import { useEffect, useState } from "react";
import { Container } from "./styles";
import sacDmService from "../../app/services/sac_dm";
import { SacDmProps } from "./types";
import { CircularProgress } from "@mui/material";

export const SacDm = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [sacDm, setSacDm] = useState<SacDmProps[]>([]);

  useEffect(() => {
    loadSacDm();
  }, []);

  const loadSacDm = async () => {
    setIsLoading(true);
    try {
      const response = await sacDmService.getSacDm();
      setSacDm(response);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container>
      <h1>SacDm</h1>
      {isLoading ? (
        <CircularProgress />
      ) : (
        <ul>
          {sacDm.map((item) => (
            <li key={item.id}>{item.id}</li>
          ))}
        </ul>
      )}
    </Container>
  );
};
