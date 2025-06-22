import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DetalharPage } from './detalhar.page';

describe('DetalharPage', () => {
  let component: DetalharPage;
  let fixture: ComponentFixture<DetalharPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DetalharPage],
    }).compileComponents();
    fixture = TestBed.createComponent(DetalharPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});