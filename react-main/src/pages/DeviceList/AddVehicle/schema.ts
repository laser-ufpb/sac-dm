import { z } from "zod";

export const vehicleSchema = z.object({
  model: z.string().min(1, "O modelo é obrigatório"),
  manufacturer: z.string().min(1, "O fabricante é obrigatório"),
  manufacture_year: z.number().int().min(1900, "Ano inválido"),
  engine_type: z.string().min(1, "O tipo de motor é obrigatório"),
  number_of_engines: z.number().int().min(1, "Número de motores inválido"),
});

export type VehicleFormData = z.infer<typeof vehicleSchema>;
