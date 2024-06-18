import { z } from "zod";

export const deviceSchema = z.object({
  device_code: z
    .string()
    .min(1, "Código do dispositivo é obrigatório")
    .max(100, "Código do dispositivo deve ter no máximo 100 caracteres"),
  vehicle_id: z.number().int().positive("Veículo é obrigatório"),
});

export type DeviceFormData = z.infer<typeof deviceSchema>;
