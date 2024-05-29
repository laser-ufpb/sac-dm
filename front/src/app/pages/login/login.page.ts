import { Component, OnInit } from '@angular/core';
import { NavController } from '@ionic/angular';
import { LoginService } from '../../services/login_service';
import { DashboardPage } from '../dashboard/dashboard.page';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {
  username: string = '';
  password: string = '';
  loginError: string | null = null;

  constructor(private loginService: LoginService, public navCtrl: NavController) { }

  ngOnInit() {
  }

  login()
  {
    this.loginService.login(this.username, this.password).subscribe(
      (response: any) => {
        this.loginError = null;
        this.navCtrl.navigateRoot('dashboard');
      },
      (error: any) => {
        this.loginError = error.error;
        console.log("erro: ", error);
      }
    )
  }
}
