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
import {
  DefaultInput,
  DefaultSelect,
} from "../../../components/forms/DefaultInput";
import { DeviceFormData, deviceSchema } from "./schema";
import DeviceService from "../../../app/services/devices";
import vehicleService from "../../../app/services/vehicle";
import { AddDeviceProps } from "./types";
import { useEffect, useState } from "react";

interface Vehicle {
  id: number;
  model: string;
  manufacturer: string;
}

export const AddDevice = ({ open, onClose, onSubmitted }: AddDeviceProps) => {
  const { control, handleSubmit, setValue } = useForm<DeviceFormData>({
    resolver: zodResolver(deviceSchema),
  });

  const [vehicles, setVehicles] = useState<Vehicle[]>([]);

  useEffect(() => {
    const fetchVehicles = async () => {
      try {
        const response = await vehicleService.getVehicles();
        setVehicles(response);
      } catch (error) {
        console.error(error);
      }
    };

    fetchVehicles();
  }, []);

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
          <FormGroup>
            <label htmlFor="vehicle_id">Veículo</label>
            <Controller
              name="vehicle_id"
              control={control}
              defaultValue={0}
              render={({ field }) => (
                <DefaultSelect
                  {...field}
                  onChange={(e) =>
                    setValue("vehicle_id", Number(e.target.value))
                  }
                >
                  <option value="" disabled>
                    Selecione um veículo
                  </option>
                  {vehicles.map((vehicle) => (
                    <option key={vehicle.id} value={vehicle.id}>
                      {vehicle.model} - {vehicle.manufacturer}
                    </option>
                  ))}
                </DefaultSelect>
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
