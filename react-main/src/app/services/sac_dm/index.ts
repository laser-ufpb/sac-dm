import { api } from "..";

class SacDmService {
  async getSacDm(limit?: number) {
    try {
      const response = await api.get("/sac_dm", {
        params: {
          limit: limit || 1000,
        },
      });
      return response.data.reverse();
    } catch (error) {
      console.error(error);
    }
  }

  async getSacDmByDeviceId(id: number, limit?: number) {
    try {
      const response = await api.get(`/sac_dm_by_device_id`, {
        params: {
          device_id: id,
          limit: limit || 1000,
        },
      });
      return response.data.reverse();
    } catch (error) {
      console.error(error);
    }
  }

  async postSacDm() {
    try {
      const value = Math.floor(Math.random() * 11);
      const timestamp = new Date().toISOString();

      const response = await api.post("/sac_dm", [
        {
          device_id: 1,
          value: value,
          timestamp: timestamp,
        },
      ]);
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  }
}

const sacDmService = new SacDmService();
export default sacDmService;
