import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-schedule-generator',
  template: `
    <h2>Generate Schedule</h2>
    <div>
      <label>Start Date</label>
      <input type="date" [(ngModel)]="startDate" />
    </div>
    <div>
      <label>End Date</label>
      <input type="date" [(ngModel)]="endDate" />
    </div>
    <button (click)="generate()">Generate</button>
  `,
  imports: [FormsModule]
})
export class ScheduleGeneratorComponent {
  startDate: string = '';
  endDate: string = '';
  
  constructor(private http: HttpClient) {}
  
  generate() {
    this.http.post('http://localhost:8000/api/v1/schedules/generate', {
      start_date: this.startDate,
      end_date: this.endDate
    }).subscribe(response => {
      console.log('Schedule generated', response);
    });
  }
}
