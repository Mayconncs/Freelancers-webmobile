import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'home',
    loadComponent: () => import('./home/home.page').then((m) => m.HomePage),
  },
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full',
  },
  {
    path: 'cadastro',
    loadComponent: () => import('./cadastro/cadastro.page').then((m) => m.CadastroPage),
  },
  {
    path: 'freelancer',
    loadComponent: () => import('./freelancer/freelancer.page').then((m) => m.FreelancerPage),
  },
  {
    path: 'perfil',
    loadComponent: () => import('./perfil/perfil.page').then((m) => m.PerfilPage),
  },
  {
    path: 'perfil/:id',
    loadComponent: () => import('./perfil/perfil.page').then((m) => m.PerfilPage),
  },
  {
    path: 'detalhar/:id',
    loadComponent: () => import('./detalhar/detalhar.page').then((m) => m.DetalharPage),
  },
  {
    path: 'projeto',
    loadComponent: () => import('./projeto/projeto.page').then((m) => m.ProjetoPage),
  },
  {
    path: 'projeto-form',
    loadComponent: () => import('./projeto/projeto-form/projeto-form.page').then((m) => m.ProjetoFormPage),
  },
  {
    path: 'projeto-form/:id',
    loadComponent: () => import('./projeto/projeto-form/projeto-form.page').then((m) => m.ProjetoFormPage),
  },
  {
    path: 'detalhar-projeto/:id',
    loadComponent: () => import('./projeto/detalhar/detalhar.page').then((m) => m.DetalharProjetoPage),
  },
];