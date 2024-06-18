import { useState, useContext } from "react";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button, IconButton } from "@mui/material";
import { CustomModal } from "../../../components/CustomModal";
import {
  ModalContent,
  ModalFooter,
  ModalHeader,
} from "../../../components/CustomModal/styles";
import { Close } from "@mui/icons-material";
import { DefaultForm } from "../../../components/forms/DefaultForm";
import { FormGroup } from "../../../components/forms/FormGroup";
import { DefaultInput } from "../../../components/forms/DefaultInput";
import { userSchema } from "./schema";
import { AuthContext } from "../../../app/contexts/AuthContext";
import { UserPayload } from "../../../app/services/login/types";

interface SignUpProps {
  open: boolean;
  onClose: () => void;
  toggleForms: () => void;
}

export const SignUp = ({ open, onClose, toggleForms }: SignUpProps) => {
  const { signUp } = useContext(AuthContext);
  const { control, handleSubmit } = useForm<UserPayload>({
    resolver: zodResolver(userSchema),
  });

  const [isLoading, setIsLoading] = useState(false);

  const onSubmit = async (data: UserPayload) => {
    setIsLoading(true);
    try {
      await signUp(data);
      onClose();
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <CustomModal open={open} onClose={onClose} size="sm">
      <ModalHeader>
        <h2>Cadastrar Usuário</h2>
        <IconButton onClick={onClose}>
          <Close />
        </IconButton>
      </ModalHeader>
      <DefaultForm onSubmit={handleSubmit(onSubmit)}>
        <ModalContent>
          <FormGroup>
            <label htmlFor="username">Nome de Usuário</label>
            <Controller
              name="username"
              control={control}
              defaultValue=""
              render={({ field }) => (
                <DefaultInput
                  {...field}
                  placeholder="Digite o nome de usuário"
                  type="text"
                />
              )}
            />
          </FormGroup>
          <FormGroup>
            <label htmlFor="email">E-mail</label>
            <Controller
              name="email"
              control={control}
              defaultValue=""
              render={({ field }) => (
                <DefaultInput
                  {...field}
                  placeholder="Digite seu e-mail"
                  type="email"
                />
              )}
            />
          </FormGroup>
          <FormGroup>
            <label htmlFor="full_name">Nome Completo</label>
            <Controller
              name="full_name"
              control={control}
              defaultValue=""
              render={({ field }) => (
                <DefaultInput
                  {...field}
                  placeholder="Digite seu nome completo"
                  type="text"
                />
              )}
            />
          </FormGroup>
          <FormGroup>
            <label htmlFor="hashed_password">Senha</label>
            <Controller
              name="hashed_password"
              control={control}
              defaultValue=""
              render={({ field }) => (
                <DefaultInput
                  {...field}
                  placeholder="Digite sua senha"
                  type="password"
                />
              )}
            />
          </FormGroup>
        </ModalContent>
        <ModalFooter>
          <Button onClick={toggleForms} style={{ marginTop: "10px" }}>
            Voltar
          </Button>
          <Button type="submit" variant="contained" disabled={isLoading}>
            {isLoading ? "Carregando..." : "Cadastrar"}
          </Button>
        </ModalFooter>
      </DefaultForm>
    </CustomModal>
  );
};
