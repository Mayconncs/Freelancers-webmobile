import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonBackButton, IonList, IonItem, IonLabel,
  IonIcon, IonButton, LoadingController, NavController, ToastController
} from '@ionic/angular/standalone';
import { Storage } from '@ionic/storage-angular';
import { Projeto } from '../projeto.model';
import { Usuario } from '../../home/usuario.model';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-detalhar-projeto',
  templateUrl: './detalhar.page.html',
  styleUrls: ['./detalhar.page.scss'],
  imports: [
    IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonBackButton, IonList, IonItem, IonLabel,
    IonIcon, IonButton, CommonModule,
  ],
  providers: [Storage],
})
export class DetalharProjetoPage implements OnInit {
  public usuario: Usuario = new Usuario();
  public projeto: Projeto = new Projeto();

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
      if (!this.usuario.freelancer_id) {
        await this.carregarPerfilUsuario();
      }
      const id = this.route.snapshot.paramMap.get('id');
      if (id) {
        await this.carregarProjeto(parseInt(id));
      } else {
        await this.apresenta_mensagem('ID do projeto não fornecido.');
        this.controle_navegacao.navigateBack('/projeto');
      }
    } else {
      await this.apresenta_mensagem('Usuário não autenticado.');
      this.controle_navegacao.navigateRoot('/home');
    }
  }

  async carregarPerfilUsuario() {
    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${this.usuario.token}`,
      },
      url: `http://127.0.0.1:8000/freelancer/api/?usuario=${this.usuario.id}`,
    };

    try {
      const resposta: HttpResponse = await CapacitorHttp.get(options);
      if (resposta.status === 200 && resposta.data.length > 0) {
        this.usuario.freelancer_id = resposta.data[0].id;
        await this.storage.set('usuario', this.usuario);
      } else {
        await this.apresenta_mensagem('Perfil não encontrado.');
        this.controle_navegacao.navigateBack('/projeto');
      }
    } catch (erro: any) {
      console.error('Erro ao carregar freelancer:', erro);
      await this.apresenta_mensagem(`Erro ao carregar perfil: ${erro?.status || 'Desconhecido'}`);
    }
  }

  async carregarProjeto(id: number) {
    const loading = await this.controle_carregamento.create({ message: 'Carregando projeto...', duration: 30000 });
    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${this.usuario.token}`,
      },
      url: `http://127.0.0.1:8000/projeto/api/${id}/`,
    };

    try {
      const resposta: HttpResponse = await CapacitorHttp.get(options);
      if (resposta.status === 200) {
        this.projeto = Object.assign(new Projeto(), resposta.data);
        loading.dismiss();
      } else if (resposta.status === 404) {
        loading.dismiss();
        await this.apresenta_mensagem('Projeto não encontrado.');
        this.controle_navegacao.navigateBack('/projeto');
      } else {
        loading.dismiss();
        await this.apresenta_mensagem(`Falha ao carregar projeto: código ${resposta.status}`);
        this.controle_navegacao.navigateBack('/projeto');
      }
    } catch (erro: any) {
      console.error('Erro ao carregar projeto:', erro);
      loading.dismiss();
      await this.apresenta_mensagem(`Erro: ${erro?.status || 'Desconhecido'}`);
      this.controle_navegacao.navigateBack('/projeto');
    }
  }

  async excluirProjeto(id: number) {
    const loading = await this.controle_carregamento.create({ message: 'Excluindo projeto...', duration: 30000 });
    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${this.usuario.token}`,
      },
      url: `http://127.0.0.1:8000/projeto/api/${id}/`,
    };

    try {
      const resposta: HttpResponse = await CapacitorHttp.delete(options);
      if (resposta.status === 204 || resposta.status === 200) {
        loading.dismiss();
        await this.apresenta_mensagem('Projeto excluído com sucesso!', 'success');
        this.controle_navegacao.navigateBack('/projeto');
      } else if (resposta.status === 403) {
        loading.dismiss();
        await this.apresenta_mensagem('Você não tem permissão para excluir este projeto.');
      } else {
        loading.dismiss();
        await this.apresenta_mensagem(`Falha ao excluir projeto: código ${resposta.status}`);
      }
    } catch (erro: any) {
      console.error('Erro ao excluir projeto:', erro);
      loading.dismiss();
      const erroMsg = erro?.data?.detail || JSON.stringify(erro?.data) || `Erro: ${erro?.status || 'Desconhecido'}`;
      await this.apresenta_mensagem(erroMsg);
    }
  }

  navegarParaEditar(id: number) {
    this.controle_navegacao.navigateForward(`/projeto-form/${id}`);
  }

  async apresenta_mensagem(texto: string, cor: string = 'danger') {
    const mensagem = await this.controle_toast.create({
      message: texto,
      cssClass: 'ion-text-center',
      duration: 3000,
      color: cor,
    });
    await mensagem.present();
  }
}