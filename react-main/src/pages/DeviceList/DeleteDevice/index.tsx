import { useForm} from "react-hook-form";
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
import { DeviceFormData, deviceSchema } from "./schema";
import DeviceService from "../../../app/services/devices";
import { DeviceProps } from "./types";
import { useEffect, useState } from "react";

export const DeleteDevice = ({ open, onClose, onSubmitted, deviceCode }: DeviceProps) => {
  const { handleSubmit, setValue } = useForm<DeviceFormData>({
    resolver: zodResolver(deviceSchema),
  });

  const [device, setDevice] = useState<DeviceFormData | null>(null);

  useEffect(() => {
    if (open) {
      const fetchDevice = async () => {
        if (!deviceCode) return;
        try {
          const response = await DeviceService.getDeviceByCode(deviceCode);
          if (response) {
            setDevice(response);
            setValue("device_code", response.device_code);
          }
        } catch (error) {
          console.error(error);
        }
      };
  
      fetchDevice();
    }
  }, [open, deviceCode, setValue]);
  

  const handleDeleteDevice = async () => {
    if (!deviceCode) {
      console.error("Código do dispositivo não fornecido.");
      return; 
    }
  
    try {
      await DeviceService.deleteDevice(deviceCode); 
      onSubmitted && onSubmitted(); // Chama a função de callback
      onClose(); 
    } catch (error) {
      console.error("Erro ao deletar dispositivo:", error);
    }
  };

  return (
    <CustomModal open={open} onClose={onClose} size="sm">
      <ModalHeader>
        <h2>Deletar dispositivo: {device?.device_code}</h2>
        <IconButton onClick={onClose}>
          <Close />
        </IconButton>
      </ModalHeader>
      <DefaultForm onSubmit={handleSubmit(() => {})}>
        <ModalContent>
          <label>Tem certeza que deseja deletar o dispositivo {device?.device_code}?</label>
        </ModalContent>
        <ModalFooter>
          <Button type="button" variant="contained" color="error" onClick={handleDeleteDevice}>
            Deletar
          </Button>
        </ModalFooter>
      </DefaultForm>
    </CustomModal>
  );
};
