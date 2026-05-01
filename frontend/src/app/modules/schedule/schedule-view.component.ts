import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-schedule-view',
  template: `
    <h2>Schedule View</h2>
    <div *ngIf="schedule">
      <pre>{{ schedule | json }}</pre>
    </div>
  `
})
export class ScheduleViewComponent implements OnInit {
  schedule: any = null;
  
  constructor(private http: HttpClient) {}
  
  ngOnInit() {
    // Load schedule by month
    const now = new Date();
    this.http.get<any[]>(`http://localhost:8000/api/v1/schedules/month/${now.getFullYear()}/${now.getMonth() + 1}`)
      .subscribe(data => {
        this.schedule = data;
      });
  }
}
