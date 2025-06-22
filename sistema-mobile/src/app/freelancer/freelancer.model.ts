export class Freelancer {
  public id: number;
  public usuario: number;
  public nome: string;
  public papel: number;
  public nome_papel: string;
  public estado: string;
  public cidade: string;
  public cep: string;
  public lote: string;
  public telefone: string;
  public email_contato: string;
  public habilidades: number[];
  public nome_habilidades: string[];
  public bio: string;
  public foto: string | undefined;

  constructor() {
    this.id = 0;
    this.usuario = 0;
    this.nome = '';
    this.papel = 0;
    this.nome_papel = '';
    this.estado = '';
    this.cidade = '';
    this.cep = '';
    this.lote = '';
    this.telefone = '';
    this.email_contato = '';
    this.habilidades = [];
    this.nome_habilidades = [];
    this.bio = '';
  }
}