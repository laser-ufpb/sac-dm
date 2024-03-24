import { z } from "zod";

export const deviceSchema = z.object({
  device_code: z.string().min(1, "O código do dispositivo é obrigatório"),
});

export type DeviceFormData = z.infer<typeof deviceSchema>;
