import { api } from "..";
import { LoginPayload, UserPayload } from "./types";

class LoginService {
  async createUser(payload: UserPayload) {
    try {
      const response = await api.post("/user", payload);
      return response.data;
    } catch (error) {
      console.error(error);
    }
  }

  async login(payload: LoginPayload) {
    try {
      const response = await api.post("/login", payload);
      return response.data;
    } catch (error) {
      console.error(error);
    }
  }
}

const loginService = new LoginService();
export default loginService;
