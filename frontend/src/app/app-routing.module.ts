import { Routes } from '@angular/router';
import { StaffListComponent } from './modules/staff/staff-list.component';
import { ScheduleGeneratorComponent } from './modules/schedule/schedule-generator.component';

export const routes: Routes = [
  { path: 'staff', component: StaffListComponent },
  { path: 'schedule', component: ScheduleGeneratorComponent },
  { path: '', redirectTo: '/staff', pathMatch: 'full' }
];
