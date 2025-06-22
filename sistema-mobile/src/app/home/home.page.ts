import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Storage } from '@ionic/storage-angular';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { IonContent, IonHeader, IonToolbar, IonTitle, IonButtons, IonMenuButton, IonList, IonItem, IonInput, IonButton, LoadingController, NavController, ToastController } from '@ionic/angular/standalone';
import { Usuario } from './usuario.model';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  imports: [IonContent, IonHeader, IonToolbar, IonTitle, IonButtons, IonMenuButton, IonList, IonItem, IonInput, IonButton, FormsModule, CommonModule],
  providers: [Storage],
  standalone: true,
})
export class HomePage implements OnInit {
  constructor(
    public controle_carregamento: LoadingController,
    public controle_navegacao: NavController,
    public controle_toast: ToastController,
    public storage: Storage
  ) {}

  async ngOnInit() {
    await this.storage.create();
    const usuario = await this.storage.get('usuario');
    if (usuario) {
      this.controle_navegacao.navigateRoot('/freelancer');
    }
  }

  public instancia: { username: string; password: string } = {
    username: '',
    password: '',
  };

  async autenticarUsuario() {
    const loading = await this.controle_carregamento.create({ message: 'Autenticando...', duration: 15000 });
    await loading.present();

    const options: HttpOptions = {
      headers: { 'Content-Type': 'application/json' },
      url: 'http://127.0.0.1:8000/autenticacao-api/',
      data: this.instancia,
    };

    try {
      const resposta: HttpResponse = await CapacitorHttp.post(options);
      if (resposta.status === 200) {
        let usuario: Usuario = Object.assign(new Usuario(), resposta.data);
        await this.storage.set('usuario', usuario);
        loading.dismiss();
        this.controle_navegacao.navigateRoot('/freelancer');
      } else {
        loading.dismiss();
        await this.apresenta_mensagem(`Falha ao autenticar: código ${resposta.status}`);
      }
    } catch (erro: any) {
      console.error(erro);
      loading.dismiss();
      await this.apresenta_mensagem(`Erro: ${erro?.status || 'Desconhecido'}`);
    }
  }

  navegarParaCadastro() {
    this.controle_navegacao.navigateForward('/cadastro');
  }

  async apresenta_mensagem(texto: string) {
    const mensagem = await this.controle_toast.create({
      message: texto,
      cssClass: 'ion-text-center',
      duration: 2000,
      color: 'danger',
    });
    await mensagem.present();
  }
}