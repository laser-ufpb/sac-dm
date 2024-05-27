import { Dialog } from "@mui/material";
import { ModalProps } from "./types";
import { ModalContainer } from "./styles";

export const CustomModal = ({
  open,
  onClose,
  children,
  size = "md",
}: ModalProps) => {
  if (!open) return null;

  const sizes = {
    xsm: "350px",
    sm: "400px",
    md: "600px",
    lg: "800px",
    xl: "1000px",
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      sx={{
        "& .MuiDialog-paper": {
          width: "100%",
          maxWidth: `${sizes[size]}`,
          borderRadius: "8px",
          border: "none",
          backgroundColor: "transparent",
        },
      }}
    >
      <ModalContainer>{children}</ModalContainer>
    </Dialog>
  );
};
