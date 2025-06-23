export class Usuario {
  public id: number;
  public username: string;
  public email: string;
  public token: string;
  public nome: string;
  public perfil_id: number; 
  public freelancer_id: number; 

  constructor() {
    this.id = 0;
    this.username = '';
    this.email = '';
    this.token = '';
    this.nome = '';
    this.perfil_id = 0;
    this.freelancer_id = 0;
  }
}