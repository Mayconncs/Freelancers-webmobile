import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonMenuButton, IonText, IonCard, IonCardContent,
  IonItem, IonThumbnail, IonLabel, IonItemOptions, IonItemOption, IonIcon, IonButton, IonSearchbar, LoadingController,
  NavController, ToastController
} from '@ionic/angular/standalone';
import { Storage } from '@ionic/storage-angular';
import { Freelancer } from './freelancer.model';
import { Usuario } from '../home/usuario.model';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { AppComponent } from '../app.component';

@Component({
  standalone: true,
  selector: 'app-freelancer',
  templateUrl: './freelancer.page.html',
  styleUrls: ['./freelancer.page.scss'],
  imports: [
    IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonMenuButton, IonText, IonCard, IonCardContent,
    IonItem, IonThumbnail, IonLabel, IonItemOptions, IonItemOption, IonIcon, IonButton, IonSearchbar, CommonModule, FormsModule,
  ],
  providers: [Storage],
})
export class FreelancerPage implements OnInit {
  public usuario: Usuario = new Usuario();
  public lista_freelancers: Freelancer[] = [];
  public lista_filtrada: Freelancer[] = [];
  public filtro: string = '';

  constructor(
    public storage: Storage,
    public controle_toast: ToastController,
    public controle_navegacao: NavController,
    public controle_carregamento: LoadingController,
    private appComponent: AppComponent
  ) {}

  async ngOnInit() {
    await this.storage.create();
    const registro = await this.storage.get('usuario');
    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro);
      await this.consultarFreelancersSistemaWeb();
    } else {
      this.controle_navegacao.navigateRoot('/home');
    }
  }

  async ionViewWillEnter() {
    await this.appComponent.checkAuthStatus();
    await this.consultarFreelancersSistemaWeb();
  }

  async consultarFreelancersSistemaWeb() {
    const loading = await this.controle_carregamento.create({ message: 'Pesquisando...', duration: 60000 });
    await loading.present();

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
        this.lista_freelancers = resposta.data;
        this.lista_filtrada = [...this.lista_freelancers];
        loading.dismiss();
      } else {
        loading.dismiss();
        await this.apresenta_mensagem(`Falha ao consultar freelancers: código ${resposta.status}`);
      }
    } catch (erro: any) {
      console.error(erro);
      loading.dismiss();
      await this.apresenta_mensagem(`Erro: ${erro?.status || 'Desconhecido'}`);
    }
  }

  filtrarFreelancers() {
    const termo = this.filtro.toLowerCase();
    this.lista_filtrada = this.lista_freelancers.filter(freelancer =>
      freelancer.nome.toLowerCase().includes(termo) ||
      freelancer.cidade?.toLowerCase().includes(termo) ||
      freelancer.estado?.toLowerCase().includes(termo) ||
      freelancer.nome_habilidades.some(h => h.toLowerCase().includes(termo))
    );
  }

  async excluirFreelancer(id: number) {
    const loading = await this.controle_carregamento.create({ message: 'Excluindo...', duration: 30000 });
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
      if (resposta.status === 200) {
        loading.dismiss();
        await this.consultarFreelancersSistemaWeb();
        await this.apresenta_mensagem('Perfil excluído com sucesso!', 'success');
      } else {
        loading.dismiss();
        await this.apresenta_mensagem(`Falha ao excluir perfil: código ${resposta.status}`);
      }
    } catch (erro: any) {
      console.error(erro);
      loading.dismiss();
      await this.apresenta_mensagem(`Erro: ${erro?.status || 'Desconhecido'}`);
    }
  }

  navegarParaCriarPerfil() {
    this.controle_navegacao.navigateForward('/perfil');
  }

  navegarParaDetalhar(id: number) {
    this.controle_navegacao.navigateForward(`/detalhar/${id}`);
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