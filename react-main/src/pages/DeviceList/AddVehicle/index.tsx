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
import { VehicleFormData, vehicleSchema } from "./schema";
import VehicleService from "../../../app/services/vehicle";

interface AddVehicleProps {
  open: boolean;
  onClose: () => void;
  onSubmitted?: () => void;
}

export const AddVehicle = ({ open, onClose, onSubmitted }: AddVehicleProps) => {
  const { control, handleSubmit } = useForm<VehicleFormData>({
    resolver: zodResolver(vehicleSchema),
  });

  const onSubmit = async (data: VehicleFormData) => {
    try {
      await VehicleService.postVehicle(data);
      onSubmitted && onSubmitted();
      onClose();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <CustomModal open={open} onClose={onClose} size="sm">
      <ModalHeader>
        <h2>Adicionar Veículo</h2>
        <IconButton onClick={onClose}>
          <Close />
        </IconButton>
      </ModalHeader>
      <DefaultForm onSubmit={handleSubmit(onSubmit)}>
        <ModalContent>
          <FormGroup>
            <label htmlFor="model">Modelo</label>
            <Controller
              name="model"
              control={control}
              defaultValue=""
              render={({ field }) => (
                <DefaultInput
                  {...field}
                  placeholder="Digite o modelo do veículo"
                  type="text"
                />
              )}
            />
          </FormGroup>
          <FormGroup>
            <label htmlFor="manufacturer">Fabricante</label>
            <Controller
              name="manufacturer"
              control={control}
              defaultValue=""
              render={({ field }) => (
                <DefaultInput
                  {...field}
                  placeholder="Digite o fabricante do veículo"
                  type="text"
                />
              )}
            />
          </FormGroup>
          <FormGroup>
            <label htmlFor="manufacture_year">Ano de Fabricação</label>
            <Controller
              name="manufacture_year"
              control={control}
              defaultValue={new Date().getFullYear()}
              render={({ field }) => (
                <DefaultInput
                  {...field}
                  placeholder="Digite o ano de fabricação do veículo"
                  type="number"
                />
              )}
            />
          </FormGroup>
          <FormGroup>
            <label htmlFor="engine_type">Tipo de Motor</label>
            <Controller
              name="engine_type"
              control={control}
              defaultValue=""
              render={({ field }) => (
                <DefaultInput
                  {...field}
                  placeholder="Digite o tipo de motor"
                  type="text"
                />
              )}
            />
          </FormGroup>
          <FormGroup>
            <label htmlFor="number_of_engines">Número de Motores</label>
            <Controller
              name="number_of_engines"
              control={control}
              defaultValue={1}
              render={({ field }) => (
                <DefaultInput
                  {...field}
                  placeholder="Digite o número de motores"
                  type="number"
                />
              )}
            />
          </FormGroup>
        </ModalContent>
        <ModalFooter>
          <Button type="submit" variant="contained">
            Adicionar
          </Button>
        </ModalFooter>
      </DefaultForm>
    </CustomModal>
  );
};
