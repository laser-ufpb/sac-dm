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

  async getSacDmByDeviceId(id: string) {
    try {
      const response = await api.get(`/sac_dm_by_device_id`, {
        params: {
          device_id: id,
        },
      });
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  }
}

const sacDmService = new SacDmService();
export default sacDmService;
