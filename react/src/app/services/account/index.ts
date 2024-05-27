import { api } from "..";

class AccountService {
  async getAccount(username: string) {
    try {
      const response = await api.get("/user/" + username);
      return response.data;
    } catch (error) {
      console.error(error);
    }
  }
}

const accountService = new AccountService();
export default accountService;
