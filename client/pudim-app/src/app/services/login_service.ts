import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";

@Injectable({
    providedIn:'root',
})
export class LoginService
{
    private apiURL = 'http://localhost:8100/login';

    constructor (private httpClient: HttpClient) {}

    login (username: string, password: string): Observable<any>
    {
        const login_data = { username, password };
        return this.httpClient.post<any>(this.apiURL, login_data);
    }
}