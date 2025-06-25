export class ClienteInfo {
  public nome: string;
  public telefone: string;
  public email_contato: string;

  constructor() {
    this.nome = '';
    this.telefone = '';
    this.email_contato = '';
  }
}

export class Projeto {
  public id: number;
  public cliente: number;
  public cliente_info: ClienteInfo;
  public titulo: string;
  public descricao: string;
  public habilidades_requeridas: number[];
  public nome_habilidades: string[];
  public estado: string;
  public cidade: string;
  public cep: string;
  public lote: string;
  public status: number;
  public nome_status: string;
  public data_criacao: string;

  constructor() {
    this.id = 0;
    this.cliente = 0;
    this.cliente_info = new ClienteInfo();
    this.titulo = '';
    this.descricao = '';
    this.habilidades_requeridas = [];
    this.nome_habilidades = [];
    this.estado = '';
    this.cidade = '';
    this.cep = '';
    this.lote = '';
    this.status = 1;
    this.nome_status = '';
    this.data_criacao = '';
  }
}