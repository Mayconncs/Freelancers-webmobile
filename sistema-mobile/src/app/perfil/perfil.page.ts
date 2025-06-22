import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, NgForm } from '@angular/forms';
import {
  IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonBackButton, IonList, IonItem, IonInput, IonButton,
  IonSelect, IonSelectOption, IonTextarea, LoadingController, NavController, ToastController
} from '@ionic/angular/standalone';
import { Storage } from '@ionic/storage-angular';
import { Freelancer } from '../freelancer/freelancer.model';
import { Usuario } from '../home/usuario.model';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-perfil',
  templateUrl: './perfil.page.html',
  styleUrls: ['./perfil.page.scss'],
  imports: [
    IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonBackButton, IonList, IonItem, IonInput, IonButton,
    IonSelect, IonSelectOption, IonTextarea, CommonModule, FormsModule,
  ],
  providers: [Storage],
})
export class PerfilPage implements OnInit {
  public usuario: Usuario = new Usuario();
  public freelancer: Freelancer = new Freelancer();
  public isEditing: boolean = false;
  public selectedFile: File | null = null;

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
        this.isEditing = true;
        await this.carregarPerfil(parseInt(id));
      }
    } else {
      this.controle_navegacao.navigateRoot('/home');
    }
  }

  async carregarPerfil(id: number) {
    const loading = await this.controle_carregamento.create({ message: 'Carregando...', duration: 30000 });
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
      } else {
        loading.dismiss();
        await this.apresenta_mensagem(`Falha ao carregar perfil: código ${resposta.status}`);
      }
    } catch (erro: any) {
      console.error(erro);
      loading.dismiss();
      await this.apresenta_mensagem(`Erro: ${erro?.status || 'Desconhecido'}`);
    }
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
    }
  }

  async salvarPerfil() {
    const loading = await this.controle_carregamento.create({ message: 'Salvando...', duration: 30000 });
    await loading.present();

    const formData = new FormData();
    formData.append('nome', this.freelancer.nome);
    formData.append('papel', this.freelancer.papel.toString());
    formData.append('estado', this.freelancer.estado || '');
    formData.append('cidade', this.freelancer.cidade || '');
    formData.append('cep', this.freelancer.cep || '');
    formData.append('lote', this.freelancer.lote || '');
    formData.append('telefone', this.freelancer.telefone || '');
    formData.append('email_contato', this.freelancer.email_contato || '');
    formData.append('habilidades', JSON.stringify(this.freelancer.habilidades));
    formData.append('bio', this.freelancer.bio || '');
    if (this.selectedFile) {
      formData.append('foto', this.selectedFile);
    }
    formData.append('usuario', this.usuario.id.toString());


    const options: HttpOptions = {
      headers: {
        Authorization: `Token ${this.usuario.token}`,
      },
      url: this.isEditing
        ? `http://127.0.0.1:8000/freelancer/api/${this.freelancer.id}/`
        : 'http://127.0.0.1:8000/freelancer/api/',
      data: formData,
    };

    const method = this.isEditing ? CapacitorHttp.put : CapacitorHttp.post;
    try {
      const resposta: HttpResponse = await method(options);
      if (resposta.status === 200 || resposta.status === 201) {
        loading.dismiss();
        await this.apresenta_mensagem('Perfil salvo com sucesso!', 'success');
        this.controle_navegacao.navigateBack('/freelancer');
      } else {
        loading.dismiss();
        await this.apresenta_mensagem(`Falha ao salvar perfil: código ${resposta.status}`);
      }
    } catch (erro: any) {
      console.error(erro);
      loading.dismiss();
      await this.apresenta_mensagem(`Erro: ${erro?.status || 'Desconhecido'}`);
    }
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