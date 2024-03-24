import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button, IconButton } from "@mui/material";
import { CustomModal } from "../../../../components/CustomModal";
import {
  ModalContent,
  ModalFooter,
  ModalHeader,
} from "../../../../components/CustomModal/styles";
import { ModalProps } from "../../../../components/CustomModal/types";
import { Close } from "@mui/icons-material";
import { DefaultForm } from "../../../../components/forms/DefaultForm";
import { FormGroup } from "../../../../components/forms/FormGroup";
import { DefaultInput } from "../../../../components/forms/DefaultInput";
import { DeviceFormData, deviceSchema } from "./schema";
import DeviceService from "../../../../app/services/devices";
import { AddDeviceProps } from "./types";

export const AddDevice = ({ open, onClose, onSubmitted }: AddDeviceProps) => {
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<DeviceFormData>({
    resolver: zodResolver(deviceSchema),
  });

  const onSubmit = async (data: DeviceFormData) => {
    try {
      await DeviceService.postDevices(data);
      onSubmitted && onSubmitted();
      onClose();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <CustomModal open={open} onClose={onClose} size="sm">
      <ModalHeader>
        <h2>Adicionar Dispositivo</h2>
        <IconButton onClick={onClose}>
          <Close />
        </IconButton>
      </ModalHeader>
      <DefaultForm onSubmit={handleSubmit(onSubmit)}>
        <ModalContent>
          <FormGroup>
            <label htmlFor="device_code">Código do Dispositivo</label>
            <Controller
              name="device_code"
              control={control}
              defaultValue=""
              render={({ field }) => (
                <DefaultInput
                  {...field}
                  placeholder="Digite o código do dispositivo"
                  type="text"
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
