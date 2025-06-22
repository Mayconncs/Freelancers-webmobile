import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ProjetoPage } from './projeto.page';

describe('ProjetoPage', () => {
  let component: ProjetoPage;
  let fixture: ComponentFixture<ProjetoPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(ProjetoPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
