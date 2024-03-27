import { api } from "..";

class SacDmService {
  async getSacDm() {
    try {
      const response = await api.get("/sac_dm");
      return response.data;
    } catch (error) {
      console.error(error);
    }
  }
}

const sacDmService = new SacDmService();
export default sacDmService;
