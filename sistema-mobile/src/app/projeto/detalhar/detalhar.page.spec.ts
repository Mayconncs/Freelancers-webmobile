import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DetalharProjetoPage } from './detalhar.page';

describe('DetalharProjetoPage', () => {
  let component: DetalharProjetoPage;
  let fixture: ComponentFixture<DetalharProjetoPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(DetalharProjetoPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
