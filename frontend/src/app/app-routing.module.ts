import { Routes } from '@angular/router';
import { DashboardComponent } from './modules/dashboard/dashboard.component';
import { StaffListComponent } from './modules/staff/staff-list.component';
import { ScheduleGeneratorComponent } from './modules/schedule/schedule-generator.component';
import { ScheduleViewComponent } from './modules/schedule/schedule-view.component';
import { ScheduleEditComponent } from './modules/schedule/schedule-edit.component';

export const routes: Routes = [
  { path: '', component: DashboardComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'staff', component: StaffListComponent },
  { path: 'schedule', component: ScheduleViewComponent },
  { path: 'schedule/generate', component: ScheduleGeneratorComponent },
  { path: 'schedule/view/:id', component: ScheduleViewComponent },
  { path: 'schedule/edit/:id', component: ScheduleEditComponent }
];
