import { z } from "zod";

export const deviceSchema = z.object({
  device_code: z
    .string()
    .min(1, "Device code is required")
    .max(100, "Device code can't exceed 100 characters"),
});

export type DeviceFormData = z.infer<typeof deviceSchema>;
