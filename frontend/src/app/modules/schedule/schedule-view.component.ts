import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-schedule-view',
  standalone: true,
  template: `
    <div class="container">
      <div class="card">
        <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
          <span>📋 Schedule View</span>
          <div style="display: flex; gap: 0.5rem;">
            <button class="btn btn-secondary" (click)="prevMonth()">◀</button>
            <span style="font-weight: 600;">{{ currentMonth }}</span>
            <button class="btn btn-secondary" (click)="nextMonth()">▶</button>
          </div>
        </div>

        <!-- Legend -->
        <div style="display: flex; gap: 1.5rem; margin: 1rem 0; flex-wrap: wrap;">
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span class="badge badge-morning">M</span> Morning
          </div>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span class="badge badge-evening">E</span> Evening
          </div>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span class="badge badge-night">N</span> Night
          </div>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span class="badge badge-off">O</span> Off
          </div>
        </div>

        <!-- Loading -->
        <div *ngIf="loading" style="text-align: center; padding: 3rem; color: #64748b;">
          ⏳ Loading schedule...
        </div>

        <!-- Calendar Grid -->
        <div *ngIf="!loading" class="table-container">
          <table>
            <thead>
              <tr>
                <th style="min-width: 150px;">Staff</th>
                <th *ngFor="let day of days" style="text-align: center; min-width: 60px;">
                  <div>{{ day.date }}</div>
                  <div style="font-size: 0.75rem; color: #94a3b8;">{{ day.dayShort }}</div>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let row of scheduleGrid">
                <td style="font-weight: 600;">{{ row.staffName }}</td>
                <td *ngFor="let shift of row.shifts" style="text-align: center;">
                  <span class="badge" [ngClass]="getBadgeClass(shift)">
                    {{ shift }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Stats -->
        <div *ngIf="!loading && stats" class="grid grid-3" style="margin-top: 1.5rem;">
          <div class="card" style="text-align: center; background: #dbeafe;">
            <h3 style="color: #1e40af;">{{ stats.totalShifts }}</h3>
            <p style="color: #3b82f6;">Total Shifts</p>
          </div>
          <div class="card" style="text-align: center; background: #d1fae5;">
            <h3 style="color: #065f46;">{{ stats.nightShifts }}</h3>
            <p style="color: #10b981;">Night Shifts</p>
          </div>
          <div class="card" style="text-align: center; background: #fef3c7;">
            <h3 style="color: #92400e;">{{ stats.offDays }}</h3>
            <p style="color: #f59e0b;">Off Days</p>
          </div>
        </div>
      </div>
    </div>
  `,
  imports: [CommonModule]
})
export class ScheduleViewComponent implements OnInit {
  currentDate = new Date();
  currentMonth = '';
  days: any[] = [];
  scheduleGrid: any[] = [];
  loading = false;
  stats: any = null;

  constructor(private apiService: ApiService) { }

  ngOnInit() {
    this.updateMonth();
    this.loadSchedule();
  }

  updateMonth() {
    this.currentMonth = this.currentDate.toLocaleString('default', { month: 'long', year: 'numeric' });
    this.generateDays();
  }

  generateDays() {
    const year = this.currentDate.getFullYear();
    const month = this.currentDate.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);

    this.days = [];
    for (let d = new Date(firstDay); d <= lastDay; d.setDate(d.getDate() + 1)) {
      this.days.push({
        date: d.getDate(),
        dayShort: d.toLocaleString('default', { weekday: 'short' }),
        fullDate: new Date(d)
      });
    }
  }

  prevMonth() {
    this.currentDate = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() - 1, 1);
    this.updateMonth();
    this.loadSchedule();
  }

  nextMonth() {
    this.currentDate = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1, 1);
    this.updateMonth();
    this.loadSchedule();
  }

  loadSchedule() {
    this.loading = true;
    const year = this.currentDate.getFullYear();
    const month = this.currentDate.getMonth() + 1;

    this.apiService.get<any[]>(`/api/v1/schedules/month/${year}/${month}`).subscribe({
      next: (schedules) => {
        this.processSchedules(schedules);
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading schedule:', err);
        this.loading = false;
      }
    });
  }

  processSchedules(schedules: any[]) {
    // TODO: Process schedule entries into grid format
    this.stats = {
      totalShifts: 0,
      nightShifts: 0,
      offDays: 0
    };
  }

  getBadgeClass(shift: string): string {
    switch (shift) {
      case 'M': return 'badge-morning';
      case 'E': return 'badge-evening';
      case 'N': return 'badge-night';
      default: return 'badge-off';
    }
  }
}
