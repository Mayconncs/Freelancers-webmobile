export class Usuario {
  public id: number;
  public nome: string;
  public email: string;
  public token: string;
  public papel: number;

  constructor() {
    this.id = 0;
    this.nome = '';
    this.email = '';
    this.token = '';
    this.papel = 0;
  }
}