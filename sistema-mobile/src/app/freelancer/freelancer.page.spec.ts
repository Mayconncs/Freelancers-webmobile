import { ComponentFixture, TestBed } from '@angular/core/testing';
import { FreelancerPage } from './freelancer.page';

describe('FreelancerPage', () => {
  let component: FreelancerPage;
  let fixture: ComponentFixture<FreelancerPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FreelancerPage],
    }).compileComponents();
    fixture = TestBed.createComponent(FreelancerPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});