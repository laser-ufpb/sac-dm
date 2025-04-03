import { z } from "zod";

export const deviceSchema = z.object({
  vehicle_id: z.number().int().positive("Veículo é obrigatório"),
});

export type DeviceFormData = z.infer<typeof deviceSchema>;
