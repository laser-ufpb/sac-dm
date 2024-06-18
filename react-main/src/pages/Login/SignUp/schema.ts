import * as z from "zod";

export const userSchema = z.object({
  username: z.string().nonempty("Nome de usuário é obrigatório"),
  email: z.string().email("Email inválido"),
  full_name: z.string().nonempty("Nome completo é obrigatório"),
  hashed_password: z.string().min(6, "Senha deve ter pelo menos 6 caracteres"),
  disabled: z.boolean(),
});

export type UserFormData = z.infer<typeof userSchema>;
