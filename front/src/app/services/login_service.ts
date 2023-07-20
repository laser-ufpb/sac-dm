import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable } from "rxjs";
import { environment } from "src/environments/environment";

@Injectable({
    providedIn:'root',
})
export class LoginService
{
    private apiURL: string = environment.baseUrl + "/token";

    constructor (private httpClient: HttpClient) {}

    login (username: string, password: string): Observable<any>
    {
        const headers = new HttpHeaders({ 'Content-Type': 'application/x-www-form-urlencoded' });
        const body = new URLSearchParams();
        body.set('username', username);
        body.set('password', password);        
        return this.httpClient.post<any>(this.apiURL, body.toString(), { headers: headers });
    }
}