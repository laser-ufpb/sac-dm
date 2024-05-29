import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class DeviceService {

  private apiURL: string = environment.baseUrl + "/device";

  constructor(private httpClient: HttpClient) { }

  deviceList(): Observable<any> {
    return this.httpClient.get<any>(this.apiURL);
  }
}
