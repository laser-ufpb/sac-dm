export interface AuthContextData {
  user: UserProps | null;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => void;
  signUp: (user: CreateUserPayload) => Promise<void>;
  setUser: (user: UserProps) => void;
  updateUser: (user: UserProps) => void;
  isLoginModalVisible: boolean;
  showLoginModal: () => void;
  hideLoginModal: () => void;
}

export interface UserProps {
  id?: number;
  username: string;
  password: string;
}

export interface CreateUserPayload {
  username: string;
  email: string;
  full_name: string;
  disabled: boolean;
  hashed_password: string;
}
