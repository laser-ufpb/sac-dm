import { Component, OnInit } from '@angular/core';
import { DeviceService } from 'src/app/services/device.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.page.html',
  styleUrls: ['./dashboard.page.scss'],
})
export class DashboardPage implements OnInit {

  devices: any[] = [];

  constructor(private deviceService: DeviceService) { }

  ngOnInit() {
    this.deviceService.deviceList().subscribe(res => {
      this.devices = res;

      // Adição do atributo "status" para cada dispositivo
      this.devices.forEach(device => {
        device["status"] = "off";
      });
      this.devices[0]["status"] = "on";
      this.devices[1]["status"] = "on";
      this.devices[2]["status"] = "on";
      this.devices[3]["status"] = "on";
      this.devices[7]["status"] = "on";
      this.devices[5]["status"] = "warning";
      this.devices[8]["status"] = "warning";

      console.log(this.devices[0]["status"]);
      console.log(res);
    }, error => {
      console.log(error);
    })
  }

}
