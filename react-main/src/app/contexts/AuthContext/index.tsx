import {
  createContext,
  PropsWithChildren,
  useMemo,
  useState,
  useCallback,
} from "react";
import { AuthContextData, CreateUserPayload, UserProps } from "./types";
import { useNavigate } from "react-router";
import { api } from "../../services";

export const AuthContext = createContext({} as AuthContextData);

export const AuthProvider = ({ children }: PropsWithChildren) => {
  const [isLoginModalVisible, setIsLoginModalVisible] = useState(false);
  const [user, setUser] = useState<UserProps | null>(() => {
    return JSON.parse(localStorage.getItem("user") || "null");
  });

  const navigate = useNavigate();

  const showLoginModal = useCallback(() => setIsLoginModalVisible(true), []);
  const hideLoginModal = useCallback(() => setIsLoginModalVisible(false), []);

  const signIn = useCallback(async (username: string, password: string) => {
    try {
      // const response = await api.post("/login", {
      //   username,
      //   password,
      // });
      // const { user } = response.data;

      // localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(username));

      // setUser(user);
    } catch (error) {
      console.error(error);
    }
  }, []);

  const signOut = useCallback(() => {
    localStorage.removeItem("user");
    localStorage.removeItem("token");
    setUser(null);
    navigate("/login");
  }, [navigate]);

  const signUp = useCallback(
    async (user: CreateUserPayload) => {
      try {
        await api.post("/user", user);
        await signIn(user.username, user.hashed_password);
      } catch (error) {
        console.error(error);
      }
    },
    [signIn]
  );

  const updateUser = useCallback(async (user: UserProps) => {
    try {
      const response = await api.put(`/user/${user.id}`, user);
      console.log(response);
    } catch (error) {
      console.error(error);
    }
  }, []);

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
