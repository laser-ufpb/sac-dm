import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "src/environments/environment";

@Injectable({
    providedIn:'root',
})
export class LoginService
{
    private apiURL: string = environment.baseUrl + "/login";

    constructor (private httpClient: HttpClient) {}

    login (username: string, password: string): Observable<any>
    {        
        return this.httpClient.post<any>(this.apiURL, { "username": username, "password": password });
    }
}