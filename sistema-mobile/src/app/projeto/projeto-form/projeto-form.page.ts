import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, NgForm } from '@angular/forms';
import {
  IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonBackButton, IonList, IonItem, IonInput, IonButton,
  IonSelect, IonSelectOption, IonTextarea, LoadingController, NavController, ToastController
} from '@ionic/angular/standalone';
import { Storage } from '@ionic/storage-angular';
import { Projeto } from '../projeto.model';
import { Usuario } from '../../home/usuario.model';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-projeto-form',
  templateUrl: './projeto-form.page.html',
  styleUrls: ['./projeto-form.page.scss'],
  imports: [
    IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonBackButton, IonList, IonItem, IonInput, IonButton,
    IonSelect, IonSelectOption, IonTextarea, CommonModule, FormsModule,
  ],
  providers: [Storage],
})
export class ProjetoFormPage implements OnInit {
  public usuario: Usuario = new Usuario();
  public projeto: Projeto = new Projeto();
  public isEditing: boolean = false;

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
        this.isEditing = true;
        await this.carregarProjeto(parseInt(id));
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
        await this.apresenta_mensagem('Perfil não encontrado. Crie um perfil primeiro.');
        this.controle_navegacao.navigateRoot('/perfil');
      }
    } catch (erro: any) {
      console.error('Erro ao carregar perfil:', erro);
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
        this.projeto.habilidades_requeridas = this.projeto.habilidades_requeridas.map(Number);
        loading.dismiss();
      } else if (resposta.status === 403) {
        loading.dismiss();
        await this.apresenta_mensagem('Você não tem permissão para editar este projeto.');
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

  async salvarProjeto() {
    const loading = await this.controle_carregamento.create({ message: 'Salvando...', duration: 30000 });
    await loading.present();

    const formData = new FormData();
    formData.append('titulo', this.projeto.titulo);
    formData.append('descricao', this.projeto.descricao);
    formData.append('habilidades_requeridas', JSON.stringify(this.projeto.habilidades_requeridas));
    formData.append('estado', this.projeto.estado || '');
    formData.append('cidade', this.projeto.cidade || '');
    formData.append('cep', this.projeto.cep || '');
    formData.append('lote', this.projeto.lote || '');
    formData.append('status', this.projeto.status.toString());
    formData.append('cliente', this.usuario.freelancer_id.toString()); // Alterado para freelancer_id

    const options: HttpOptions = {
      headers: {
        Authorization: `Token ${this.usuario.token}`,
      },
      url: this.isEditing
        ? `http://127.0.0.1:8000/projeto/api/${this.projeto.id}/`
        : 'http://127.0.0.1:8000/projeto/api/',
      data: formData,
    };

    const method = this.isEditing ? CapacitorHttp.put : CapacitorHttp.post;
    try {
      const resposta: HttpResponse = await method(options);
      if (resposta.status === 200 || resposta.status === 201) {
        loading.dismiss();
        await this.apresenta_mensagem('Projeto salvo com sucesso!', 'success');
        this.controle_navegacao.navigateBack('/projeto');
      } else {
        loading.dismiss();
        const erroMsg = resposta.data?.detail || JSON.stringify(resposta.data) || `Código ${resposta.status}`;
        await this.apresenta_mensagem(`Falha ao salvar projeto: ${erroMsg}`);
      }
    } catch (erro: any) {
      console.error('Erro ao salvar projeto:', erro);
      loading.dismiss();
      const erroMsg = erro?.data?.detail || JSON.stringify(erro?.data) || `Erro: ${erro?.status || 'Desconhecido'}`;
      await this.apresenta_mensagem(erroMsg);
    }
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