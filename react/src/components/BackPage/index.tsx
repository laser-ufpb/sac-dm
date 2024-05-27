import { ArrowBack } from "@mui/icons-material";
import { Button } from "@mui/material";

export const BackPage = () => {
  const goBack = () => {
    window.history.back();
  };
  return (
    <Button variant="outlined" startIcon={<ArrowBack />} onClick={goBack}>
      Voltar
    </Button>
  );
};
