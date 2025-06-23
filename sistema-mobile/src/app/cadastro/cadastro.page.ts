import { Component } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { IonContent, IonHeader, IonToolbar, IonTitle, IonButtons, IonBackButton, IonList, IonItem, IonInput, IonButton, LoadingController, NavController, ToastController } from '@ionic/angular/standalone';
import { CommonModule } from '@angular/common';
import { Storage } from '@ionic/storage-angular';
import { Usuario } from '../home/usuario.model';

@Component({
  selector: 'app-cadastro',
  templateUrl: 'cadastro.page.html',
  styleUrls: ['cadastro.page.scss'],
  imports: [IonContent, IonHeader, IonToolbar, IonTitle, IonButtons, IonBackButton, IonList, IonItem, IonInput, IonButton, FormsModule, CommonModule],
  standalone: true,
  providers: [Storage],
})
export class CadastroPage {
  public instancia: { username: string; email: string; password: string; confirmar_senha: string } = {
    username: '',
    email: '',
    password: '',
    confirmar_senha: '',
  };

  constructor(
    public controle_carregamento: LoadingController,
    public controle_navegacao: NavController,
    public controle_toast: ToastController,
    private storage: Storage
  ) {}

  async cadastrarUsuario() {
    if (this.instancia.password !== this.instancia.confirmar_senha) {
      await this.apresenta_mensagem('As senhas não coincidem.');
      return;
    }

    const loading = await this.controle_carregamento.create({ message: 'Cadastrando...', duration: 15000 });
    await loading.present();

    const options: HttpOptions = {
      headers: { 'Content-Type': 'application/json' },
      url: 'http://127.0.0.1:8000/cadastro-api/',
      data: {
        username: this.instancia.username,
        email: this.instancia.email,
        password: this.instancia.password,
        confirmar_senha: this.instancia.confirmar_senha,
      },
    };

    try {
      const resposta: HttpResponse = await CapacitorHttp.post(options);
      if (resposta.status === 201) {
        const userData: Usuario = {
          id: resposta.data.id,
          username: resposta.data.username,
          email: resposta.data.email,
          token: resposta.data.token,
          nome: '',
          perfil_id: 0,
          freelancer_id: 0,
        };
        await this.storage.create();
        await this.storage.set('usuario', userData);
        loading.dismiss();
        await this.apresenta_mensagem('Cadastro realizado com sucesso!', 'success');
        this.controle_navegacao.navigateBack('/home');
      } else {
        loading.dismiss();
        const errorMsg = resposta.data?.detail || `Falha ao cadastrar: código ${resposta.status}`;
        await this.apresenta_mensagem(errorMsg);
        console.error('Erro resposta:', resposta.data);
      }
    } catch (erro: any) {
      console.error('Erro ao cadastrar:', erro);
      loading.dismiss();
      const errorMsg = erro?.data?.detail || `Erro: ${erro?.status || 'Desconhecido'}`;
      await this.apresenta_mensagem(errorMsg);
    }
  }

  navegarParaLogin() {
    this.controle_navegacao.navigateBack('/home');
  }

  async apresenta_mensagem(texto: string, cor: string = 'danger') {
    const mensagem = await this.controle_toast.create({
      message: texto,
      cssClass: 'ion-text-center',
      duration: 2000,
      color: cor,
    });
    await mensagem.present();
  }
}