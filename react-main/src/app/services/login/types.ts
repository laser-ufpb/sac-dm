export interface UserPayload {
  username: string;
  email: string;
  full_name: string;
  disabled: boolean;
  hashed_password: string;
}

export interface LoginPayload {
  username: string;
  password: string;
}
