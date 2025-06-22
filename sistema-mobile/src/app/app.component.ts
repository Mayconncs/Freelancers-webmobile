import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import {
  IonApp, IonMenu, IonHeader, IonToolbar, IonTitle, IonContent, IonList, IonMenuToggle, IonItem, IonIcon,
  IonLabel, IonRouterOutlet, ToastController
} from '@ionic/angular/standalone';
import { Storage } from '@ionic/storage-angular';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { NavController } from '@ionic/angular';
import { Usuario } from './home/usuario.model';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss'],
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    IonApp, IonMenu, IonHeader, IonToolbar, IonTitle, IonContent, IonList, IonMenuToggle, IonItem, IonIcon,
    IonLabel, IonRouterOutlet
  ],
  providers: [Storage, ToastController, NavController]
})
export class AppComponent implements OnInit {
  public isAuthenticated: boolean = false;
  public usuario: Usuario = new Usuario();
  public profileId: number | null = null;

  constructor(
    private storage: Storage,
    private toastController: ToastController,
    private navController: NavController
  ) {}

  async ngOnInit() {
    await this.storage.create();
    const registro = await this.storage.get('usuario');
    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro);
      this.isAuthenticated = true;
      await this.fetchUserProfile();
    }
  }

  async fetchUserProfile() {
    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${this.usuario.token}`,
      },
      url: 'http://127.0.0.1:8000/freelancer/api/',
    };

    try {
      const resposta: HttpResponse = await CapacitorHttp.get(options);
      if (resposta.status === 200) {
        const profiles = resposta.data;
        const userProfile = profiles.find((profile: any) => profile.usuario === this.usuario.id);
        if (userProfile) {
          this.profileId = userProfile.id;
        } else {
          console.warn('Perfil do usuário não encontrado.');
        }
      } else {
        console.error('Erro ao buscar perfil:', resposta.status);
      }
    } catch (erro: any) {
      console.error('Erro ao buscar perfil:', erro);
    }
  }

  async navigateToMyProfile() {
    if (!this.isAuthenticated) {
      await this.presentToast('Faça login para ver seu perfil.');
      this.navController.navigateRoot('/home');
      return;
    }

    if (this.profileId) {
      this.navController.navigateForward(`/detalhar/${this.profileId}`);
    } else {
      await this.presentToast('Você ainda não possui um perfil. Crie um agora.');
      this.navController.navigateForward('/perfil');
    }
  }

  async logout() {
    await this.storage.remove('usuario');
    this.isAuthenticated = false;
    this.profileId = null;
    await this.presentToast('Logout realizado com sucesso!', 'success');
    this.navController.navigateRoot('/home');
  }

  async presentToast(message: string, color: string = 'danger') {
    const toast = await this.toastController.create({
      message,
      cssClass: 'ion-text-center',
      duration: 2000,
      color,
    });
    await toast.present();
  }
}