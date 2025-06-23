import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonMenuButton, IonText, IonCard, IonCardContent,
  IonItem, IonLabel, IonButton, IonSearchbar, LoadingController,
  NavController, ToastController
} from '@ionic/angular/standalone';
import { Storage } from '@ionic/storage-angular';
import { Projeto } from './projeto.model';
import { Usuario } from '../home/usuario.model';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';

@Component({
  standalone: true,
  selector: 'app-projeto',
  templateUrl: './projeto.page.html',
  styleUrls: ['./projeto.page.scss'],
  imports: [
    IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonMenuButton, IonText, IonCard, IonCardContent,
    IonItem, IonLabel, IonButton, IonSearchbar, CommonModule, FormsModule,
  ],
  providers: [Storage],
})
export class ProjetoPage implements OnInit {
  public usuario: Usuario = new Usuario();
  public lista_projetos: Projeto[] = [];
  public lista_filtrada: Projeto[] = [];
  public filtro: string = '';

  constructor(
    public storage: Storage,
    public controle_toast: ToastController,
    public controle_navegacao: NavController,
    public controle_carregamento: LoadingController
  ) {}

  async ngOnInit() {
    await this.storage.create();
    const registro = await this.storage.get('usuario');
    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro);
      if (!this.usuario.freelancer_id) {
        await this.carregarPerfilUsuario();
      }
      await this.consultarProjetosSistemaWeb();
    } else {
      this.controle_navegacao.navigateRoot('/home');
    }
  }

  async ionViewWillEnter() {
    await this.consultarProjetosSistemaWeb();
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
      }
    } catch (erro: any) {
      console.error('Erro ao carregar perfil:', erro);
      await this.apresenta_mensagem(`Erro ao carregar perfil: ${erro?.status || 'Desconhecido'}`);
    }
  }

  async consultarProjetosSistemaWeb() {
    const loading = await this.controle_carregamento.create({ message: 'Pesquisando...', duration: 60000 });
    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${this.usuario.token}`,
      },
      url: 'http://127.0.0.1:8000/projeto/api/',
    };

    try {
      const resposta: HttpResponse = await CapacitorHttp.get(options);
      if (resposta.status === 200) {
        this.lista_projetos = resposta.data;
        this.lista_filtrada = [...this.lista_projetos];
        loading.dismiss();
      } else {
        loading.dismiss();
        await this.apresenta_mensagem(`Falha ao consultar projetos: código ${resposta.status}`);
      }
    } catch (erro: any) {
      console.error(erro);
      loading.dismiss();
      await this.apresenta_mensagem(`Erro: ${erro?.status || 'Desconhecido'}`);
    }
  }

  filtrarProjetos() {
    const termo = this.filtro.toLowerCase();
    this.lista_filtrada = this.lista_projetos.filter(projeto =>
      projeto.titulo.toLowerCase().includes(termo) ||
      projeto.cidade?.toLowerCase().includes(termo) ||
      projeto.estado?.toLowerCase().includes(termo) ||
      projeto.nome_habilidades.some(h => h.toLowerCase().includes(termo))
    );
  }

  async excluirProjeto(id: number) {
    const loading = await this.controle_carregamento.create({ message: 'Excluindo...', duration: 30000 });
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
        await this.consultarProjetosSistemaWeb();
        await this.apresenta_mensagem('Projeto excluído com sucesso!', 'success');
      } else if (resposta.status === 403) {
        loading.dismiss();
        await this.apresenta_mensagem('Você não tem permissão para excluir este projeto.');
      } else {
        loading.dismiss();
        await this.apresenta_mensagem(`Falha ao excluir projeto: código ${resposta.status}`);
      }
    } catch (erro: any) {
      console.error(erro);
      loading.dismiss();
      await this.apresenta_mensagem(`Erro: ${erro?.status || 'Desconhecido'}`);
    }
  }

  navegarParaCriarProjeto() {
    this.controle_navegacao.navigateForward('/projeto-form');
  }

  navegarParaDetalhar(id: number) {
    this.controle_navegacao.navigateForward(`/detalhar-projeto/${id}`);
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