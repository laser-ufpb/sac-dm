import { createContext, PropsWithChildren, useMemo, useState } from "react";
import { AuthContextData, CreateUserPayload, UserProps } from "./types";
import { useNavigate } from "react-router";
import { api } from "../../services";

export const AuthContext = createContext({} as AuthContextData);

export const AuthProvider = ({ children }: PropsWithChildren) => {
  const [isLoginModalVisible, setIsLoginModalVisible] = useState(false);
  const [user, setUser] = useState<UserProps | null>(() => {
    const user = JSON.parse(localStorage.getItem("user") || "null");

    return user;
  });

  const [token] = useState<string>(() => {
    const token = localStorage.getItem("token");

    return token || "";
  });

  const navigate = useNavigate();

  const showLoginModal = () => setIsLoginModalVisible(true);
  const hideLoginModal = () => setIsLoginModalVisible(false);

  async function signIn(username: string, password: string) {
    try {
      const response = await api.post("/login", {
        username,
        password,
      });

      const { token, user } = response.data;

      localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(user));

      setUser(user);
    } catch (error) {
      console.log(error);
    }
  }

  function signOut() {
    localStorage.removeItem("token");
    localStorage.removeItem("user");

    setUser(null);

    navigate("/login");
  }

  async function signUp(user: CreateUserPayload) {
    try {
      const response = await api.post("/user", {
        ...user,
        status_id: 0,
      });
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  }

  async function updateUser(user: UserProps) {
    try {
      const response = await api.put(`/user/${user.id}`, user);
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  }

  const memoizedValues = useMemo(
    () => ({
      user,
      setUser,
      signIn,
      signOut,
      signUp,
      updateUser,
      isLoginModalVisible,
      showLoginModal,
      hideLoginModal,
    }),
    [
      user,
      setUser,
      signIn,
      signOut,
      signUp,
      updateUser,
      isLoginModalVisible,
      showLoginModal,
      hideLoginModal,
    ]
  );

  return (
    <AuthContext.Provider value={memoizedValues}>
      {children}
    </AuthContext.Provider>
  );
};
