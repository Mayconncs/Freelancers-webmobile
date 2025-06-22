import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonBackButton, IonList, IonItem, IonLabel,
  IonIcon, IonButton, LoadingController, NavController, ToastController
} from '@ionic/angular/standalone';
import { Storage } from '@ionic/storage-angular';
import { Freelancer } from '../freelancer/freelancer.model';
import { Usuario } from '../home/usuario.model';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-detalhar',
  templateUrl: './detalhar.page.html',
  styleUrls: ['./detalhar.page.scss'],
  imports: [
    IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonBackButton, IonList, IonItem, IonLabel,
    IonIcon, IonButton, CommonModule,
  ],
  providers: [Storage],
})
export class DetalharPage implements OnInit {
  public usuario: Usuario = new Usuario();
  public freelancer: Freelancer = new Freelancer();

  constructor(
    public storage: Storage,
    public controle_toast: ToastController,
    public controle_navegacao: NavController,
    public controle_carregamento: LoadingController,
    private route: ActivatedRoute
  ) {}

  async ngOnInit() {
    await this.storage.create();
    const registro = await this.storage.get('usuario');
    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro);
      const id = this.route.snapshot.paramMap.get('id');
      if (id) {
        await this.carregarPerfil(parseInt(id));
      } else {
        await this.apresenta_mensagem('ID do perfil não fornecido.');
        this.controle_navegacao.navigateBack('/freelancer');
      }
    } else {
      await this.apresenta_mensagem('Usuário não autenticado.');
      this.controle_navegacao.navigateRoot('/home');
    }
  }

  async carregarPerfil(id: number) {
    const loading = await this.controle_carregamento.create({ message: 'Carregando perfil...', duration: 30000 });
    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${this.usuario.token}`,
      },
      url: `http://127.0.0.1:8000/freelancer/api/${id}/`,
    };

    try {
      const resposta: HttpResponse = await CapacitorHttp.get(options);
      if (resposta.status === 200) {
        this.freelancer = Object.assign(new Freelancer(), resposta.data);
        loading.dismiss();
      } else if (resposta.status === 404) {
        loading.dismiss();
        await this.apresenta_mensagem('Perfil não encontrado.');
        this.controle_navegacao.navigateBack('/freelancer');
      } else {
        loading.dismiss();
        await this.apresenta_mensagem(`Falha ao carregar perfil: código ${resposta.status}`);
      }
    } catch (erro: any) {
      console.error('Erro ao carregar perfil:', erro);
      loading.dismiss();
      await this.apresenta_mensagem(`Erro: ${erro?.status || 'Desconhecido'}`);
      this.controle_navegacao.navigateBack('/freelancer');
    }
  }

  async excluirPerfil(id: number) {
    const loading = await this.controle_carregamento.create({ message: 'Excluindo perfil...', duration: 30000 });
    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${this.usuario.token}`,
      },
      url: `http://127.0.0.1:8000/freelancer/api/${id}/`,
    };

    try {
      const resposta: HttpResponse = await CapacitorHttp.delete(options);
      if (resposta.status === 204 || resposta.status === 200) {
        loading.dismiss();
        await this.apresenta_mensagem('Perfil excluído com sucesso!', 'success');
        this.controle_navegacao.navigateBack('/freelancer');
      } else {
        loading.dismiss();
        await this.apresenta_mensagem(`Falha ao excluir perfil: código ${resposta.status}`);
      }
    } catch (erro: any) {
      console.error('Erro ao excluir perfil:', erro);
      loading.dismiss();
      await this.apresenta_mensagem(`Erro: ${erro?.status || 'Desconhecido'}`);
    }
  }

  navegarParaEditar(id: number) {
    this.controle_navegacao.navigateForward(`/perfil/${id}`);
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