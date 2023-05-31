import { Component, OnInit } from '@angular/core';
import { LoginService } from '../../services/login_service';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {
  username: string = '';
  password: string = '';
  loginError: string | null = null;

  constructor(private loginService: LoginService) { }

  ngOnInit() {
  }

  login()
  {
    this.loginService.login(this.username, this.password).subscribe(
      (response) => {
        console.log(response);
      },
      (error) => {
        this.loginError = error.message;
        console.log(error);
      }
    )
  }
}
